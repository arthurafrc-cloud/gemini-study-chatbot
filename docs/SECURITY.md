# Segurança

## Chave da API

Trate a chave da Gemini API como uma senha. Quem a tiver pode consumir a cota do seu projeto e gerar cobranças.

O projeto segue estas regras:

- A chave é lida da variável de ambiente `GEMINI_API_KEY`, carregada do arquivo `.env`.
- Nenhum arquivo versionado contém uma chave real. O `.env.example` traz só um texto de exemplo.
- O `.gitignore` bloqueia `.env` e `.streamlit/secrets.toml`.

## Antes de publicar ou fazer push

1. Confirme que o `.env` não será enviado:

   ```bash
   git status
   git check-ignore -v .env
   ```

   O segundo comando deve mostrar a regra do `.gitignore` que cobre o arquivo.

2. Procure padrões de chave nos arquivos versionados e no histórico:

   ```bash
   git grep -nE "AIza[0-9A-Za-z_-]{20,}"
   git log -p --all -S"GEMINI_API_KEY=" -- . ":(exclude).env.example"
   ```

   Os dois comandos não devem mostrar uma chave real. Se mostrarem, **não publique**: gere uma chave nova, desative a antiga e só então decida como tratar o histórico.

3. Confirme que nenhuma captura de tela, log ou documento mostra a chave.

## Se a chave vazar

1. Crie uma chave nova no [Google AI Studio](https://aistudio.google.com/apikey).
2. Atualize o `.env` e valide que o app funciona com a nova.
3. Desative a chave antiga.
4. Confira o uso da conta por sinais de consumo inesperado.

Apagar o arquivo em um commit novo **não** remove a chave do histórico do Git. A chave antiga deve ser considerada comprometida e revogada.

## Pastas sincronizadas

Se o projeto fica em uma pasta sincronizada (OneDrive, Google Drive, Dropbox), o `.env` também é enviado para a nuvem do serviço. Considere manter o projeto fora dessas pastas ou restringir o acesso à conta.

## Publicando a interface web

- A chave fica no servidor que executa o Streamlit e não é enviada ao navegador. Isso é correto: a documentação do Google recomenda não colocar a chave em código de aplicações cliente, onde ela pode ser extraída.
- O app **não tem login nem limite de uso**. Se for publicado na internet, qualquer visitante poderá gerar consumo na sua chave. Antes de publicar, considere autenticação, limite de mensagens e alertas de cobrança.
- Em plataformas de hospedagem, configure a chave nos "secrets" ou variáveis de ambiente da plataforma, nunca no repositório.

## Observação sobre as variáveis do SDK

O SDK `google-genai` lê `GEMINI_API_KEY` ou `GOOGLE_API_KEY` automaticamente. Este projeto passa a chave de forma explícita (`genai.Client(api_key=...)`), então uma variável `GOOGLE_API_KEY` definida no seu sistema não substitui a do `.env`.

## Referências

- [Usando chaves da Gemini API](https://ai.google.dev/gemini-api/docs/api-key)
- [Limites de uso](https://ai.google.dev/gemini-api/docs/rate-limits)
