/**
 * IPTV Tarefas — registro de pedidos no Google Sheets
 * ---------------------------------------------------
 * Implantação:
 *   1. script.google.com → Novo projeto → cole este arquivo
 *   2. Execute setup() uma vez (autorize o acesso à planilha)
 *   3. Implantar → Nova implantação → Tipo: App da Web
 *        Executar como: Eu
 *        Quem tem acesso: Qualquer pessoa
 *   4. Copie a URL /exec e cole em SITE_CONFIG.pedidosEndpoint (assets/js/config.js)
 *
 * Depois de cada alteração no código é preciso criar uma NOVA versão de
 * implantação: "Gerenciar implantações → editar → Versão: nova".
 */

var SHEET_ID = '1z3bw3np7cErLM42QE0--gfRYMh-isUxIEK6BovJOdgg';
var ABA = 'Pedidos';
var NOTIFICAR = 'xyz905391@gmail.com';
var MARCA = 'IPTV Tarefas';

/** Segredo compartilhado com o site. Troque por um valor seu e repita
 *  o mesmo valor em SITE_CONFIG.pedidosToken. Deixe '' para desativar. */
var TOKEN = 'troque-este-valor';

var COLUNAS = [
  'Data/hora', 'Pedido', 'Plano', 'Duração', 'Bônus', 'Conexões',
  'Total (R$)', 'Nome', 'Telefone', 'País', 'E-mail',
  'Pagamento', 'Status', 'Origem', 'Observações'
];

/* ------------------------------------------------------------------ */
/* Instalação                                                          */
/* ------------------------------------------------------------------ */

function setup() {
  var planilha = SpreadsheetApp.openById(SHEET_ID);
  var aba = planilha.getSheetByName(ABA) || planilha.insertSheet(ABA);

  aba.clear();
  aba.getRange(1, 1, 1, COLUNAS.length).setValues([COLUNAS]);

  var cabecalho = aba.getRange(1, 1, 1, COLUNAS.length);
  cabecalho.setFontWeight('bold')
           .setBackground('#0f2019')
           .setFontColor('#eaf5ef')
           .setVerticalAlignment('middle');
  aba.setRowHeight(1, 34);
  aba.setFrozenRows(1);

  var larguras = [150, 110, 130, 90, 110, 90, 100, 170, 150, 110, 210, 110, 110, 120, 240];
  for (var i = 0; i < larguras.length; i++) aba.setColumnWidth(i + 1, larguras[i]);

  aba.getRange('A2:A').setNumberFormat('dd/mm/yyyy hh:mm');
  aba.getRange('G2:G').setNumberFormat('#,##0.00');

  // Menu suspenso na coluna Status
  var status = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Novo', 'Em contato', 'Pago', 'Entregue', 'Cancelado'], true)
    .setAllowInvalid(false)
    .build();
  aba.getRange('M2:M').setDataValidation(status);

  Logger.log('Aba "%s" pronta com %s colunas.', ABA, COLUNAS.length);
}

/* ------------------------------------------------------------------ */
/* Endpoints                                                           */
/* ------------------------------------------------------------------ */

function doGet() {
  return json({ ok: true, servico: MARCA, aba: ABA });
}

function doPost(e) {
  var trava = LockService.getScriptLock();
  try {
    trava.waitLock(20000);

    var dados = ler(e);
    if (!dados) return json({ ok: false, erro: 'corpo-invalido' });
    if (TOKEN && dados.token !== TOKEN) return json({ ok: false, erro: 'token-invalido' });

    // Campos mínimos: sem nome e telefone o pedido não serve para nada.
    if (!texto(dados.nome) || !texto(dados.telefone)) {
      return json({ ok: false, erro: 'campos-obrigatorios' });
    }
    // Armadilha anti-robô: o site envia este campo sempre vazio.
    if (texto(dados.website)) return json({ ok: true, ignorado: true });

    var aba = SpreadsheetApp.openById(SHEET_ID).getSheetByName(ABA);
    if (!aba) return json({ ok: false, erro: 'aba-inexistente' });

    var agora = new Date();
    var referencia = 'IT-' + Utilities.formatDate(agora, 'America/Sao_Paulo', 'yyMMdd-HHmmss');

    aba.appendRow([
      agora,
      referencia,
      texto(dados.plano),
      texto(dados.duracao),
      dados.bonus ? '+3 meses grátis' : '—',
      Number(dados.conexoes) || 1,
      Number(dados.total) || 0,
      texto(dados.nome),
      "'" + texto(dados.telefone),     // apóstrofo: preserva o + e os zeros à esquerda
      texto(dados.pais),
      texto(dados.email),
      texto(dados.pagamento),
      'Novo',
      texto(dados.origem) || 'site',
      texto(dados.observacoes)
    ]);

    notificar(referencia, dados);
    return json({ ok: true, referencia: referencia });

  } catch (erro) {
    console.error(erro);
    return json({ ok: false, erro: String(erro) });
  } finally {
    try { trava.releaseLock(); } catch (ignorado) {}
  }
}

