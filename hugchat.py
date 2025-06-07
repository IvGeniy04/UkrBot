# hugchat.py — клієнт для HuggingChat API

import requests
import json
from typing import Dict, List, Optional


class ChatBot:
    def __init__(self, cookie_path: str):
        self.cookie_path = cookie_path
        self.cookies = self.load_cookies()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://huggingface.co/chat/", 
            "Content-Type": "application/json",
        }
        self.conversation_id = None

    def load_cookies(self) -> dict:
        """
        Завантажує cookies із файлу JSON або TXT.
        Якщо файл у форматі Netscape — конвертуємо в словник.
        """
        try:
            # Спробуємо завантажити як JSON (наприклад, з Cookie Editor)
            with open(self.cookie_path, "r", encoding="utf-8") as f:
                data = f.read().strip()

            # Якщо це JSON масив із об'єктами
            try:
                cookies_json = json.loads(data)
                cookie_dict = {c["name"]: c["value"] for c in cookies_json}
                return cookie_dict
            except json.JSONDecodeError:
                # Якщо не JSON, припустимо простий формат name=value
                lines = data.splitlines()
                cookie_dict = {}
                for line in lines:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        cookie_dict[key] = value
                return cookie_dict

        except Exception as e:
            raise FileNotFoundError(f"Не можу знайти або прочитати файл cookie: {self.cookie_path}. Помилка: {e}")

    def query(self, prompt: str) -> str:
        """
        Відправляє запит до HuggingChat через POST-запит
        """

        url = "https://huggingface.co/chat/" 
        payload = {
            "inputs": prompt,
            "parameters": {"temperature": 0.8},
            "options": {"use_cache": False, "is_retry": False, "use_stream": True}
        }

        print(f"[DEBUG] Надсилаємо запит до HuggingChat...")  # 🔍 Додано лог
        response = requests.post(
            url,
            json=payload,
            headers=self.headers,
            cookies=self.cookies,
            timeout=30
        )

        print(f"[DEBUG] Відповідь статус: {response.status_code}")  # 🔍 Лог статусу
        print(f"[DEBUG] Відповідь текст: {response.text[:200]}...")  # 🔍 Перші 200 символів

        if response.status_code == 200:
            try:
                return response.json().get("generated_text", "Не зрозумів запиту")
            except json.JSONDecodeError:
                return "Помилка парсингу відповіді"
        else:
            return f"[Помилка] Код: {response.status_code}, Текст: {response.text[:100]}"