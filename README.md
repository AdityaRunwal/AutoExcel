**# 🚀 AutoExcel**

**### Natural-Language Data Cleaning for Excel & CSV Files**

[![Python]\(https\://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)]\()

[![FastAPI]\(https\://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)]\()

[![PostgreSQL]\(https\://img.shields.io/badge/PostgreSQL-database-336791?logo=postgresql&logoColor=white)]\()

[![Tests]\(https\://img.shields.io/badge/tests-71%20passing-brightgreen?logo=pytest&logoColor=white)]\()

[![License]\(https\://img.shields.io/badge/license-learning%20project-lightgrey)]\()

\<details>

\<summary>\<strong>📋 Table of Contents\</strong>\</summary>

\- [Why AutoExcel?]\(#-why-autoexcel)

\- [Project Objective]\(#-project-objective)

\- [Key Features]\(#-key-features)

\- [Supported Data-Cleaning Operations]\(#-supported-data-cleaning-operations)

\- [Example Prompts]\(#-example-prompts)

\- [How AutoExcel Works]\(#️-how-autoexcel-works)

\- [Data Science Perspective]\(#-data-science-perspective)

\- [AI / Machine Learning Perspective]\(#-ai--machine-learning-perspective)

\- [Validation & Testing]\(#-validation--testing)

\- [Architecture]\(#️-architecture)

\- [Technology Stack]\(#️-technology-stack)

\- [Project Structure]\(#-project-structure)

\- [My Contribution]\(#-my-contribution)

\- [Screenshots]\(#-screenshots)

\- [Running the Project Locally]\(#-running-the-project-locally)

\- [API Overview]\(#-api-overview)

\- [Important Design Decisions]\(#-important-design-decisions)

\- [Engineering Trade-offs]\(#️-engineering-trade-offs)

\- [Future Improvements]\(#-future-improvements)

\- [What I Learned]\(#-what-i-learned)

\- [Connection to My Career Goal]\(#-connection-to-my-career-goal)

\- [Project Status]\(#-project-status)

\- [About Me]\(#-about-me)

\</details>

---

# 🔗 Live Demo**

**\*\*Try it here:\*\*** [https\://autoexcel-aditya.netlify.app/]\(https\://autoexcel-aditya.netlify.app/)

*\*Note: the backend runs on a free hosting tier that sleeps after inactivity. The first request after idle time may take 30-50 seconds to wake up — subsequent requests are fast.\**

\---

**

---



\---

**# 🎯 Project Objective**

The main objective of AutoExcel is to make common **\*\*data-cleaning and preprocessing operations easier to perform through natural-language instructions\*\*** while keeping the process transparent and predictable.

The project combines concepts from:

\- Data Science

\- Data Cleaning

\- Data Preprocessing

\- Python

\- pandas

\- Backend Development

\- REST APIs

\- Database Management

\- Software Testing

\- Natural-Language Processing concepts

\---

**# ⭐ Key Features**

**### 📂 File Support**

Supports:

\- \`.xlsx\`

\- \`.xls\`

\- \`.csv\`

The application automatically handles the input format and generates the appropriate output format.

\---

**### 💬 Natural-Language Cleaning**

Users can describe cleaning operations in simple language.

For example:

\`\`\`text

Remove duplicate rows

\`\`\`

or:

\`\`\`text

Delete repeated records and fill missing values with the average.

\`\`\`

The system identifies the requested operations and converts them into executable cleaning steps.

\---

**### 🔍 Dataset Analysis**

Before cleaning, AutoExcel analyzes the uploaded dataset and provides information such as:

\- Number of rows

\- Number of columns

\- Missing values

\- Duplicate records

\- Column information

\- Dataset structure

This gives the user a quick understanding of the data before applying changes.

\---

**### 📝 Cleaning Plan Review**

One of the most important design decisions in AutoExcel is that the application does **\*\*not blindly modify the uploaded data\*\***.

Instead:

\`\`\`text

User Prompt

     ↓

Operation Detection

     ↓

Validation

     ↓

Cleaning Plan

     ↓

User Review

     ↓

Execution

\`\`\`

The user can see what AutoExcel intends to perform before applying the changes.

This makes the system more transparent and reduces unexpected modifications.

\---

**### ✅ Result Validation**

After cleaning, AutoExcel checks whether the requested operations actually produced the expected result.

For example:

\`\`\`text

Before:

Rows       → 1000

Duplicates → 25

After:

Rows       → 975

Duplicates → 0

\`\`\`

This gives the user evidence that the requested cleaning operation was actually performed.

\---

**### 📊 Before / After Summary**

AutoExcel provides a comparison of the dataset before and after cleaning.

Example:

\| Metric | Before | After |

\|---|---:|---:|

\| Rows | 1000 | 975 |

\| Columns | 12 | 12 |

\| Missing Values | 48 | 0 |

\| Duplicate Rows | 25 | 0 |

\---

**### 🗃️ Cleaning History**

Cleaning operations are stored in a PostgreSQL database.

The history records information such as:

\- File name

\- User prompt

\- Operations performed

\- Status

\- Timestamp

This provides a persistent record of previous cleaning activities.

\---

**### 📑 Excel Output Formatting**

For Excel files, AutoExcel can generate a cleaner output with:

\- Styled headers

\- Adjusted column widths

\- Separate summary information

\- Cleaned dataset

\---

**# 🧹 Supported Data-Cleaning Operations**

AutoExcel supports a range of common data-preprocessing operations.

\| Category | Operations |

\|---|---|

\| **\*\*Duplicates\*\*** | Remove duplicate rows, remove duplicate columns |

\| **\*\*Missing Values\*\*** | Fill with mean, median, mode; remove rows with missing values |

\| **\*\*Text Cleaning\*\*** | Remove extra spaces, standardize text |

\| **\*\*Structure\*\*** | Remove empty rows/columns, standardize column names |

\| **\*\*Columns\*\*** | Remove, rename, split, and merge columns |

\| **\*\*Data Types\*\*** | Convert values to numeric, text, or date |

\| **\*\*Dates\*\*** | Standardize date formats |

\| **\*\*Value Cleaning\*\*** | Remove negative values, replace negative values |

\| **\*\*Row Operations\*\*** | Filter rows based on conditions |

\| **\*\*Sorting\*\*** | Sort ascending or descending |

\| **\*\*Calculated Columns\*\*** | Create columns using safe arithmetic expressions |

\| **\*\*Grouping\*\*** | Group and summarize data |

\| **\*\*Reporting\*\*** | Generate dataset summary information |

\---

**# 💬 Example Prompts**

**### Remove duplicates**

\`\`\`text

Remove duplicate rows

\`\`\`

**### Handle missing values**

\`\`\`text

Fill missing values with mean

\`\`\`

**### Clean text**

\`\`\`text

Remove extra spaces and convert names to title case

\`\`\`

**### Sort data**

\`\`\`text

Sort Salary in descending order

\`\`\`

**### Remove a column**

\`\`\`text

Remove the Notes column

\`\`\`

**### Split a column**

\`\`\`text

Split Full Name into First Name and Last Name

\`\`\`

**### Merge columns**

\`\`\`text

Merge First Name and Last Name into Full Name

\`\`\`

**### Create a calculated column**

\`\`\`text

Create a Total column using Price multiplied by Quantity

\`\`\`

**### Group data**

\`\`\`text

Group by City and calculate the sum of Sales

\`\`\`

\---

**# ⚙️ How AutoExcel Works**

The complete workflow is:

\`\`\`text

                  ┌──────────────────┐

                  │   Upload File    │

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │ Analyze Dataset  │

                  │ rows / columns   │

                  │ missing / dupes  │

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │  User Prompt     │

                  │ Natural Language │

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │ Detect Operations│

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │ Validate Against │

                  │ Actual Dataset   │

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │ Cleaning Plan    │

                  │     Review       │

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │ Execute Cleaning │

                  └────────┬─────────┘

                           ↓

                  ┌──────────────────┐

                  │ Validate Result  │

                  └────────┬─────────┘

                           ↓

             ┌─────────────┴─────────────┐

             ↓                           ↓

      Before / After                Cleaned File

         Summary                    Download

             ↓

      Cleaning History

\`\`\`

\---

**# 🧠 Data Science Perspective**

Although AutoExcel is an application, the core of the project is strongly connected to **\*\*Data Science workflows\*\***.

A typical Data Science pipeline looks like:

\`\`\`text

Raw Data

   ↓

Data Understanding

   ↓

Data Cleaning

   ↓

Data Preprocessing

   ↓

Feature Engineering

   ↓

Model Training

   ↓

Evaluation

\`\`\`

AutoExcel focuses mainly on the **\*\*Data Understanding → Data Cleaning → Data Preprocessing\*\*** part.

The cleaning engine uses **\*\*pandas\*\*** to perform operations directly on DataFrames.

This project helped me work practically with concepts such as:

\- DataFrame manipulation

\- Missing-value handling

\- Duplicate detection

\- Data-type conversion

\- Data validation

\- Text preprocessing

\- Filtering

\- Sorting

\- Aggregation

\- Data transformation

\- Dataset statistics

These are fundamental operations that appear repeatedly in real-world Data Science and Machine Learning projects.

\---

**# 🤖 AI / Machine Learning Perspective**

AutoExcel currently does **\*\*not depend on an external LLM to perform the actual cleaning operations\*\***.

Instead, the current implementation uses a **\*\*deterministic operation-detection approach\*\***.

For example:

\`\`\`text

User:

"Remove duplicate rows and fill missing values with mean."

                ↓

Detected Operations:

[

    "remove_duplicates",

    "fill_missing_mean"

]

                ↓

Validated Plan

                ↓

pandas DataFrame Operations

                ↓

Cleaned Dataset

\`\`\`

**### Why this approach?**

For a data-cleaning application, predictable behavior is important.

A deterministic pipeline provides:

\- Reproducible results

\- Easier debugging

\- Lower complexity

\- No API cost for every cleaning request

\- No dependency on external LLM availability

\- Easier testing

\- More controlled data transformations

This is a deliberate engineering decision rather than simply adding an AI model because the project contains natural-language input.

\---

**# 🧪 Validation & Testing**

Testing was treated as an important part of the project rather than something added at the end.

The project includes an automated **\*\*pytest test suite\*\*** covering areas such as:

\- Operation detection

\- Cleaning logic

\- Validation logic

\- API endpoints

\- Edge cases

\- Error handling

Current test suite:

\`\`\`text

71 automated tests

\`\`\`

The purpose of these tests is to make sure changes to the cleaning engine do not silently break existing functionality.

Run the tests with:

\`\`\`bash

cd backend

pytest -v

\`\`\`

\---

**# 🏗️ Architecture**

AutoExcel follows a simple full-stack architecture.

\`\`\`text

┌─────────────────────────────────────┐

│             Frontend                │

│        HTML + CSS + JavaScript      │

└──────────────────┬──────────────────┘

                   │

                   │ HTTP / REST API

                   ↓

┌─────────────────────────────────────┐

│              FastAPI                │

│             Backend                 │

├─────────────────────────────────────┤

│ File Upload                         │

│ Dataset Analysis                    │

│ Operation Detection                 │

│ Validation                          │

│ Cleaning Engine                     │

│ Result Validation                   │

│ Summary Generation                  │

└───────────────┬─────────────────────┘

                │

        ┌───────┴────────┐

        ↓                ↓

┌───────────────┐  ┌────────────────┐

│    pandas     │  │  PostgreSQL    │

│ Data Processing│  │ Cleaning       │

│               │  │ History        │

└───────────────┘  └────────────────┘

\`\`\`

\---

**# 🛠️ Technology Stack**

**## Backend**

\- **\*\*Python\*\***

\- **\*\*FastAPI\*\***

\- **\*\*pandas\*\***

\- **\*\*SQLAlchemy\*\***

\- **\*\*PostgreSQL\*\***

\- **\*\*openpyxl\*\***

\- **\*\*Uvicorn\*\***

**## Frontend**

\- **\*\*HTML\*\***

\- **\*\*CSS\*\***

\- **\*\*JavaScript\*\***

The frontend intentionally uses vanilla web technologies rather than a large frontend framework because the main learning and engineering focus of this project is the **\*\*data-processing and backend pipeline\*\***.

**## Testing**

\- **\*\*pytest\*\***

\- **\*\*httpx\*\***

\---

**# 📁 Project Structure**

\`\`\`text

AutoExcel/

│

├── backend/

│   │

│   ├── app/

│   │   ├── routes/

│   │   │   ├── ai_clean.py

│   │   │   ├── upload.py

│   │   │   └── clean.py

│   │   │

│   │   ├── database.py

│   │   ├── main.py

│   │   ├── models.py

│   │   └── schemas.py

│   │

│   ├── tests/

│   │   └── ...

│   │

│   └── requirements.txt

│

├── frontend/

│   ├── index.html

│   ├── script.js

│   └── style.css

│

├── docs/

│   ├── PRD.md

│   ├── TRD.md

│   ├── BACKEND_SCHEMA.md

│   ├── AI_SCHEMA.md

│   └── UI_UX_SPEC.md

│

└── README.md

\`\`\`

\---

**# 👨‍💻 My Contribution**

**## Project Ownership & Technical Decision-Making**

AutoExcel was developed using an **\*\*AI-assisted / vibe-coding workflow\*\***, but the project was not treated as a black-box generated application.

I was responsible for defining the problem, deciding the project scope, designing the workflow, evaluating technical trade-offs, testing the application, and directing the implementation.

**### My main contributions include:**

**\*\*1. Problem Definition\*\***

Identified repetitive spreadsheet data cleaning as a practical problem and designed a workflow that allows users to express cleaning requirements in natural language.

**\*\*2. System Architecture\*\***

Designed the overall flow:

\`\`\`text

Upload

→ Analyze

→ Detect

→ Validate

→ Review

→ Execute

→ Validate

→ Download

\`\`\`

**\*\*3. Data Processing Logic\*\***

Worked with the design and implementation of data-cleaning operations using **\*\*Python and pandas\*\***, including missing values, duplicates, filtering, sorting, transformations, and aggregation.

**\*\*4. Validation Design\*\***

Designed the plan-review and result-validation approach so that the system does not simply modify data without showing the user what will happen.

**\*\*5. Backend Development\*\***

Worked with:

\- FastAPI

\- REST APIs

\- Request/response handling

\- File processing

\- pandas DataFrames

\- SQLAlchemy

\- PostgreSQL

**\*\*6. Database Design\*\***

Used PostgreSQL to persist cleaning history and designed the database model around information such as:

\`\`\`text

filename

prompt

operations

status

created_at

\`\`\`

**\*\*7. Testing\*\***

Designed and maintained the testing approach for the cleaning engine, validation logic, and API behavior.

**\*\*8. Debugging\*\***

Worked through issues involving:

\- CORS configuration

\- API/backend integration

\- frontend/backend communication

\- function integration

\- summary generation

\- UI behavior

\- file-format handling

\- CSV and Excel processing

**\*\*9. AI-Assisted Development\*\***

Claude and other AI coding tools were used as development assistants to accelerate implementation, debugging, and code iteration.

However, the project decisions were driven by my understanding of the requirements and by testing the resulting implementation.

This workflow reflects how I currently use AI tools: **\*\*as development accelerators while retaining responsibility for architecture, technical decisions, validation, and the final result.\*\***



**# 📸 Screenshots**

Screenshots of the AutoExcel application and its main features.

**### 1. Upload Interface**

![Upload Interface]\(screenshots/01-upload.png)

**### 2. Cleaning Plan Review**

![Cleaning Plan Review]\(screenshots/02-plan-review\.png)

**### 3. Before / After Summary**

![Before / After Summary]\(screenshots/03-summary.png)

**### 4. Cleaning History**

![Cleaning History]\(screenshots/04-history.png)

**### 5. Generated Excel / CSV Output**

![Generated Excel / CSV Output]\(screenshots/05-excel-output.png)

\---

**# 🚀 Running the Project Locally**

**## 1. Clone the Repository**

\`\`\`bash

git clone https\://github.com/AdityaRunwal/AutoExcel.git

cd AutoExcel

\`\`\`

\---

**## 2. Backend Setup**

\`\`\`bash

cd backend

\`\`\`

Create a virtual environment:

\`\`\`bash

python -m venv venv

\`\`\`

Activate it on Windows:

\`\`\`bash

venv\Scripts\activate

\`\`\`

Install dependencies:

\`\`\`bash

pip install -r requirements.txt

\`\`\`

\---

**## 3. Configure PostgreSQL**

Create a PostgreSQL database for the application.

Example:

\`\`\`text

Database:

autoexcel

\`\`\`

Configure the database connection according to the project's environment configuration.

\---

**## 4. Start the Backend**

\`\`\`bash

uvicorn app.main\:app --reload

\`\`\`

Backend:

\`\`\`text

http\://127.0.0.1:8000

\`\`\`

FastAPI documentation:

\`\`\`text

http\://127.0.0.1:8000/docs

\`\`\`

\---

**## 5. Start the Frontend**

Open another terminal:

\`\`\`bash

cd frontend

\`\`\`

Run:

\`\`\`bash

python -m http.server 3000

\`\`\`

Frontend:

\`\`\`text

http\://127.0.0.1:3000

\`\`\`

\---

**# 🔌 API Overview

The current cleaning workflow uses a two-step plan-and-execute flow:

`/preview-plan` → review the generated cleaning plan → `/ai-clean` → execute the approved cleaning operations

Some of the main backend endpoints include:

| Endpoint | Purpose |
|---|---|
| `/upload` | Upload and analyze a dataset |
| `/preview-plan` | Detect requested operations, validate them against the dataset, and generate a cleaning plan for review |
| `/ai-clean` | Execute the approved cleaning operations and generate the cleaned output |
| `/summary` | Generate cleaning summary information |
| `/history` | Retrieve previous cleaning operations |
| `/db-test` | Test database connectivity |

> **Note:** A `clean.py` route module is present in the project structure, but the supplied README does not establish whether `/clean` is still used by the current frontend workflow. The documented primary cleaning flow is `/preview-plan` followed by `/ai-clean`.

The backend follows a REST-style API architecture for communication between the frontend and data-processing layer.

---

# 🔐 Important Design Decisions**

**## Why pandas?**

pandas is one of the most widely used Python libraries for practical data analysis and preprocessing.

Since AutoExcel focuses on data cleaning, DataFrames provide a natural structure for:

\- filtering

\- transformation

\- aggregation

\- missing-value handling

\- duplicate detection

\- type conversion

\---

**## Why FastAPI?**

FastAPI provides a lightweight and modern way to expose the data-processing functionality through REST APIs.

It also provides automatic API documentation through Swagger UI.

\---

**## Why PostgreSQL?**

PostgreSQL is used to persist cleaning history instead of keeping it only in application memory.

This gives the project experience with:

\- relational databases

\- database schemas

\- ORM-based interaction

\- persistent application data

\---

**## Why a Plan-Review Workflow?**

A cleaning application should not unexpectedly modify user data.

Therefore:

\`\`\`text

Prompt

 ↓

Detected Operations

 ↓

Validation

 ↓

User Review

 ↓

Execution

\`\`\`

This provides a safer and more understandable user experience.

\---

**# ⚖️ Engineering Trade-offs**

A major decision in this project was choosing **\*\*deterministic operation detection instead of relying entirely on an LLM\*\***.

**### LLM-based approach**

Potential advantages:

\- More flexible language understanding

\- Better handling of complex instructions

\- More conversational interaction

Potential disadvantages:

\- Non-deterministic behavior

\- API dependency

\- Additional cost

\- Increased latency

\- More difficult testing

\- Potentially unpredictable transformations

**### Current AutoExcel approach**

The current implementation prioritizes:

\`\`\`text

Predictability

\+

Testability

\+

Reproducibility

\+

Controlled Data Transformations

\`\`\`

This makes the current version better suited to a controlled data-cleaning workflow.

A future version could explore an LLM layer while keeping the actual data transformations deterministic.

\---

**# 🔮 Future Improvements**

Possible future directions include:

\- LLM-powered natural-language understanding

\- More advanced column inference

\- Automatic data-quality scoring

\- Data profiling dashboard

\- More advanced validation rules

\- User authentication

\- Cloud deployment

\- Larger file processing

\- Background processing for large datasets

\- ML-assisted anomaly detection

\- Automatic preprocessing recommendations

\- Integration with machine-learning pipelines

An important future direction is connecting the cleaning workflow more directly with **\*\*Machine Learning preprocessing pipelines\*\***.

For example:

\`\`\`text

Raw Dataset

     ↓

AutoExcel Data Cleaning

     ↓

Data Validation

     ↓

Feature Engineering

     ↓

ML Dataset

     ↓

Machine Learning Model

\`\`\`

\---

**# 📚 What I Learned**

Building AutoExcel gave me practical experience beyond simply writing Python scripts.

**### Data Science**

\- Data cleaning

\- Data preprocessing

\- pandas DataFrames

\- Missing-value handling

\- Data transformation

\- Aggregation

\- Dataset profiling

**### Machine Learning Foundations**

The project strengthened my understanding of why data quality and preprocessing are important before building ML models.

**### Backend Development**

\- FastAPI

\- REST APIs

\- File uploads

\- API validation

\- Backend/frontend communication

**### Databases**

\- PostgreSQL

\- SQLAlchemy

\- Relational data modeling

\- Persistent application history

**### Software Engineering**

\- Project architecture

\- Testing

\- Validation

\- Debugging

\- Error handling

\- Documentation

\- Modular code structure

**### AI-Assisted Development**

The project also gave me practical experience using AI coding assistants as part of a development workflow while maintaining responsibility for:

\- requirements

\- architecture

\- technical decisions

\- testing

\- debugging

\- validation

\- final implementation

\---

**# 🎓 Connection to My Career Goal**

My primary career goal is to work in **\*\*AI/ML and Data Science\*\***.

AutoExcel is intentionally aligned with that direction.

Rather than building a generic CRUD application, I wanted to build something around a real **\*\*data-processing problem\*\***.

The project demonstrates my interest in:

\`\`\`text

Python

   ↓

Data Processing

   ↓

Data Cleaning

   ↓

Data Preprocessing

   ↓

Machine Learning Foundations

   ↓

AI/ML Applications

\`\`\`

It represents the type of practical engineering work I want to continue building toward **\*\*AI/ML Engineer and Data Science roles\*\***.

\---

**# 📌 Project Status**

**\*\*Current Status:\*\*** Functional student project

The current version focuses on:

\- File processing

\- Data cleaning

\- Natural-language operation detection

\- Validation

\- Result summaries

\- Database history

\- Automated testing

The project is designed as a practical foundation that can later evolve toward more advanced AI/ML-powered data-processing capabilities.

\---

**# 👨‍💻 About Me**

**\*\*Aditya Runwal\*\***

AI & Data Science Student  

Aspiring AI/ML Engineer

Interested in:

\- Machine Learning

\- Data Science

\- Deep Learning

\- Computer Vision

\- Generative AI

\- Large Language Models

\- Data Structures & Algorithms

**### Connect with me**

**\*\*GitHub:\*\***  

https\://github.com/AdityaRunwal

**\*\*LinkedIn:\*\***  

https\://linkedin.com/in/aditya-runwal-b9a85b322

\---

**# ⭐ If You Found This Project Interesting**

Feel free to explore the repository, experiment with the application, and provide feedback.

\---

**## 📄 License

This repository does not currently include a formal open-source license. It is intended as a learning and portfolio project.
