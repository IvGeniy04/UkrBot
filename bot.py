# bot.py — UkrBot

import discord
from hugchat import ChatBot
import os
from config import PERSONALITY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

chatbot = ChatBot(cookie_path="cookies.json")

@client.event
async def on_ready():
    print(f'{client.user} працює!')

@client.event
async def on_message(message):
    print(f"[LOG] Отримано повідомлення від {message.author}: {message.content}")  # 🔍 Лог отриманого повідомлення

    if message.author == client.user:
        return

    if client.user in message.mentions:
        query = message.content.replace(f"<@{client.user.id}>", "").strip()
        full_prompt = f"{PERSONALITY}\n\nЗапит: {query}"

        print(f"[LOG] Обробляємо запит: {full_prompt}")  # 🔍 Лог запиту

        try:
            response = chatbot.query(full_prompt)
            print(f"[LOG] Отримали відповідь: {response}")  # 🔍 Лог відповіді
            await message.channel.send(f"{message.author.mention} {response}")
        except Exception as e:
            print(f"[ERROR] Помилка при обробці запиту: {e}")
            await message.channel.send("На жаль, зараз не можу відповісти.")

client.run(os.getenv("DISCORD_TOKEN"))