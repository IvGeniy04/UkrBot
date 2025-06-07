# hugchat.py — клієнт для HuggingChat API

import requests
import json
from typing import Dict, List, Optional
import logging
import sys

# Увімкнути детальне логування
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("HugChatBot")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ChatBot:
    def __init__(self, cookie_path: str):
        logger.debug(f"[INIT] Ініціалізація бота. Шлях до cookie: {cookie_path}")
        self.cookie_path = cookie_path
        self.cookies = self.load_cookies()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Referer": "https://huggingface.co/chat/", 
            "Content-Type": "application/json"
        }
        self.conversation_id = None
        logger.info("[INIT] Бот успішно створений")

    def load_cookies(self) -> dict:
        """
        Завантажує cookies із файлу JSON або TXT.
        Якщо файл у форматі Netscape — конвертуємо в словник.
        """
        try:
            logger.debug(f"[COOKIES] Спроба завантаження cookie-файлу: {self.cookie_path}")
            with open(self.cookie_path, "r", encoding="utf-8") as f:
                data = f.read().strip()
            logger.debug(f"[COOKIES] Вміст файлу: {data[:200]}...")

            # Спробуємо завантажити як JSON (Cookie Editor формат)
            try:
                cookies_json = json.loads(data)
                if isinstance(cookies_json, list):
                    cookie_dict = {}
                    for cookie in cookies_json:
                        name = cookie.get("name")
                        value = cookie.get("value")
                        if name and value:
                            cookie_dict[name] = value
                    logger.debug(f"[COOKIES] Використовую cookie (JSON): {cookie_dict.keys()}")
                    return cookie_dict
                else:
                    raise ValueError("[COOKIES] JSON не є масивом об'єктів")
            except json.JSONDecodeError as e:
                logger.warning(f"[COOKIES] Файл не є коректним JSON: {e}. Спроба читання як простий текст.")

            # Якщо не JSON → спробуємо прочитати як name=value
            lines = data.splitlines()
            cookie_dict = {}
            for line in lines:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    cookie_dict[key] = value
            logger.debug(f"[COOKIES] Використовую cookie (TXT): {cookie_dict.keys()}")
            return cookie_dict

        except Exception as e:
            logger.error(f"[COOKIES] Не вдалося завантажити cookie: {e}")
            raise FileNotFoundError(f"Не можу знайти або прочитати файл cookie: {self.cookie_path}. Помилка: {e}")

    def query(self, prompt: str) -> str:
        """
        Відправляє запит до HuggingChat через POST-запит
        """

        logger.debug(f"[QUERY] Обробляється запит: {prompt}")

        url = "https://huggingface.co/chat/" 
        payload = {
            "inputs": prompt,
            "parameters": {"temperature": 0.8},
            "options": {"use_cache": False, "is_retry": False, "use_stream": True}
        }

        logger.debug(f"[REQUEST] Надсилається POST-запит на {url}")
        logger.debug(f"[REQUEST] Payload: {payload}")
        logger.debug(f"[REQUEST] Headers: {self.headers}")
        logger.debug(f"[REQUEST] Cookies: {self.cookies}")

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                cookies=self.cookies,
                timeout=30
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"[REQUEST] Помилка при надсиланні запиту: {e}")
            return "[Помилка] Не вдалося встановити з'єднання"

        logger.debug(f"[RESPONSE] Отримано відповідь. Статус: {response.status_code}")
        logger.debug(f"[RESPONSE] Текст відповіді (перші 200 символів): {response.text[:200]}...")

        if response.status_code == 200:
            try:
                result = response.json()
                generated_text = result.get("generated_text", "[Помилка] Пуста відповідь")
                logger.info(f"[RESPONSE] Згенеровано текст: {generated_text[:100]}...")
                return generated_text
            except json.JSONDecodeError as e:
                logger.error(f"[RESPONSE] Помилка парсингу JSON: {e}. Відповідь: {response.text[:200]}...")
                return "[Помилка] Не можу розпізнати відповідь від сервера"
        else:
            logger.error(f"[RESPONSE] Невдалий запит. Код: {response.status_code}, Текст: {response.text[:200]}...")
            return f"[Помилка] HTTP {response.status_code}: {response.text[:100]}..."
