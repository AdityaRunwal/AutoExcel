// API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000';

// State Variables
let selectedFile = null;

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const dropzonePrompt = document.getElementById('dropzone-prompt');
const fileDetails = document.getElementById('file-details');
const fileNameSpan = document.getElementById('file-name');
const fileSizeSpan = document.getElementById('file-size');
const removeFileBtn = document.getElementById('remove-file-btn');

const cleanForm = document.getElementById('clean-form');
const promptInput = document.getElementById('prompt-input');
const submitBtn = document.getElementById('submit-btn');
const btnText = submitBtn.querySelector('.btn-text');
const spinner = document.getElementById('spinner');

const statusMessage = document.getElementById('status-message');
const downloadContainer = document.getElementById('download-container');
const downloadFilename = document.getElementById('download-filename');
const downloadBtn = document.getElementById('download-btn');

const planContainer = document.getElementById('plan-container');
const planStepsList = document.getElementById('plan-steps-list');
const planSkippedList = document.getElementById('plan-skipped-list');
const applyPlanBtn = document.getElementById('apply-plan-btn');
const cancelPlanBtn = document.getElementById('cancel-plan-btn');

const summaryContainer = document.getElementById('summary-container');
const summaryStatus = document.getElementById('summary-status');
const beforeRows = document.getElementById('before-rows');
const beforeColumns = document.getElementById('before-columns');
const beforeMissing = document.getElementById('before-missing');
const beforeDuplicates = document.getElementById('before-duplicates');

const afterRows = document.getElementById('after-rows');
const afterColumns = document.getElementById('after-columns');
const afterMissing = document.getElementById('after-missing');
const afterDuplicates = document.getElementById('after-duplicates');

const rowsRemoved = document.getElementById('rows-removed');
const columnsRemoved = document.getElementById('columns-removed');
const missingChanged = document.getElementById('missing-changed');
const duplicatesRemoved = document.getElementById('duplicates-removed');
const operationsList = document.getElementById('operations-list');

const datasetContainer = document.getElementById('dataset-container');

const datasetRows = document.getElementById('dataset-rows');
const datasetColumns = document.getElementById('dataset-columns');
const datasetMissing = document.getElementById('dataset-missing');
const datasetDuplicates = document.getElementById('dataset-duplicates');
const datasetEmptyRows = document.getElementById('dataset-empty-rows');
const datasetEmptyColumns = document.getElementById('dataset-empty-columns');

const datasetPreviewHead = document.getElementById('dataset-preview-head');
const datasetPreviewBody = document.getElementById('dataset-preview-body');

const refreshHistoryBtn = document.getElementById('refresh-history-btn');
const historyTbody = document.getElementById('history-tbody');

async function fetchDatasetInfo(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(
                errorData?.detail || 'Unable to analyze the dataset.'
            );
        }

        const data = await response.json();

        // Dataset information
        datasetRows.textContent = data.rows;
        datasetColumns.textContent = data.columns;
        datasetMissing.textContent = data.total_missing_values;
        datasetDuplicates.textContent = data.duplicate_rows;
        datasetEmptyRows.textContent = data.empty_rows;
        datasetEmptyColumns.textContent = data.empty_columns;

        // Preview table
        renderDatasetPreview(data.preview, data.column_names);

        datasetContainer.classList.remove('hidden');

    } catch (error) {
        console.error('Dataset information error:', error);

        datasetContainer.classList.add('hidden');

        showStatus(
            `Unable to analyze dataset: ${error.message}`,
            'error'
        );
    }
}

function renderDatasetPreview(rows, columns) {
    datasetPreviewHead.innerHTML = '';
    datasetPreviewBody.innerHTML = '';

    if (!rows || rows.length === 0) {
        datasetPreviewBody.innerHTML = `
            <tr>
                <td colspan="100%" class="table-state-cell">
                    No preview data available.
                </td>
            </tr>
        `;
        return;
    }

    const headerRow = document.createElement('tr');

    columns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column;
        headerRow.appendChild(th);
    });

    datasetPreviewHead.appendChild(headerRow);

    rows.forEach(row => {
        const tr = document.createElement('tr');

        columns.forEach(column => {
            const td = document.createElement('td');

            const value = row[column];

            td.textContent =
                value === null || value === undefined
                    ? ''
                    : value;

            tr.appendChild(td);
        });

        datasetPreviewBody.appendChild(tr);
    });
}

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateSubmitButtonState();
    fetchHistory();
});

