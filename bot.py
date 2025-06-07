# bot.py — UkrBot - Розумний AI-учасник чату

import discord
from hugchat import ChatBot
import os
import time

# Завантажуємо конфігурацію
from config import PERSONALITY

# Токен бота з Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Ініціалізуємо AI-чатбота
chatbot = ChatBot(cookie_path="cookies.json")

# Пам'ять користувачів
user_context = {}

# Налаштування дискорд клієнта
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Подія: коли бот запущений
@client.event
async def on_ready():
    print(f'{client.user} працює!')

# Подія: обробка повідомлень
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Якщо бота згадано
    if client.user in message.mentions:
        user = message.author.name
        query = message.content.replace(f"<@{client.user.id}>", "").strip()

        # Додаємо контекст розмови
        user_context[user] = query

        # Формуємо запит з особистістю
        full_prompt = f"{PERSONALITY}\n\n{query}"

        try:
            response = chatbot.query(full_prompt)
            await message.channel.send(f"{message.author.mention} {response}")
        except Exception as e:
            await message.channel.send("На жаль, зараз не можу відповісти.")

    # Випадкове втручання (10% шанс)
    if random.random() < 0.1:
        if any(word in message.content.lower() for word in ["україна", "війна", "любов", "життя", "мем"]):
            response = chatbot.query("Що ти думаєш про це?")
            await message.channel.send(response)

# Запуск бота
client.run(DISCORD_TOKEN)