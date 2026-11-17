"""Configurações do projeto: chave da API, modelo e leitura do prompt."""

import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

# Pasta raiz do projeto (a que contém app_web.py, .env, etc.)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
PLACEHOLDER = "sua_chave_aqui"

# Lê o arquivo .env e coloca as variáveis no ambiente.
# "utf-8-sig" aceita arquivos salvos com BOM (comum no Bloco de Notas antigo).
load_dotenv(ENV_PATH, encoding="utf-8-sig")

APP_TITLE = "SENAI Networking Assistant"
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
PROMPTS_DIR = BASE_DIR / "prompts"


def _diagnostico() -> str:
    """Descobre por que a chave não foi encontrada e devolve uma dica."""
    if not ENV_PATH.exists():
        # Caso 1: a chave foi colada em outro arquivo
        exemplo = BASE_DIR / ".env.example"
        if exemplo.exists():
            valor = (
                dotenv_values(exemplo, encoding="utf-8-sig").get("GEMINI_API_KEY") or ""
            ).strip()
            if valor and valor != PLACEHOLDER:
                return (
                    "Você colocou a chave dentro do .env.example. Ele é só um modelo: "
                    "crie uma cópia chamada .env (sem '.example') com essa linha."
                )
        # Caso 2: o Windows escondeu a extensão e salvou como .env.txt
        if (BASE_DIR / ".env.txt").exists():
            return "Existe um arquivo '.env.txt'. Renomeie para '.env' (sem o .txt)."
        return f"O arquivo .env não existe. Ele deveria estar em: {ENV_PATH}"

    # O .env existe, então o problema está no conteúdo
    valores = dotenv_values(ENV_PATH, encoding="utf-8-sig")
    if "GEMINI_API_KEY" not in valores:
        nomes = ", ".join(valores.keys()) or "nenhuma"
        return (
            f"O .env existe ({ENV_PATH}), mas não tem a variável GEMINI_API_KEY. "
            f"Variáveis encontradas: {nomes}. Confira a grafia e se salvou o arquivo."
        )
    return (
        f"O .env existe ({ENV_PATH}), mas GEMINI_API_KEY está vazia ou ainda é "
        f"'{PLACEHOLDER}'. Cole a chave real depois do sinal de igual e salve."
    )


def get_api_key() -> str:
    """Devolve a chave da API ou explica como configurá-la."""
    key = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    if key and key != PLACEHOLDER:
        return key
    raise RuntimeError(
        "Chave da API não encontrada.\n"
        f"  Diagnóstico: {_diagnostico()}\n"
        "  Formato esperado, numa única linha: GEMINI_API_KEY=sua_chave "
        "(sem aspas e sem espaços).\n"
        "  Gere uma chave em https://aistudio.google.com/apikey"
    )


def load_prompt(name: str = "senai_redes.txt") -> str:
    """Lê um prompt de sistema da pasta prompts/."""
    return (PROMPTS_DIR / name).read_text(encoding="utf-8").strip()
