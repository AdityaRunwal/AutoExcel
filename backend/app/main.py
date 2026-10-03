from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.ai_clean import router as ai_clean_router
from app.routes.clean import router as clean_router
from app.routes.upload import router as upload_router
from app.database import engine

from app.database import Base, engine
from app.models import CleaningHistory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(clean_router)
app.include_router(ai_clean_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "AutoExcel API is running"}


@app.get("/db-test")
def database_test():
    try:
        with engine.connect() as connection:
            return {"message": "PostgreSQL connection successful"}
    except Exception as e:
        return {"error": str(e)}