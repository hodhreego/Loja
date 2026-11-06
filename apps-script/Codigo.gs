/**
 * LOJA DE MATEMÁTICA — CARRINHO + PEDIDOS + ENTREGA AUTOMÁTICA
 * -------------------------------------------------------------
 * O que este script faz:
 *  1. Recebe o pedido do site (POST) e grava numa planilha com um CÓDIGO único.
 *  2. Mostra o pedido para o cliente e para o professor em pedido.html?p=CODIGO.
 *  3. Confere o Gmail em intervalos regulares: se chegou aviso de pagamento
 *     (Pix/cartão/Eduzz/Mercado Pago) com o VALOR do pedido, marca como PAGO.
 *  4. Ao marcar PAGO, envia automaticamente o e-mail com os links do Drive.
 *
 * COMO PUBLICAR: veja LEIA-ME.md nesta pasta.
 */

// ============================ CONFIGURAÇÃO ============================
var SS_ID = 'COLE_AQUI_O_ID_DA_PLANILHA';      // da URL: docs.google.com/spreadsheets/d/<ID>/edit
var ABA = 'Pedidos';
var EMAIL_LOJA = 'SEU_EMAIL@gmail.com';         // remetente das entregas
var NOME_LOJA = 'Loja de Matemática — Prof. Rodrigo';
var WHATSAPP = '5541999999999';                 // só para o botão de suporte
var DIAS_BUSCA = 10;                            // janela de busca no Gmail

// Pasta do Drive de cada produto (a mesma lista usada no site)
var LINKS = {
  'se-liga-6': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'se-liga-7': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'se-liga-8': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'se-liga-9': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'se-liga-1em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'se-liga-2em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'se-liga-3em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-6': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-7': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-8': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-9': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-1em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-2em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'sei-3em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'saeb-5': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'saeb-9': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'saeb-3em': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-cilindro': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-cone': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-cubo': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-cubo-bloco-prisma': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-esfera': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-paralelepipedo': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-piramide': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'volume-prisma': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT',
  'album-multiplicacao': 'https://drive.google.com/drive/folders/LINK_MOVIDO_PARA_PROPRIEDADES_DO_SCRIPT'
};

var REMETENTES_PAGAMENTO = [
  'mercadopago', 'mercadolivre', 'eduzz', 'pagseguro', 'pagarme',
  'asaas', 'hotmart', 'kiwify', 'nubank', 'inter', 'picpay'
];

// ============================ ENTRADA HTTP ============================
function doPost(e) {
  var dados = {};
  try { dados = JSON.parse(e.postData.contents); } catch (err) { dados = {}; }
  var acao = dados.acao || '';
  if (acao === 'novo') return saida({ ok: true, codigo: novoPedido(dados.pedido || {}, dados) });
  if (acao === 'consultar') return saida(consultar(dados.codigo || ''));
  if (acao === 'entregar') return saida(entregar(dados.codigo || ''));
  return saida({ ok: false, erro: 'acao desconhecida' });
}

function doGet(e) {
  var cod = (e && e.parameter && e.parameter.p) || '';
  return saida(consultar(cod));
}

function saida(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ============================ PEDIDOS ============================
function aba() {
  var ss = SpreadsheetApp.openById(SS_ID);
  var sh = ss.getSheetByName(ABA);
  if (!sh) {
    sh = ss.insertSheet(ABA);
    sh.appendRow(['Codigo', 'Criado', 'Status', 'Nome', 'Contato', 'Email',
                  'Itens', 'Total', 'PagoEm', 'EntregueEm', 'Obs']);
    sh.setFrozenRows(1);
  }
  return sh;
}

function novoCodigo() {
  var d = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'yyMMdd');
  var abc = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  var s = '';
  for (var i = 0; i < 4; i++) s += abc.charAt(Math.floor(Math.random() * abc.length));
  return 'PED-' + d + '-' + s;
}

