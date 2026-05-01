from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

from contextlib import asynccontextmanager
from app.infrastructure.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## SGK Crawler API
    A powerful API for crawling and managing Vietnamese textbook images.
    
    ### Features
    * **Crawl Books**: Initiate background crawling of textbooks from source URLs.
    * **Manage Books**: Retrieve information about crawled books and their pages.
    * **Health Monitoring**: Check the status of the API and database.
    """,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "Antigravity Dev Team",
        "url": "https://github.com/baokha04/crawler-sgk",
    },
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

def dev():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)

if __name__ == "__main__":
    dev()
