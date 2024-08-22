from fastapi import FastAPI, Depends, Header, HTTPException
from database import engine, Base
from routes import grant
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(grant.router)

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting the FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
