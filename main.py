"""app service"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import index
from app.router import task

from app.model.database_operator import DatabaseOperator

app = FastAPI(title="LifeInTrust", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router)
app.include_router(task.router)


def start_app():
    """launch app"""
    uvicorn.run(app=app)


if __name__ == "__main__":
    DatabaseOperator().create_database()
    start_app()
