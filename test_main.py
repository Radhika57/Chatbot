from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_pdf():
    with open("dummy.pdf", "rb") as file:
        response = client.post("/upload_pdf/", files={"file": ("dummy.pdf", file, "application/pdf")})
    assert response.status_code == 200
    assert "text" in response.json()

def test_query_pdf():
    text = "This is a sample text extracted from the PDF."
    query = "What is this text about?"
    response = client.post("/query_pdf/", json={"query": query, "text": text})
    assert response.status_code == 200
    assert "response" in response.json()
