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
/** Nome da aba de destino.
 *  Deixe '' para usar a PRIMEIRA aba da planilha (a que você já tem aberta).
 *  Coloque 'Pedidos' para o script criar e usar uma aba separada. */
var ABA = '';
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
  var aba = garantirAba(true);
  Logger.log('Aba "%s" pronta com %s colunas.', ABA, COLUNAS.length);
  return aba;
}

/**
 * Devolve a aba de pedidos, criando e formatando se ela não existir.
 * Chamada também pelo doPost: assim um pedido nunca se perde por causa
 * de uma aba ausente, mesmo que setup() nunca tenha sido executado.
 */
function garantirAba(reformatar) {
  var planilha = SpreadsheetApp.openById(SHEET_ID);

  // Sem nome definido: usa a primeira aba da planilha.
  if (!ABA) {
    var primeira = planilha.getSheets()[0];
    if (reformatar) Logger.log('Usando a primeira aba: "%s"', primeira.getName());
    return primeira;
  }

  var aba = planilha.getSheetByName(ABA);
  var nova = !aba;
  if (nova) aba = planilha.insertSheet(ABA);
  if (!nova && !reformatar) return aba;

  if (reformatar) aba.clear();
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

  var status = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Novo', 'Em contato', 'Pago', 'Entregue', 'Cancelado'], true)
    .setAllowInvalid(false)
    .build();
  aba.getRange('M2:M').setDataValidation(status);

  return aba;
}

