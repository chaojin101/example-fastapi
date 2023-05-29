from main import app
from fastapi.testclient import TestClient

if __name__ == "__main__":
    client = TestClient(app)
    response = client.put("/posts/2")
    print(response.text)
