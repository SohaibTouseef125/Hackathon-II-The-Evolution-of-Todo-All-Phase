import requests
import json
import uuid

def test_chat_api():
    # Create a fake user ID for testing
    user_id = str(uuid.uuid4())

    # Example API endpoint - you'll need to provide a valid JWT token
    url = f"http://localhost:8000/api/{user_id}/chat"

    # Sample request payload
    payload = {
        "message": "Hello, can you help me add a task?",
        "conversation_id": str(uuid.uuid4())
    }

    # Headers - you'll need a valid JWT token for a real test
    headers = {
        "Content-Type": "application/json",
        # "Authorization": "Bearer YOUR_VALID_JWT_TOKEN_HERE"  # Uncomment and add real token for full test
    }

    try:
        print(f"Testing chat API endpoint: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")

        # This will likely fail due to missing auth, but will test if the endpoint exists
        response = requests.post(url, json=payload, headers=headers)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        return response.status_code

    except requests.exceptions.ConnectionError:
        print("Connection error: Could not connect to the server")
        print("Make sure the backend server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"Error testing chat API: {str(e)}")
        return None

if __name__ == "__main__":
    test_chat_api()