/* ------------------------------------------------------------------ */
/* Auxiliares                                                          */
/* ------------------------------------------------------------------ */

function ler(e) {
  try {
    if (e && e.postData && e.postData.contents) return JSON.parse(e.postData.contents);
    if (e && e.parameter && e.parameter.payload) return JSON.parse(e.parameter.payload);
    if (e && e.parameter) return e.parameter;
  } catch (erro) {
    console.error('JSON inválido: ' + erro);
  }
  return null;
}

function texto(v) {
  return v === null || v === undefined ? '' : String(v).trim().slice(0, 500);
}

function moeda(v) {
  return 'R$ ' + (Number(v) || 0).toFixed(2).replace('.', ',');
}

function notificar(referencia, d) {
  if (!NOTIFICAR) return;
  var linhas = [
    'Pedido: ' + referencia,
    'Plano: ' + texto(d.plano) + ' (' + texto(d.duracao) + (d.bonus ? ' + 3 meses grátis' : '') + ')',
    'Conexões: ' + (Number(d.conexoes) || 1),
    'Total: ' + moeda(d.total),
    '',
    'Nome: ' + texto(d.nome),
    'Telefone: ' + texto(d.telefone) + (texto(d.pais) ? ' (' + texto(d.pais) + ')' : ''),
    'E-mail: ' + (texto(d.email) || '—'),
    'Pagamento: ' + (texto(d.pagamento) || '—'),
    '',
    'Planilha: https://docs.google.com/spreadsheets/d/' + SHEET_ID
  ];
  MailApp.sendEmail({
    to: NOTIFICAR,
    subject: '[' + MARCA + '] Novo pedido ' + referencia + ' — ' + texto(d.nome),
    body: linhas.join('\n')
  });
}

function json(objeto) {
  return ContentService
    .createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ------------------------------------------------------------------ */
/* Teste local (Executar → testar)                                     */
/* ------------------------------------------------------------------ */

function testar() {
  var resposta = doPost({
    postData: {
      contents: JSON.stringify({
        token: TOKEN,
        plano: 'Plano Gold',
        duracao: '15 meses',
        bonus: true,
        conexoes: 2,
        total: 509.83,
        nome: 'Teste Manual',
        telefone: '+55 11 98877-6655',
        pais: 'Brasil',
        email: 'teste@exemplo.com.br',
        pagamento: 'Cartão',
        origem: 'teste'
      })
    }
  });
  Logger.log(resposta.getContent());
}

/**
 * Diagnóstico: mostra em qual planilha o script está mexendo e o que existe lá.
 * Execute esta função e leia o "Registro de execução".
 */
function diagnosticar() {
  Logger.log('Conta em uso: %s', Session.getEffectiveUser().getEmail());
  Logger.log('SHEET_ID no código: %s', SHEET_ID);
  try {
    var planilha = SpreadsheetApp.openById(SHEET_ID);
    Logger.log('Planilha encontrada: "%s"', planilha.getName());
    Logger.log('URL: %s', planilha.getUrl());
    var abas = planilha.getSheets().map(function (a) { return a.getName(); });
    Logger.log('Abas existentes: %s', abas.join(' | '));
    Logger.log('Aba "%s" existe? %s', ABA, abas.indexOf(ABA) >= 0 ? 'SIM' : 'NÃO — rode setup()');
    Logger.log('E-mail de aviso: %s', NOTIFICAR);
    Logger.log('Cota de e-mails restante hoje: %s', MailApp.getRemainingDailyQuota());
  } catch (erro) {
    Logger.log('ERRO ao abrir a planilha: %s', erro);
    Logger.log('Confira se o SHEET_ID está certo e se esta conta tem acesso ao documento.');
  }
}
