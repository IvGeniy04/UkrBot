import discord
from hugchat import ChatBot
import os
from config import PERSONALITY

# Увімкни доступ до тексту повідомлень
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Ініціалізація AI-бота
try:
    chatbot = ChatBot(cookie_path="cookies.json")
except Exception as e:
    print(f"[ERROR] Не вдалося створити ChatBot: {e}")

@client.event
async def on_ready():
    print(f'{client.user} працює!')

@client.event
async def on_message(message):
    print(f"[LOG] Отримано повідомлення від {message.author}: {message.content}")
    
    if message.author == client.user:
        return

    if client.user in message.mentions:
        query = message.content.replace(f"<@{client.user.id}>", "").strip()
        full_prompt = f"{PERSONALITY}\n\nЗапит: {query}"

        try:
            response = chatbot.query(full_prompt)
            print(f"[LOG] Отримана відповідь: {response[:200]}...")

            await message.channel.send(f"{message.author.mention} {response}")
        except Exception as e:
            print(f"[ERROR] Помилка при обробці запиту: {e}")
            await message.channel.send("На жаль, зараз не можу відповісти.")

client.run(os.getenv("DISCORD_TOKEN"))
