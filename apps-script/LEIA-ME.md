# Carrinho + Pedidos + Entrega automática

Três peças:

1. **Site** (`index.html`) — carrinho com código do pedido, enviado pelo WhatsApp.
2. **Página do pedido** (`pedido.html?p=CODIGO`) — cliente e professor veem o mesmo pedido.
3. **Google Apps Script** (`apps-script/Codigo.gs`) — grava o pedido numa planilha, confere o Gmail e entrega por e-mail.

---

## 1. Criar a planilha

1. Abra <https://sheets.new> e dê o nome `Pedidos Loja de Matemática`.
2. Copie o ID da URL: `docs.google.com/spreadsheets/d/`**`ESTE_TRECHO`**`/edit`.

## 2. Publicar o script

1. Na planilha: **Extensões → Apps Script**.
2. Apague o conteúdo e cole `apps-script/Codigo.gs`.
3. No topo do arquivo, ajuste:
   - `SS_ID` → o ID da planilha;
   - `EMAIL_LOJA` → seu Gmail;
   - `WHATSAPP` → seu número com DDI (ex.: `5541999999999`).
4. **Pastas de entrega (privacidade).** Este arquivo fica no repositório público,
   então os links do Drive **não** ficam nele. Em **Configurações do projeto →
   Propriedades do script**, crie uma propriedade por produto:
   `link_se-liga-6` = `https://drive.google.com/drive/folders/...` (o nome é
   `link_` + o slug usado no site). Sem isso, a entrega sai como "em produção".
5. Salve (Ctrl+S) e rode a função `teste` uma vez para autorizar as permissões
   (Gmail, Planilha, E-mail). Ele cria um pedido de teste na planilha.

## 3. Publicar como Web App

1. **Implantar → Nova implantação → Tipo: App da Web**.
2. Executar como: **eu**. Quem tem acesso: **qualquer pessoa**.
3. Copie a URL que termina em `/exec`.

## 4. Ligar no site

No `index.html`, procure:

```js
const API_PEDIDOS="";
```

e cole a URL entre as aspas. Faça o mesmo em `pedido.html`.

Depois rode `python build_loja.py` e publique.

## 5. Conferir pagamentos no Gmail (automático)

O script procura e-mails de pagamento (Mercado Pago, Eduzz, PagSeguro, Pagar.me,
Asaas, Hotmart, Kiwify, Nubank, Inter, PicPay) dos últimos 10 dias.
Se o **valor** do pedido aparecer no e-mail, o pedido vira **pago** e o material é
enviado na hora para o e-mail do cliente.

Para rodar sozinho:

1. No editor do Apps Script: **Acionadores (relógio) → Criar acionador**.
2. Função: `vigiaPagamentos`. Evento: **Baseado em tempo → A cada 10 minutos**.
3. Salvar.

Ao marcar **pago** manualmente na coluna *Status*, o `onEdit` dispara a entrega.

## 6. Colunas da planilha

| Coluna | O que é |
|---|---|
| Codigo | código do pedido (ex.: `PED-261106-A7K2`) |
| Criado | data/hora do pedido |
| Status | `pendente` → `pago` → `entregue` (ou `cancelado`) |
| Nome / Contato / Email | dados do comprador (o site envia se preenchidos) |
| Itens | JSON com slug, nome, preço e quantidade |
| Total | valor em reais |
| PagoEm / EntregueEm | datas automáticas |
| Obs | observações suas |

## Limites honestos

- O casamento pelo **valor** pode errar se dois pedidos tiverem o mesmo total no
  mesmo dia. Nesse caso o script marca o primeiro pendente; confira na planilha.
- Nome/e-mail do pagador no aviso do banco costuma vir incompleto; por isso o
  critério principal é o valor.
- A entrega é **por e-mail**. Se quiser entrega dentro do WhatsApp, é preciso a
  API oficial (número verificado + template aprovado, com custo por conversa).
- Links do Drive: use pastas com permissão “qualquer pessoa com o link” **somente
  leitura**, nunca edição.