// Event Listeners Setup
function setupEventListeners() {
    // Dropzone Click
    dropzone.addEventListener('click', () => {
        if (!selectedFile && !submitBtn.disabled && spinner.classList.contains('hidden')) {
            fileInput.click();
        }
    });

    // Dropzone Keyboard Accessibility
    dropzone.addEventListener('keydown', (e) => {
        if ((e.key === 'Enter' || e.key === ' ') && !selectedFile && spinner.classList.contains('hidden')) {
            e.preventDefault();
            fileInput.click();
        }
    });

    // File Input Change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Prompt Input Listener for validation
    promptInput.addEventListener('input', () => {
        updateSubmitButtonState();
    });

    // Drag & Drop
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (spinner.classList.contains('hidden')) {
                dropzone.classList.add('dragover');
            }
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        if (!spinner.classList.contains('hidden')) return;
        const dt = e.dataTransfer;
        if (dt.files && dt.files.length > 0) {
            handleFileSelect(dt.files[0]);
        }
    });

    // Remove File
    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        clearSelectedFile();
    });

    // Form Submit (now shows plan preview instead of cleaning immediately)
    cleanForm.addEventListener('submit', handlePreviewSubmit);

    // Apply Plan Button
    applyPlanBtn.addEventListener('click', handleApplyPlan);

    // Cancel Plan Button
    cancelPlanBtn.addEventListener('click', () => {
        planContainer.classList.add('hidden');
    });

    // Refresh History Button
    refreshHistoryBtn.addEventListener('click', fetchHistory);
}

// Update Submit Button State (Disabled unless file is selected AND prompt is not empty)
function updateSubmitButtonState() {
    const isFileSelected = !!selectedFile;
    const isPromptNotEmpty = promptInput.value.trim().length > 0;
    submitBtn.disabled = !(isFileSelected && isPromptNotEmpty);
}

// File Selection Handler
function handleFileSelect(file) {
    const validExtensions = ['.xlsx', '.xls', '.csv'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));

    if (!isValid) {
        showStatus('Please select a valid dataset file (.xlsx, .xls, .csv).', 'error');
        return;
    }

    selectedFile = file;
    fileNameSpan.textContent = file.name;
    fileSizeSpan.textContent = `(${formatFileSize(file.size)})`;

    dropzonePrompt.classList.add('hidden');
    fileDetails.classList.remove('hidden');
    hideStatus();
    updateSubmitButtonState();

    fetchDatasetInfo(file);
}

// Clear Selected File
function clearSelectedFile() {
    selectedFile = null;
    fileInput.value = '';
    fileNameSpan.textContent = '';
    fileSizeSpan.textContent = '';

    fileDetails.classList.add('hidden');
    dropzonePrompt.classList.remove('hidden');
    updateSubmitButtonState();
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form Submission Handler (POST /preview-plan) - shows the plan, does not clean yet
async function handlePreviewSubmit(e) {
    e.preventDefault();

    if (!selectedFile || promptInput.value.trim().length === 0) {
        return;
    }

    const promptText = promptInput.value.trim();

    setLoadingState(true);
    hideStatus();
    downloadContainer.classList.add('hidden');
    summaryContainer.classList.add('hidden');
    planContainer.classList.add('hidden');

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('prompt', promptText);

        const response = await fetch(`${API_BASE_URL}/preview-plan`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            let errorText = 'Failed to build a cleaning plan.';

            try {
                const errJson = await response.json();
                if (errJson && errJson.detail) {
                    errorText = errJson.detail;
                }
            } catch (_) {
                // Response was not JSON
            }

            throw new Error(errorText);
        }

        const data = await response.json();

        if (!data.has_plan || !data.steps || data.steps.length === 0) {
            const msg = data.message
                ? `⚠ ${data.message}`
                : '⚠ No supported cleaning operation was detected in your prompt.';
            showStatus(msg, 'error');
            return;
        }

        renderPlan(data.steps, data.skipped_steps || []);
        planContainer.classList.remove('hidden');

    } catch (err) {
        console.error('Error building plan:', err);
        showStatus(
            `Error: ${err.message || 'Unable to connect to FastAPI backend at http://127.0.0.1:8000.'}`,
            'error'
        );
    } finally {
        setLoadingState(false);
    }
}

// Render the plan steps and any skipped steps
function renderPlan(steps, skippedSteps) {
    planStepsList.innerHTML = steps
        .map((step, index) => `<div>${index + 1}. ${escapeHtml(step.description)}</div>`)
        .join('');

    if (skippedSteps.length > 0) {
        planSkippedList.innerHTML = '<h3>Skipped Steps</h3>' + skippedSteps
            .map(step => `<div>⚠ ${escapeHtml(step.operation)}: ${escapeHtml(step.reason)}</div>`)
            .join('');
    } else {
        planSkippedList.innerHTML = '';
    }
}

