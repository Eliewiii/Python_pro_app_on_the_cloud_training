import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core import FileProcessor, __version__

# 1. Initialize the App
app = FastAPI(title="Algorithm R&D API")

"""
Start the server : uvicorn app.main:app --reload ot --workers 4
Stop the server : Ctrl + C in the terminal
Request example : curl -X POST "http://127.0.0.1:8000/process" \
                       -H "Content-Type: application/json" \
                       -d '{"file_path": "data/test_numbers.txt"}' or -d @path_to_json.json
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_debug.log"),
        logging.StreamHandler(),  # Also prints to your VS Code terminal
    ],
)
logger = logging.getLogger(__name__)


class FileProcessorRequest(BaseModel):
    file_path: str
    ignore_invalid: bool = True


@app.post("/process")
async def sum_file(request: FileProcessorRequest):

    target_path = Path(request.file_path)

    try:
        with FileProcessor.session():
            logger.info(f"Processing started for: {target_path}")
            result = FileProcessor.sum_file(
                file_path=target_path, ignore_invalid=request.ignore_invalid
            )
            return {"status": "success", "result": result}

    except FileNotFoundError as e:
        # 4. Map internal errors to HTTP errors
        raise HTTPException(status_code=404, detail="The specified file was not found.") from e
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"IO error: {str(e)}") from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}") from e
    except Exception as e:
        # 5. Catch-all for unexpected R&D bugs
        raise HTTPException(status_code=500, detail="Internal server error.") from e


@app.get("/health")
async def health_check():
    return {"status": "online", "version": __version__}
