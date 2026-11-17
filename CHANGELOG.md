# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). O projeto ainda não tem versões publicadas.

## [Não lançado]

### Adicionado

- Chat no terminal e interface web (Streamlit) com resposta em streaming e memória de sessão.
- Prompt de sistema em `prompts/senai_redes.txt`.
- Exemplos progressivos em `exemplos/`.
- Testes da camada de configuração.
- Capturas de tela reais do chat no terminal em `assets/screenshots/`.
- Documentação: README, arquitetura, segurança e tutorial.
- Mensagens de erro de configuração que indicam a causa provável (`.env` ausente, `.env.txt`, chave colada no `.env.example`, variável com nome errado).

### Corrigido

- `Cannot send a request, as the client has been closed`: o cliente da API era uma variável local de `create_chat()` e a conexão era fechada ao fim da função. O cliente agora é mantido no nível do módulo em `src/chatbot.py`.
- Anotações de tipo com `|` exigem Python 3.10; a documentação indicava 3.9. O pré-requisito foi corrigido para 3.10 e o módulo passou a usar `from __future__ import annotations`.

### Alterado

- Uso do SDK `google-genai` e do modelo `gemini-3.5-flash` no lugar do SDK `google-generativeai` e do modelo `gemini-1.5-flash`, que aparecem em tutoriais antigos e saíram de linha.
