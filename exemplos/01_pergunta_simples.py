"""PASSO 1: uma única pergunta, uma única resposta (sem memória).

Rode com:  python exemplos/01_pergunta_simples.py
"""

import os

from dotenv import load_dotenv
from google import genai

load_dotenv()  # lê o arquivo .env

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

resposta = client.models.generate_content(
    model=MODELO,
    contents="Explique o que é DHCP em 3 frases simples.",
)

print(resposta.text)
