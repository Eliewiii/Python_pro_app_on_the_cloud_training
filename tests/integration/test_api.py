from fastapi.testclient import TestClient

from app.main import app
from core import __version__

client = TestClient(app)


def test_health_check():
    """Verify the API is alive."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "version": f"{__version__}"}


def test_process_file_success(tmp_path):
    """Verify the API correctly processes a valid file."""
    # Create a temporary file for the test
    test_file = tmp_path / "numbers.txt"
    test_file.write_text("10\n20\n30")

    # Send the path to the API
    response = client.post("/process", json={"file_path": str(test_file)})

    assert response.status_code == 200
    assert response.json()["result"] == 60


def test_process_file_not_found():
    """Verify the API returns 404 for a missing file."""
    response = client.post("/process", json={"file_path": "non_existent_file.txt"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