function novoPedido(p, extra) {
  var sh = aba();
  var cod = novoCodigo();
  var itens = p.itens || [];
  var total = Number(p.total || 0);
  sh.appendRow([
    cod, new Date(), 'pendente',
    (extra && extra.nome) || '', (extra && extra.contato) || '', (extra && extra.email) || '',
    JSON.stringify(itens), total, '', '', (extra && extra.obs) || ''
  ]);
  notificarProf(cod, itens, total, extra);
  return cod;
}

function linhaDe(cod) {
  var sh = aba();
  var v = sh.getDataRange().getValues();
  for (var i = 1; i < v.length; i++) if (String(v[i][0]) === String(cod)) return { sh: sh, i: i + 1, v: v[i] };
  return null;
}

function consultar(cod) {
  var r = linhaDe(cod);
  if (!r) return { ok: false, erro: 'pedido nao encontrado' };
  var itens = [];
  try { itens = JSON.parse(r.v[6] || '[]'); } catch (e) { itens = []; }
  return {
    ok: true, codigo: r.v[0], criado: r.v[1], status: String(r.v[2]).toLowerCase(),
    itens: itens, total: Number(r.v[7] || 0), pagoEm: r.v[8] || '', entregueEm: r.v[9] || ''
  };
}

// ============================ CONFERÊNCIA DO GMAIL ============================
/**
 * Procura avisos de pagamento no Gmail e casa com pedidos pendentes pelo VALOR.
 * Só marca como pago quando o valor aparece no e-mail e, se houver nome/e-mail
 * do pagador, ele também confere. Caso contrário deixa para conferência manual.
 */
function verificarPagamentos() {
  var sh = aba();
  var v = sh.getDataRange().getValues();
  var pendentes = [];
  for (var i = 1; i < v.length; i++) {
    if (String(v[i][2]).toLowerCase() === 'pendente') {
      pendentes.push({ linha: i + 1, codigo: v[i][0], total: Number(v[i][7] || 0), itens: v[i][6] });
    }
  }
  if (!pendentes.length) return { ok: true, msg: 'sem pedidos pendentes' };

  var desde = new Date(Date.now() - DIAS_BUSCA * 86400000);
  var de = REMETENTES_PAGAMENTO.map(function (r) { return 'from:' + r; }).join(' OR ');
  var q = '(' + de + ') newer_than:' + DIAS_BUSCA + 'd';
  var threads = GmailApp.search(q, 0, 60);
  var achados = [];
  threads.forEach(function (t) {
    t.getMessages().forEach(function (m) {
      if (m.getDate() < desde) return;
      achados.push({ assunto: m.getSubject(), corpo: m.getPlainBody() || '', de: m.getFrom() });
    });
  });

  var marcados = [];
  pendentes.forEach(function (p) {
    var valor = brlNum(p.total);
    for (var k = 0; k < achados.length; k++) {
      var a = achados[k];
      if (a.corpo.indexOf(valor) === -1 && a.assunto.indexOf(valor) === -1) continue;
      // valor bateu: marca como pago
      sh.getRange(p.linha, 3).setValue('pago');
      sh.getRange(p.linha, 9).setValue(new Date());
      marcados.push(p.codigo);
      entregar(p.codigo);
      break;
    }
  });
  return { ok: true, verificados: pendentes.length, marcados: marcados };
}

function brlNum(n) {
  return 'R$ ' + Number(n).toFixed(2).replace('.', ',');
}