// Apply Plan Button Handler (POST /ai-clean) - actually cleans the dataset
async function handleApplyPlan() {
    if (!selectedFile || promptInput.value.trim().length === 0) {
        return;
    }

    const promptText = promptInput.value.trim();

    setLoadingState(true);
    hideStatus();
    downloadContainer.classList.add('hidden');
    summaryContainer.classList.add('hidden');

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('prompt', promptText);

        const response = await fetch(`${API_BASE_URL}/ai-clean`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            let errorText = 'Failed to clean the dataset.';

            try {
                const errJson = await response.json();

                if (errJson && errJson.detail) {
                    errorText = errJson.detail;
                }
            } catch (_) {
                // Response was not JSON
            }

            throw new Error(errorText);
        }

        const contentType = response.headers.get('content-type') || '';

        // Handle JSON responses such as no_operation or error
        if (contentType.includes('application/json')) {
            const data = await response.json();

            if (data && data.status === 'no_operation') {
                const suggestions = (data.suggestions || [])
                    .map(item => `• ${item}`)
                    .join('\n');

                showStatus(
                    `⚠ ${data.message}\n\nTry one of these:\n${suggestions}`,
                    'error'
                );

                return;
            }

            if (data && data.status === 'error') {
                showStatus(
                    `✕ ${data.message || 'Unable to process the dataset.'}`,
                    'error'
                );

                return;
            }

            // Catch-all: some other JSON shape came back — stop here, do NOT fall through to blob()
            showStatus('Unexpected response from server.', 'error');
            return;
        }

        // Only reached when the response was NOT JSON — safe to read as blob exactly once
        const blob = await response.blob();

        // Use the actual filename the server sent back (it may differ from the
        // original upload, e.g. a CSV upgraded to .xlsx when a summary sheet was requested)
        const disposition = response.headers.get('content-disposition') || '';
        const filenameMatch = disposition.match(/filename="?([^"]+)"?/);
        const cleanedFileName = filenameMatch ? filenameMatch[1] : `cleaned_${selectedFile.name}`;

        const downloadUrl = window.URL.createObjectURL(blob);

        downloadBtn.href = downloadUrl;
        downloadBtn.download = cleanedFileName;
        downloadFilename.textContent = cleanedFileName;

        downloadBtn.onclick = () => {
            setTimeout(() => {
                window.URL.revokeObjectURL(downloadUrl);
            }, 1000);
        };

        downloadContainer.classList.remove('hidden');
        planContainer.classList.add('hidden');

        showStatus(
            '✓ Your file has been cleaned successfully.',
            'success'
        );

        await fetchSummary();
        fetchHistory();

    } catch (err) {
        console.error('Error cleaning dataset:', err);

        showStatus(
            `Error: ${err.message || 'Unable to connect to FastAPI backend at http://127.0.0.1:8000.'}`,
            'error'
        );

    } finally {
        setLoadingState(false);
    }
}

