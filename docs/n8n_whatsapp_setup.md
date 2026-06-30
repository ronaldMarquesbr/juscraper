# Automação n8n + WhatsApp para alertas de leads

Esta documentação explica como rodar a automação que consulta leads no Supabase, envia alerta pelo WhatsApp e atualiza o status do lead para `SENT`.

## Visão geral

```text
Supabase → n8n busca leads NEW → monta mensagem → envia WhatsApp → atualiza lead para SENT
```

## Arquivos usados

Segredos fora do repositório:

```text
C:\Users\ponci\n8n-secrets.ps1
C:\Users\ponci\start-n8n.ps1
```

Workflow exportado dentro do projeto:

```text
C:\Users\ponci\juscraper\n8n\workflows\juscraper_whatsapp_leads.json
```

## Segurança

Nunca suba para o GitHub arquivos com chaves ou tokens:

```text
.env
n8n-secrets.ps1
start-n8n.ps1
```

## 1. Arquivo de segredos

Crie:

```powershell
notepad C:\Users\ponci\n8n-secrets.ps1
```

Conteúdo:

```powershell
$env:N8N_BLOCK_ENV_ACCESS_IN_NODE="false"

$env:SUPABASE_URL="https://SEU-PROJETO.supabase.co"
$env:SUPABASE_SERVICE_ROLE_KEY="SUA_SUPABASE_SECRET_KEY"

$env:WHATSAPP_ACCESS_TOKEN="SEU_TOKEN_DA_META"
$env:WHATSAPP_PHONE_NUMBER_ID="SEU_PHONE_NUMBER_ID"
$env:WHATSAPP_TO_NUMBER="55DDDNUMERO_DESTINATARIO"
```

Exemplo de número:

```powershell
$env:WHATSAPP_TO_NUMBER="5591985743244"
```

Não use `+`, espaços, traços ou `0` antes do DDD.

## 2. Script para iniciar o n8n

Crie:

```powershell
notepad C:\Users\ponci\start-n8n.ps1
```

Conteúdo:

```powershell
. "C:\Users\ponci\n8n-secrets.ps1"

Write-Host "N8N_BLOCK_ENV_ACCESS_IN_NODE=$env:N8N_BLOCK_ENV_ACCESS_IN_NODE"
Write-Host "SUPABASE_URL configurada: $([bool]$env:SUPABASE_URL)"
Write-Host "SUPABASE_SERVICE_ROLE_KEY configurada: $([bool]$env:SUPABASE_SERVICE_ROLE_KEY)"
Write-Host "WHATSAPP_ACCESS_TOKEN configurado: $([bool]$env:WHATSAPP_ACCESS_TOKEN)"
Write-Host "WHATSAPP_PHONE_NUMBER_ID configurado: $([bool]$env:WHATSAPP_PHONE_NUMBER_ID)"
Write-Host "WHATSAPP_TO_NUMBER configurado: $([bool]$env:WHATSAPP_TO_NUMBER)"

n8n.cmd
```

## 3. Iniciar o n8n

Feche instâncias antigas:

```powershell
taskkill /IM node.exe /F
```

Inicie:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\ponci\start-n8n.ps1
```

Resultado esperado:

```text
N8N_BLOCK_ENV_ACCESS_IN_NODE=false
SUPABASE_URL configurada: True
SUPABASE_SERVICE_ROLE_KEY configurada: True
WHATSAPP_ACCESS_TOKEN configurado: True
WHATSAPP_PHONE_NUMBER_ID configurado: True
WHATSAPP_TO_NUMBER configurado: True
```

Acesse:

```text
http://localhost:5678
```

## 4. Configuração dos nodes

### Buscar leads NEW

Método:

```text
GET
```

URL:

```text
{{ $env.SUPABASE_URL }}/rest/v1/lead
```

Query parameters:

```text
select = id,created_at,name,username,problem_description,category,status,comment_id
status = eq.NEW
order = created_at.asc
limit = 5
```

Headers:

```text
apikey          {{ $env.SUPABASE_SERVICE_ROLE_KEY }}
Authorization   Bearer {{ $env.SUPABASE_SERVICE_ROLE_KEY }}
Content-Type    application/json
```

### Montar mensagem WhatsApp

Tipo: `Code`

Código:

```javascript
const inputItems = $input.all();

let leads = [];

for (const item of inputItems) {
  if (Array.isArray(item.json)) {
    leads.push(...item.json);
  } else if (Array.isArray(item.json.data)) {
    leads.push(...item.json.data);
  } else if (item.json && item.json.id) {
    leads.push(item.json);
  }
}

