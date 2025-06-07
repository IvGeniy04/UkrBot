import discord
from hugchat import ChatBot
import os
from config import PERSONALITY

# Ввімкнути доступ до тексту повідомлень
intents = discord.Intents.default()
intents.message_content = True  # 🔍 Обов’язковий рядок для нових версій
client = discord.Client(intents=intents)

# Підключення до HuggingChat
try:
    chatbot = ChatBot(cookie_path="cookies.json")
except Exception as e:
    print(f"[ERROR] Не вдалося створити ChatBot: {e}")

@client.event
async def on_ready():
    print(f'{client.user} працює!')

@client.event
async def on_message(message):
    print(f"[LOG] Отримано повідомлення від {message.author}: {message.content}")  # 🔍 Лог кожного повідомлення
    
    if message.author == client.user:
        return

    if client.user in message.mentions:
        query = message.content.replace(f"<@{client.user.id}>", "").strip()
        full_prompt = f"{PERSONALITY}\n\nЗапит: {query}"

        print(f"[DEBUG] Обробляється запит: {full_prompt}")  # 🔍 Лог запиту

        try:
            response = chatbot.query(full_prompt)
            print(f"[DEBUG] Отримана відповідь: {response[:100]}...")  # 🔍 Перші 100 символів
            await message.channel.send(f"{message.author.mention} {response}")
        except Exception as e:
            print(f"[ERROR] Помилка при генерації відповіді: {e}")
            await message.channel.send("На жаль, зараз не можу відповісти.")

client.run(os.getenv("DISCORD_TOKEN"))
