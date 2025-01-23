from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    token = None

    def on_start(self):
        # Initialize login and set token only once per user
        cookies = login("test123", "test123")
        self.token = cookies.get("token")
        self.headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Sec-GPC": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Cookies": f"token={self.token}",
        }

    @task
    def fetch_cart(self):
        # Perform the GET request to the /cart endpoint
        with self.client.get(
            "/cart",
            headers={
                **self.headers,
                "Accept": "application/json",
                "Referer": f"{self.host}/product/1",
                "Upgrade-Insecure-Requests": "1",
            },
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

if _name_ == "_main_":
    run_single_user(AddToCart)