return leads.map((lead) => {
  const nome = lead.name || "Não informado";
  const usuario = lead.username
    ? `@${String(lead.username).replace(/^@/, "")}`
    : "Não informado";

  const categoria = lead.category || "Não classificada";
  const descricao = lead.problem_description || "Sem descrição";
  const criadoEm = lead.created_at || "Sem data";

  const mensagem = [
    "⚖️ Novo possível lead jurídico",
    "",
    `ID: ${lead.id}`,
    `Nome: ${nome}`,
    `Instagram: ${usuario}`,
    `Categoria: ${categoria}`,
    `Status: ${lead.status || "NEW"}`,
    `Criado em: ${criadoEm}`,
    "",
    "Descrição:",
    descricao,
    "",
    "Ação sugerida: revisar no Juscraper antes de qualquer contato externo.",
  ].join("\n");

  return {
    json: {
      lead_id: lead.id,
      mensagem,
      lead,
    },
  };
});
```

### Enviar WhatsApp

Método:

```text
POST
```

URL:

```text
https://graph.facebook.com/v25.0/{{ $env.WHATSAPP_PHONE_NUMBER_ID }}/messages
```

Headers:

```text
Authorization    Bearer {{ $env.WHATSAPP_ACCESS_TOKEN }}
Content-Type     application/json
```

Body em modo `Expression`:

```javascript
{
  {
    JSON.stringify({
      messaging_product: "whatsapp",
      to: $env.WHATSAPP_TO_NUMBER,
      type: "text",
      text: {
        preview_url: false,
        body: $json.mensagem,
      },
    });
  }
}
```

Observação: para `type: "text"`, o destinatário precisa estar dentro da janela de atendimento. Para testes, envie antes uma mensagem do WhatsApp pessoal para o número comercial.

### Marcar lead como SENT

Método:

```text
PATCH
```

URL:

```text
{{ $env.SUPABASE_URL }}/rest/v1/lead
```

Query parameter:

```text
id = eq.{{ $('Montar mensagem WhatsApp').item.json.lead_id }}
```

Se o campo estiver em modo Expression:

```javascript
={{ 'eq.' + $('Montar mensagem WhatsApp').item.json.lead_id }}
```

Headers:

```text
apikey          {{ $env.SUPABASE_SERVICE_ROLE_KEY }}
Authorization   Bearer {{ $env.SUPABASE_SERVICE_ROLE_KEY }}
Content-Type    application/json
Prefer          return=minimal
```

Body em modo `Expression`:

```javascript
{
  {
    JSON.stringify({
      status: "SENT",
      updated_at: $now.toISO(),
    });
  }
}
```

## 5. Testar

No Supabase, coloque um lead como `NEW`:

```sql
update public.lead
set status = 'NEW'
where id = 1;
```

Ou crie um lead de teste:

```sql
insert into public.lead (
  name,
  username,
  problem_description,
  category,
  status
)
values (
  'Cliente Teste',
  'cliente_teste',
  'Tenho dúvidas sobre um problema trabalhista.',
  'EMPLOYMENT',
  'NEW'
);
```

Resultado esperado:

```text
1. O WhatsApp recebe a mensagem do lead.
2. O lead no Supabase muda de NEW para SENT.
3. O mesmo lead não é enviado novamente no próximo ciclo.
```

## 6. Exportar o workflow

No n8n:

```text
Workflow → Export / Download
```

Salve em:

```text
C:\Users\ponci\juscraper\n8n\workflows\juscraper_whatsapp_leads.json
```

Antes de commitar, abra o JSON exportado e confirme que aparecem apenas variáveis:

```text
{{ $env.WHATSAPP_ACCESS_TOKEN }}
{{ $env.SUPABASE_SERVICE_ROLE_KEY }}
{{ $env.WHATSAPP_TO_NUMBER }}
```

Não pode aparecer:

```text
sb_secret_...
EAAN...
```

## 7. Atualizar .gitignore

Na raiz do projeto:

```gitignore
.env
.venv/
__pycache__/
*.pyc
n8n-secrets.ps1
start-n8n.ps1
```

## 8. Commit

```powershell
cd C:\Users\ponci\juscraper

mkdir docs -ErrorAction SilentlyContinue
mkdir n8n -ErrorAction SilentlyContinue
mkdir n8n\workflows -ErrorAction SilentlyContinue

git status
git add docs/n8n_whatsapp_setup.md n8n/workflows/juscraper_whatsapp_leads.json .gitignore
git commit -m "docs: adicionar guia da automacao n8n com WhatsApp"
```

## 9. Problemas comuns

### access to env vars denied

O n8n não foi iniciado com `N8N_BLOCK_ENV_ACCESS_IN_NODE=false`.

Use:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\ponci\start-n8n.ps1
```

### n8n's port 5678 is already in use

Feche instâncias antigas:

```powershell
taskkill /IM node.exe /F
```

### (#100) Invalid parameter

Verifique:

```text
1. WHATSAPP_TO_NUMBER deve ser o destinatário, não o número comercial.
2. WHATSAPP_PHONE_NUMBER_ID deve ser o ID do número da Meta.
3. Para mensagem text, o destinatário precisa estar dentro da janela de atendimento.
4. O número deve estar no formato 55DDDNUMERO.
```

### JSON Body inválido

Use o body do WhatsApp em modo `Expression` com `JSON.stringify`.

## 10. Próximos passos

```text
1. Criar template oficial novo_lead_juridico aprovado pela Meta.
2. Configurar webhook para receber respostas do WhatsApp.
3. Atualizar lead para APPROVED ou DISCARDED conforme resposta.
4. Criar documentação de produção com Docker ou servidor.
```
