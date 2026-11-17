"""PASSO 2: conversa em loop COM memória.

Teste: diga "Meu nome é Arthur" e depois pergunte "Qual é o meu nome?".
Digite "sair" para encerrar.

Rode com:  python exemplos/02_chat_com_memoria.py
"""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# O objeto "chat" guarda o histórico da conversa automaticamente
chat = client.chats.create(model=MODELO)

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "sair":
        break
    if not pergunta:
        continue

    resposta = chat.send_message(pergunta)

    print()
    print("Bot:", resposta.text)
    print()
