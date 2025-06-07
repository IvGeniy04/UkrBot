# hugchat.py — клієнт для HuggingChat API

import requests
from typing import Optional

class ChatBot:
    def __init__(self, cookie_path: str):
        self.cookies = self.load_cookies(cookie_path)
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://huggingface.co/chat/", 
        }
        self.conversation_id = None

    def load_cookies(self, path: str) -> dict:
        with open(path, "r") as f:
            lines = f.readlines()
        cookies = {}
        for line in lines:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                cookies[key] = value
        return cookies

    def query(self, prompt: str) -> str:
        url = "https://huggingface.co/chat/" 
        payload = {
            "inputs": prompt,
            "parameters": {"temperature": 0.8},
            "options": {"use_cache": False}
        }

        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            cookies=self.cookies
        )

        if response.status_code == 200:
            return response.json().get("generated_text", "Не зрозумів запиту")
        else:
            return "На жаль, зараз не можу відповісти"