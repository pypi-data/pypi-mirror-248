import requests
import json

class BoxCordClient:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/API/V10"
    def _request(self, method, endpoint, data=None):
        headers = {
            "Authorization": f"Bot {self.token}"
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, json=data)
        if response.status_code // 100 != 2:
            print(f"Error: {response.status_code} - {response.text}")
        return response.json()
    def send_message(self, channel_id, content):
        data = {
            "content": content
        }
        endpoint = f"/channels/{channel_id}/messages"
        self._request("POST", endpoint, data)