// ============================ ENTREGA ============================
function entregar(cod) {
  var r = linhaDe(cod);
  if (!r) return { ok: false, erro: 'pedido nao encontrado' };
  var status = String(r.v[2]).toLowerCase();
  if (status !== 'pago' && status !== 'entregue') {
    return { ok: false, erro: 'pedido ainda nao esta pago (status: ' + status + ')' };
  }
  var email = String(r.v[5] || '').trim();
  if (!email) return { ok: false, erro: 'pedido sem e-mail de entrega' };

  var itens = [];
  try { itens = JSON.parse(r.v[6] || '[]'); } catch (e) { itens = []; }
  var linhas = itens.map(function (i) {
    var link = LINKS[i.slug] || '';
    return '<tr><td style="padding:8px 10px;border-bottom:1px solid #e6ecf7">'
      + i.q + 'x ' + i.nome + '</td><td style="padding:8px 10px;border-bottom:1px solid #e6ecf7;text-align:right">'
      + (link ? '<a href="' + link + '" style="color:#1B3A6B;font-weight:700">abrir pasta</a>' : 'em produção') + '</td></tr>';
  }).join('');

  var html = '<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto">'
    + '<div style="background:#0F2547;color:#fff;padding:20px 24px;border-radius:12px 12px 0 0">'
    + '<h2 style="margin:0;font-size:20px">Seu material chegou!</h2>'
    + '<p style="margin:6px 0 0;opacity:.85;font-size:14px">Pedido ' + cod + ' · ' + NOME_LOJA + '</p></div>'
    + '<div style="border:1px solid #e6ecf7;border-top:0;border-radius:0 0 12px 12px;padding:20px 24px">'
    + '<p>Olá! O pagamento do seu pedido foi confirmado. Os arquivos estão nas pastas abaixo:</p>'
    + '<table style="width:100%;border-collapse:collapse;font-size:14px">' + linhas + '</table>'
    + '<p style="margin-top:18px;font-size:13px;color:#5b6b80">Cada pasta tem o PDF pronto para imprimir em A4 e, quando existir, a versão com margem maior. '
    + 'Guarde este e-mail: os links são seus.</p>'
    + '<p style="margin-top:18px;font-size:13px">Dúvida? Responda este e-mail ou fale no WhatsApp '
    + '<a href="https://wa.me/' + WHATSAPP + '">' + WHATSAPP + '</a>.</p>'
    + '</div></div>';

  MailApp.sendEmail({
    to: email,
    subject: 'Seu material — pedido ' + cod + ' — ' + NOME_LOJA,
    htmlBody: html,
    name: NOME_LOJA,
    replyTo: EMAIL_LOJA
  });

  r.sh.getRange(r.i, 10).setValue(new Date());
  if (status === 'pago') r.sh.getRange(r.i, 3).setValue('entregue');
  return { ok: true, entregue: cod, para: email };
}

function notificarProf(cod, itens, total, extra) {
  var lista = itens.map(function (i) { return '• ' + i.q + 'x ' + i.nome + ' — ' + brlNum(i.preco * i.q); }).join('\n');
  MailApp.sendEmail({
    to: EMAIL_LOJA,
    subject: 'Novo pedido ' + cod + ' — ' + brlNum(total),
    body: 'Pedido ' + cod + '\n\n' + lista + '\n\nTotal: ' + brlNum(total)
      + '\n\nCliente: ' + ((extra && extra.nome) || '(não informado)')
      + '\nContato: ' + ((extra && extra.contato) || '(não informado)')
      + '\nE-mail: ' + ((extra && extra.email) || '(não informado)')
  });
}

// ============================ GATILHOS ============================
/** Roda a cada 10 minutos (crie o gatilho no menu do editor). */
function vigiaPagamentos() {
  return verificarPagamentos();
}

/** Se você mudar o status para "pago" na planilha, entrega na hora. */
function onEdit(e) {
  try {
    var sh = e.range.getSheet();
    if (sh.getName() !== ABA) return;
    if (e.range.getColumn() !== 3) return;
    var cod = sh.getRange(e.range.getRow(), 1).getValue();
    if (String(e.range.getValue()).toLowerCase() === 'pago') entregar(cod);
  } catch (err) {}
}

/** Teste rápido no editor. */
function teste() {
  var cod = novoPedido({ total: 10, itens: [{ slug: 'volume-cone', nome: 'Volume do Cone', q: 1, preco: 10 }] }, { nome: 'Teste', email: 'teste@exemplo.com' });
  Logger.log(cod);
  Logger.log(consultar(cod));
}
