"""Funções que criam o cliente e a conversa com o Gemini."""

from __future__ import annotations

from google import genai
from google.genai import types

from .config import MODEL, get_api_key, load_prompt

# O cliente PRECISA continuar vivo enquanto o chat for usado.
# Se ele fosse só uma variável local de uma função, o Python o descartaria ao
# fim da função e a biblioteca fecharia a conexão ("client has been closed").
# Por isso ele fica guardado aqui, no nível do módulo.
_client: genai.Client | None = None


def create_client() -> genai.Client:
    """Devolve o cliente da Gemini API (criado uma única vez)."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=get_api_key())
    return _client


def create_chat(system_prompt: str | None = None):
    """Cria uma conversa com memória e personalidade.

    O objeto devolvido guarda o histórico sozinho: cada send_message()
    já envia as mensagens anteriores junto.
    """
    client = create_client()
    instruction = system_prompt if system_prompt is not None else load_prompt()
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=instruction),
    )
