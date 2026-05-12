import logging
from typing import List

from fastapi import FastAPI

from core.processor import FileProcessor

# 1. Initialize the App
app = FastAPI(title="Algorithm R&D API")  # TODO change name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_debug.log"),
        logging.StreamHandler(),  # Also prints to your VS Code terminal
    ],
)
logger = logging.getLogger(__name__)


@app.post("/simulate")  # TODO to adjust
def run_sim(data: List[str]):
    with FileProcessor.session():
        return [FileProcessor.process_data(d) for d in data]
