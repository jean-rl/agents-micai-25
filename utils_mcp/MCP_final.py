import httpx
from mcp.server.fastmcp import FastMCP
import keyring
import json
from typing import Any, Dict, Optional, List

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

# --- Tutorial Start Point ---
@mcp.tool()
def register(username: str) -> Dict[str, Any]:
    """
    Registers a new user account with the trading API and saves the token
    to 'trading_token.json' for persistence.

    :param username: The desired username for registration.
    :return: A dictionary with the token and initial balance, or an error.
    """
    data = {"username": username}
    response = _api_request("POST", "register", data)

    if "token" in response:
        # The set_token method now handles both in-memory and file saving
        token_store.set_token(username, response['token'])
        print(f"✅ Successfully registered user '{username}' and saved token to file.")

    return response


@mcp.tool()
def consult_account() -> Dict[str, Any]:
    """
    Consults the user's account information, including balance and positions.
    Requires a token to be registered.
    """
    token = token_store.get_token()
    if not token:
        return {"error": "No token found. Please register or check your 'trading_token.json' file."}

    data = {"token": token}
    response = _api_request("POST", "account", data)
    return response

@mcp.tool()
def consult_market() -> Dict[str, Any]:
    """
    Consults the current market data, including stock prices and news.
    """
    response = _api_request("GET", "market")
    return response


@mcp.tool()
def consult_market_history() -> Dict[str, Any]:
    """
    Retrieves the complete historical price data and news history
    for all 5 stocks from the first round up to the current round.

    The response is split into a 'prices' list (round, stock prices)
    and a 'news_history' list (round, news string).
    """
    response = _api_request("GET", "market/history")
    return response

@mcp.tool()
def buy(stock_symbol: str, quantity: int) -> Dict[str, Any]:
    """
    Buys a specified quantity of a stock.
    """
    token = token_store.get_token()
    if not token:
        return {"error": "No token found. Please register or check your 'trading_token.json' file."}

    data = {
        "token": token,
        "stock_symbol": stock_symbol.upper(),
        "quantity": quantity
    }
    response = _api_request("POST", "buy", data)
    return response

@mcp.tool()
def sell(stock_symbol: str, quantity: int) -> Dict[str, Any]:
    """
    Sells a specified quantity of a stock.
    """
    token = token_store.get_token()
    if not token:
        return {"error": "No token found. Please register or check your 'trading_token.json' file."}

    data = {
        "token": token,
        "stock_symbol": stock_symbol.upper(),
        "quantity": quantity
    }
    response = _api_request("POST", "sell", data)
    return response

@mcp.tool()
def optimize_profit_strategy():
    """
    Executes the full trading strategy:
    1. Consults account balance and positions.
    2. Consults market history.
    3. Makes basic predictions for all stocks.
    4. Executes a simplified profit optimization strategy (Sell winners, Buy predicted winners).
    """
    pass

if __name__ == "__main__":
    mcp.run(transport="stdio")