/** Remove acentos e maiúsculas, para comparar cabeçalhos com segurança. */
function chave(texto) {
  return String(texto || '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]/g, '');
}

/**
 * Nomes aceitos para cada campo, em português, francês e inglês.
 * Assim o script funciona tanto na aba "Pedidos" quanto na planilha
 * que você já usa nos outros sites.
 */
var SINONIMOS = {
  data:      ['datahora', 'data', 'date'],
  referencia:['pedido', 'referencia', 'commande', 'reference', 'order'],
  plano:     ['plano', 'formule', 'formula', 'pack', 'plan'],
  duracao:   ['duracao', 'duree', 'duration'],
  bonus:     ['bonus', 'offert', 'oferta'],
  conexoes:  ['conexoes', 'connexions', 'connections', 'telas'],
  total:     ['totalr', 'total', 'prix', 'prixe', 'preco', 'price', 'valor', 'montant'],
  nome:      ['nome', 'nom', 'name', 'cliente', 'client'],
  telefone:  ['telefone', 'telephone', 'phone', 'whatsapp', 'tel'],
  pais:      ['pais', 'pays', 'country'],
  email:     ['email', 'mail', 'ecorreio'],
  pagamento: ['pagamento', 'paiement', 'payment'],
  status:    ['status', 'statut', 'estado'],
  origem:    ['origem', 'origine', 'source', 'site'],
  obs:       ['observacoes', 'obs', 'notes', 'remarques', 'comentarios']
};

/** Escreve uma linha respeitando os cabeçalhos existentes na aba. */
function escreverLinha(aba, valores) {
  var largura = Math.max(aba.getLastColumn(), 1);
  var cabecalhos = aba.getRange(1, 1, 1, largura).getValues()[0].map(chave);

  // Aba vazia, sem cabeçalho: cria o padrão do script.
  if (!cabecalhos.join('')) {
    aba.getRange(1, 1, 1, COLUNAS.length).setValues([COLUNAS]);
    aba.setFrozenRows(1);
    cabecalhos = COLUNAS.map(chave);
    largura = COLUNAS.length;
  }

  var linha = new Array(largura).fill('');
  var usados = 0;

  Object.keys(SINONIMOS).forEach(function (campo) {
    if (valores[campo] === undefined) return;
    for (var i = 0; i < cabecalhos.length; i++) {
      if (SINONIMOS[campo].indexOf(cabecalhos[i]) >= 0) {
        linha[i] = valores[campo];
        usados++;
        return;
      }
    }
  });

  if (!usados) {
    // Nenhum cabeçalho reconhecido: grava na ordem padrão, sem perder o pedido.
    Logger.log('Nenhum cabeçalho reconhecido em "%s" — gravando na ordem padrão.', aba.getName());
    linha = COLUNAS.map(function (c) {
      var achado = '';
      Object.keys(SINONIMOS).forEach(function (campo) {
        if (SINONIMOS[campo].indexOf(chave(c)) >= 0 && valores[campo] !== undefined) achado = valores[campo];
      });
      return achado;
    });
  }

  aba.appendRow(linha);
  return usados;
}

/* ------------------------------------------------------------------ */
/* Endpoints                                                           */
/* ------------------------------------------------------------------ */

function doGet() {
  var existe = false;
  try {
    existe = !!SpreadsheetApp.openById(SHEET_ID).getSheetByName(ABA);
  } catch (erro) {}
  return json({ ok: true, servico: MARCA, aba: ABA, abaExiste: existe });
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

    var aba = garantirAba(false);

    var agora = new Date();
    var referencia = 'IT-' + Utilities.formatDate(agora, 'America/Sao_Paulo', 'yyMMdd-HHmmss');

    var usados = escreverLinha(aba, {
      data: agora,
      referencia: referencia,
      plano: texto(dados.plano),
      duracao: texto(dados.duracao),
      bonus: dados.bonus ? '+3 meses grátis' : '—',
      conexoes: Number(dados.conexoes) || 1,
      total: Number(dados.total) || 0,
      nome: texto(dados.nome),
      telefone: "'" + texto(dados.telefone),   // apóstrofo preserva o + e os zeros
      pais: texto(dados.pais),
      email: texto(dados.email),
      pagamento: texto(dados.pagamento),
      status: 'Novo',
      origem: texto(dados.origem) || 'site',
      obs: texto(dados.observacoes)
    });
    Logger.log('Linha gravada em "%s" (%s colunas preenchidas).', aba.getName(), usados);

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

  var plano = texto(d.plano) + (texto(d.duracao) ? ' · ' + texto(d.duracao) : '') +
              (d.bonus ? ' · +3 meses grátis' : '');
  var telefone = texto(d.telefone);
  var digitos = telefone.replace(/[^0-9]/g, '');
  var quando = Utilities.formatDate(new Date(), 'America/Sao_Paulo', "dd/MM/yyyy 'às' HH:mm");

  var copiavel = function (valor) {
    return '<br><span style="display:inline-block;margin-top:6px;padding:5px 9px;border-radius:6px;' +
      'background:#eef4f1;border:1px solid #d7e3dd;font-family:Consolas,Menlo,monospace;' +
      'font-size:13px;font-weight:400;color:#12211a;-webkit-user-select:all;user-select:all">' +
      valor + '</span>';
  };

  // Cada linha: [rótulo, HTML exibido, texto puro para o corpo simples]
  var linhas = [
    ['Pedido', referencia, referencia],
    ['Plano', plano, plano],
    ['Preço', moeda(d.total), moeda(d.total)],
    ['Conexões', String(Number(d.conexoes) || 1), String(Number(d.conexoes) || 1)],
    ['Nome', texto(d.nome), texto(d.nome)],
    ['Telefone',
      (digitos ? '<a href="tel:' + telefone + '" style="color:#0b7a4b">' + telefone + '</a>' : telefone) +
      (digitos ? copiavel(digitos) +
        '<br><span style="font-size:11px;color:#8a9a92">toque e segure (ou clique duas vezes) para copiar</span>' : ''),
      telefone + (digitos ? '  [' + digitos + ']' : '')],
    ['E-mail',
      texto(d.email)
        ? '<a href="mailto:' + texto(d.email) + '" style="color:#0b7a4b">' + texto(d.email) + '</a>' +
          copiavel(texto(d.email))
        : '—',
      texto(d.email) || '—'],
    ['Pagamento', texto(d.pagamento) || '—', texto(d.pagamento) || '—'],
    ['Origem', texto(d.origem) || 'site', texto(d.origem) || 'site'],
    ['Data', quando, quando]
  ];
  if (texto(d.observacoes)) linhas.push(['Observações', texto(d.observacoes), texto(d.observacoes)]);

  var celulas = linhas.map(function (l, i) {
    var fundo = i % 2 ? '#f7faf8' : '#ffffff';
    return '<tr>' +
      '<td style="padding:11px 14px;background:' + fundo + ';border:1px solid #e3ebe6;' +
      'color:#5b6b63;font-size:14px;width:34%">' + l[0] + '</td>' +
      '<td style="padding:11px 14px;background:' + fundo + ';border:1px solid #e3ebe6;' +
      'color:#12211a;font-size:14px;font-weight:600">' + l[1] + '</td></tr>';
  }).join('');

  var botao = digitos
    ? '<a href="https://wa.me/' + digitos + '" style="display:inline-block;margin-top:22px;' +
      'padding:13px 24px;border-radius:8px;background:#17b47c;color:#ffffff;' +
      'font-weight:700;font-size:15px;text-decoration:none">Falar com o cliente no WhatsApp</a>'
    : '';

  var html =
    '<div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:0 auto;padding:8px">' +
      '<h2 style="color:#0b7a4b;font-size:21px;margin:0 0 6px">🛒 Novo pedido — ' + MARCA + '</h2>' +
      '<p style="color:#5b6b63;font-size:14px;margin:0 0 18px">' +
        'Recebido pelo popup de pedido do site.</p>' +
      '<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;width:100%">' +
        celulas +
      '</table>' +
      botao +
      '<p style="color:#8a9a92;font-size:12px;margin:22px 0 0">' +
        '<a href="https://docs.google.com/spreadsheets/d/' + SHEET_ID + '" ' +
        'style="color:#8a9a92">Abrir a planilha de pedidos</a></p>' +
    '</div>';

  var textoSimples = linhas.map(function (l) { return l[0] + ': ' + l[2]; }).join('\n') +
    (digitos ? '\n\nWhatsApp: https://wa.me/' + digitos : '');

  MailApp.sendEmail({
    to: NOTIFICAR,
    subject: '🛒 Novo pedido — ' + MARCA + ' — ' + texto(d.plano) + ' (' + moeda(d.total) + ')',
    body: textoSimples,
    htmlBody: html
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
  Logger.log('Resposta: %s', resposta.getContent());
  Logger.log('Planilha: https://docs.google.com/spreadsheets/d/%s', SHEET_ID);
  Logger.log('E-mails restantes hoje: %s', MailApp.getRemainingDailyQuota());
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
    var destino = garantirAba(false);
    Logger.log('Aba de destino: "%s"', destino.getName());
    var largura = Math.max(destino.getLastColumn(), 1);
    Logger.log('Cabeçalhos: %s', destino.getRange(1, 1, 1, largura).getValues()[0].join(' | '));
    Logger.log('Linhas já preenchidas: %s', destino.getLastRow() - 1);
    Logger.log('E-mail de aviso: %s', NOTIFICAR);
    Logger.log('Cota de e-mails restante hoje: %s', MailApp.getRemainingDailyQuota());
  } catch (erro) {
    Logger.log('ERRO ao abrir a planilha: %s', erro);
    Logger.log('Confira se o SHEET_ID está certo e se esta conta tem acesso ao documento.');
  }
}

/**
 * Mostra a URL real do App da Web deste projeto, direto da fonte.
 * Execute e compare com a URL colada em config.js — se forem diferentes,
 * o site está enviando os pedidos para um endereço que não existe mais.
 */
function mostrarUrl() {
  var servico = ScriptApp.getService();
  Logger.log('App da Web ativo? %s', servico.isEnabled() ? 'SIM' : 'NÃO — nunca foi implantado');
  Logger.log('URL real: %s', servico.getUrl());
  Logger.log('ID do script: %s', ScriptApp.getScriptId());
}
