"""PASSO 3: dar personalidade ao bot com uma instrução de sistema.

A "system_instruction" vale para a conversa inteira e não aparece como
mensagem do usuário. É assim que você transforma um chatbot genérico
em um especialista (Tutor SENAI, Assistente Cisco, etc.).

Rode com:  python exemplos/03_personalidade.py
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

PERSONALIDADE = """
Você é um instrutor técnico de redes do SENAI.
Especialidades: Redes Cisco, Python, Linux.
Explique de forma simples, em português do Brasil, com exemplos práticos.
"""

chat = client.chats.create(
    model=MODELO,
    config=types.GenerateContentConfig(system_instruction=PERSONALIDADE),
)

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
