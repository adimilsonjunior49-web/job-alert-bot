# Job Alert Bot (Telegram) — GitHub Actions (a cada 3 horas)

Este projeto coleta vagas recentes de múltiplas fontes (via APIs quando disponível), filtra pelas regras de negócio
e envia alertas para um bot do Telegram.

## ✅ O que ele entrega
- A cada 3 horas (GitHub Actions cron), busca vagas recentes.
- Filtra por:
  - Cargos: Analista Sênior, Coordenador, Supervisor, Gerente
  - Áreas: Riscos/Seguro, Qualidade, ESG
  - Setores: logística, seguradora, corretora, transportadoras
  - Regime: CLT
  - Localidade:
    - Brasil inteiro se 100% remoto
    - Presencial/Híbrido apenas São Paulo (cidade)
- Deduplica para não reenviar a mesma vaga.

## 1) Criar bot no Telegram
1. No Telegram, fale com **@BotFather**
2. Crie um bot com `/newbot`
3. Copie o **BOT TOKEN**

Para obter seu **CHAT_ID**:
- Envie uma mensagem qualquer para o bot (ex.: `/start`)
- Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
- Pegue o `chat.id` do retorno

## 2) Configurar Secrets do GitHub
No seu repositório: **Settings → Secrets and variables → Actions → New repository secret**

Obrigatórios:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Opcionais (habilitam mais fontes):
- `JOOBLE_API_KEY`
- `INFOJOBS_CLIENT_ID`
- `INFOJOBS_CLIENT_SECRET`

## 3) Rodar localmente
```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
export JOOBLE_API_KEY="..."   # opcional
python -m src.main
```

## 4) Rodar no GitHub Actions
O workflow está em `.github/workflows/scheduler.yml` e roda:
- Automaticamente a cada 3 horas (UTC)
- Manualmente via `workflow_dispatch`

## Observação importante (ToS/anti-bloqueio)
Este projeto prioriza fontes por **API** e integração “amigável”.
Evite scraping agressivo de portais que proíbam isso nos termos.
