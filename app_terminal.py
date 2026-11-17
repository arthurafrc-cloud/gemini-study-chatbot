"""Chatbot no terminal (versão organizada, usando a pasta src/).

Rode com:  python app_terminal.py
"""

from src.chatbot import create_chat
from src.config import APP_TITLE, MODEL


def main() -> None:
    try:
        chat = create_chat()
    except RuntimeError as erro:
        print(f"Erro de configuração: {erro}")
        return

    print(f"=== {APP_TITLE} (modelo: {MODEL}) ===")
    print('Digite sua pergunta. Digite "sair" para encerrar.\n')

    while True:
        pergunta = input("Você: ").strip()

        if pergunta.lower() == "sair":
            print("Até a próxima!")
            break
        if not pergunta:
            continue

        print("\nBot: ", end="", flush=True)
        try:
            for pedaco in chat.send_message_stream(pergunta):
                print(pedaco.text or "", end="", flush=True)
        except Exception as erro:  # rede fora, limite de uso, chave inválida...
            print(f"\n[Erro ao falar com a API: {erro}]")
        print("\n")


if __name__ == "__main__":
    main()