// Fetch and Render Cleaning Summary
async function fetchSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/summary`);
        if (!response.ok) {
            throw new Error(`Failed to fetch summary: ${response.statusText}`);
        }
        const data = await response.json();
        renderSummary(data);
        summaryContainer.classList.remove('hidden');
    } catch (error) {
        console.error('Error fetching cleaning summary:', error);
    }
}

// Render the Cleaning Summary section
function renderSummary(data) {
    const before = data.before || {};
    const after = data.after || {};
    const changes = data.changes || {};
    const operations = data.operations || [];
    const validation = data.validation || null;

    beforeRows.textContent = before.rows ?? '—';
    beforeColumns.textContent = before.columns ?? '—';
    beforeMissing.textContent = before.missing_values ?? '—';
    beforeDuplicates.textContent = before.duplicate_rows ?? '—';

    afterRows.textContent = after.rows ?? '—';
    afterColumns.textContent = after.columns ?? '—';
    afterMissing.textContent = after.missing_values ?? '—';
    afterDuplicates.textContent = after.duplicate_rows ?? '—';

    rowsRemoved.textContent = changes.rows_removed ?? '—';
    columnsRemoved.textContent = changes.columns_removed ?? '—';
    missingChanged.textContent = changes.missing_values_changed ?? '—';
    duplicatesRemoved.textContent = changes.duplicates_removed ?? '—';

    operationsList.innerHTML = operations.length > 0
        ? operations.map(op => `<span>${escapeHtml(formatOperationName(op))}</span>`).join(', ')
        : '<p>No operations detected.</p>';

    if (validation && validation.status === 'warning' && validation.warnings && validation.warnings.length > 0) {
        summaryStatus.textContent = '⚠ Cleaning completed with warnings';
        summaryStatus.className = 'summary-status summary-status-warning';

        const warningHtml = '<div class="summary-warning-box"><strong>Validation Warnings</strong><ul>' +
            validation.warnings.map(w => `<li>${escapeHtml(w)}</li>`).join('') +
            '</ul></div>';

        operationsList.innerHTML += warningHtml;
    } else {
        summaryStatus.textContent = '✓ Cleaning completed successfully';
        summaryStatus.className = 'summary-status';
    }
}

// Fetch Cleaning History
async function fetchHistory() {
    console.log('fetchHistory called');
    try {
        const response = await fetch(`${API_BASE_URL}/history`);
        console.log('fetchHistory response status:', response.status);
        if (!response.ok) {
            throw new Error(`Failed to fetch history: ${response.statusText}`);
        }
        const data = await response.json();
        renderHistoryTable(data);
    } catch (error) {
        console.error('Error fetching cleaning history:', error);
        if (historyTbody) {
            historyTbody.innerHTML = `
                <tr>
                    <td colspan="5" class="table-state-cell">
                        Unable to load cleaning history.
                    </td>
                </tr>
            `;
        }
    }
}

// Render History Table Rows
function renderHistoryTable(history) {
    if (!history || history.length === 0) {
        historyTbody.innerHTML = `
            <tr>
                <td colspan="5" class="table-state-cell">
                    No cleaning history yet. Your cleaned files will appear here.
                </td>
            </tr>
        `;
        return;
    }

    const sorted = [...history].reverse();

    historyTbody.innerHTML = sorted.map(item => {
        const dateStr = item.created_at ? new Date(item.created_at).toLocaleString() : 'N/A';
        const operationsStr = item.operations || 'None';

        const formattedOperations = operationsStr !== 'None'
            ? operationsStr
                .split(',')
                .map(operation => formatOperationName(operation.trim()))
                .join(', ')
            : 'None';
        const rawStatus = (item.status || 'completed').toLowerCase();

        const displayStatus = rawStatus.charAt(0).toUpperCase() + rawStatus.slice(1);
        const promptText = escapeHtml(item.prompt || '');

        return `
            <tr>
                <td><strong>${escapeHtml(item.filename)}</strong></td>
                <td class="prompt-cell" title="${promptText}">${promptText}</td>
                <td><code>${escapeHtml(formattedOperations)}</code></td>
                <td>
                    <span class="status-pill status-${rawStatus}">
                        ${escapeHtml(displayStatus)}
                    </span>
                </td>
                <td>${dateStr}</td>
            </tr>
        `;
    }).join('');
}

// UI State Helpers
function setLoadingState(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        btnText.textContent = 'Cleaning...';
        spinner.classList.remove('hidden');
        promptInput.disabled = true;
        removeFileBtn.disabled = true;
        dropzone.style.pointerEvents = 'none';
    } else {
        btnText.textContent = 'Clean Dataset';
        spinner.classList.add('hidden');
        promptInput.disabled = false;
        removeFileBtn.disabled = false;
        dropzone.style.pointerEvents = 'auto';
        updateSubmitButtonState();
    }
}

function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
}

function hideStatus() {
    statusMessage.textContent = '';
    statusMessage.className = 'status-message hidden';
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function formatOperationName(operation) {
    const names = {
        remove_duplicates: 'Remove Duplicate Rows',
        fill_missing_mean: 'Fill Missing Values with Mean',
        fill_missing_median: 'Fill Missing Values with Median',
        fill_missing_mode: 'Fill Missing Values with Mode',
        remove_empty_rows: 'Remove Empty Rows',
        remove_empty_columns: 'Remove Empty Columns',
        standardize_columns: 'Standardize Column Names',
        remove_negative_values: 'Remove Negative Values',
        remove_extra_spaces: 'Remove Extra Spaces',
        remove_missing: 'Remove Rows with Missing Values',
        convert_numeric: 'Convert Columns to Numeric',
        remove_duplicate_columns: 'Remove Duplicate Columns',
        replace_negative_with_mean: 'Replace Negative Values with Mean',
        remove_invalid_rows: 'Remove Invalid Rows'
    };

    return names[operation] || operation;
}
