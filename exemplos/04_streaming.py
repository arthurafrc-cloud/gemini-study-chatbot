"""PASSO 4: resposta em streaming (o texto aparece aos poucos, como no ChatGPT).

Rode com:  python exemplos/04_streaming.py
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

chat = client.chats.create(
    model=MODELO,
    config=types.GenerateContentConfig(
        system_instruction="Você é um instrutor de redes. Seja claro e objetivo."
    ),
)

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "sair":
        break
    if not pergunta:
        continue

    print("\nBot: ", end="", flush=True)
    for pedaco in chat.send_message_stream(pergunta):
        print(pedaco.text or "", end="", flush=True)
    print("\n")
