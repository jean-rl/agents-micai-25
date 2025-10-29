import httpx
from mcp.server.fastmcp import FastMCP
from mcp import types
import keyring
import json
from typing import Any, Dict, Optional

mcp = FastMCP("proj-mcp")

API_BASE_URL = "https://axum-todo-list-giz6.shuttle.app"

# --- Token Storage Management ---
class TokenStore:
    SERVICE_NAME = "TradingBotClient"

    def __init__(self):
        self.username = None
        self.token = None
        self._load_token()

    def _load_token(self):
        """Load token from OS keychain."""
        try:
            credentials = keyring.get_password(self.SERVICE_NAME, "credentials")
            if credentials:
                data = json.loads(credentials)
                self.username = data.get("username")
                self.token = data.get("token")
                print(f"🔑 Loaded token for user '{self.username}' from secure keychain.")
        except Exception as e:
            print(f"⚠️ Failed to load token from keychain: {e}")

    def _save_token(self):
        """Save token to OS keychain."""
        try:
            data = json.dumps({
                "username": self.username,
                "token": self.token
            })
            keyring.set_password(self.SERVICE_NAME, "credentials", data)
            print(f"✅ Token for '{self.username}' securely stored in keychain.")
        except Exception as e:
            print(f"⚠️ Failed to save token to keychain: {e}")

    def set_token(self, username, token):
        self.username = username
        self.token = token
        self._save_token()

    def get_token(self):
        return self.token
    
# --- Helper to fetch API data ---
def _api_request(method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handles making API requests and basic error handling (using httpx)."""
    url = f"{API_BASE_URL}/{endpoint}"

    try:
        with httpx.Client(timeout=10.0) as client:  # You can adjust timeout
            if method.upper() == 'POST':
                response = client.post(url, json=data)
            elif method.upper() == 'GET':
                response = client.get(url, params=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()  # Raises for 4xx and 5xx responses

        if response.content:
            return response.json()
        return {"message": "Success (No content)", "status_code": response.status_code}

    except httpx.HTTPStatusError as errh:
        try:
            error_data = errh.response.json()
            return {"error": f"HTTP Error: {error_data.get('message', 'Unknown API Error')}"}
        except json.JSONDecodeError:
            return {"error": f"HTTP Error: {errh.response.status_code} - {errh.response.text}"}
    except httpx.ConnectError:
        return {"error": f"Connection Error: Could not connect to API at {API_BASE_URL}. Is the server running?"}
    except httpx.ReadTimeout:
        return {"error": "Timeout Error: API took too long to respond."}
    except httpx.RequestError as err:
        return {"error": f"An unexpected request error occurred: {err}"}
    except ValueError as errv:
        return {"error": str(errv)}
    
token_store = TokenStore()