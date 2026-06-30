# Juscraper + n8n + WhatsApp

Automação criada para consultar leads com `status = NEW` no Supabase, enviar alerta interno no WhatsApp e depois marcar o lead como `SENT`.

## Variáveis necessárias no n8n

Configure estas variáveis no ambiente do n8n:

```env
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_SERVICE_ROLE_KEY=SUA_SERVICE_ROLE_KEY
WHATSAPP_ACCESS_TOKEN=SEU_TOKEN_META
WHATSAPP_PHONE_NUMBER_ID=SEU_PHONE_NUMBER_ID
WHATSAPP_TO_NUMBER=55DDDNUMERO
```

`WHATSAPP_TO_NUMBER` deve ficar em formato internacional, sem +, sem espaços e sem traços.

Exemplo:

```env
WHATSAPP_TO_NUMBER=5591999999999
```

## Fluxo

1. Schedule Trigger roda a cada 10 minutos.
2. Busca até 5 leads com `status = NEW`.
3. Monta uma mensagem com dados do lead.
4. Envia a mensagem via WhatsApp Cloud API.
5. Atualiza o lead para `status = SENT`.

## Importação no n8n

1. Abra o n8n.
2. Vá em Workflows.
3. Clique em Import from File.
4. Escolha `juscraper_n8n_whatsapp_leads.json`.
5. Confira os nodes HTTP Request.
6. Ative o workflow.

## Observação

Essa automação é para alerta interno da equipe. Não recomendo contato automático com pessoas capturadas em redes sociais sem validação humana e base legal adequada.
