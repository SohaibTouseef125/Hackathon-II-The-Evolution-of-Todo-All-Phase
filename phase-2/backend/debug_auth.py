from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/test-login")
def test_login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {
        "username": form_data.username,
        "password": form_data.password,
        "scopes": form_data.scopes,
        "grant_type": form_data.grant_type
    }

# Test the endpoint
if __name__ == "__main__":
    client = TestClient(app)

    # Test with form data (this is how the test client sends data)
    response = client.post("/test-login", data={
        "username": "test@example.com",
        "password": "securepassword"
    })

    print("Response Status:", response.status_code)
    print("Response Body:", response.json())