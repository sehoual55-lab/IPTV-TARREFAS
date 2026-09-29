/* ==========================================================================
   IPTV Tarefas — configuração editável
   Altere apenas este arquivo para mudar preços ou contato.
   Depois de mudar os preços aqui, rode:  python3 _sources/definir_precos.py
   para propagar os valores no HTML, no FAQ e no JSON-LD.
   ========================================================================== */

window.SITE_CONFIG = {
  brand: "IPTV Tarefas",
  domain: "https://iptv-tarefas.online",

  /* Número de WhatsApp em formato internacional, sem "+" nem espaços.
     Deixe "" para esconder o botão de WhatsApp. */
  whatsapp: "447412836986",

  /* Número como ele aparece escrito no widget. */
  whatsappExibicao: "+44 7412 836986",

  /* Registro dos pedidos no Google Sheets (opcional).
     Cole aqui a URL /exec do App da Web e repita o mesmo TOKEN do Codigo.gs.
     Com o endpoint vazio, nada é enviado: o pedido segue apenas pelo WhatsApp. */
  pedidosEndpoint: "https://script.google.com/macros/s/AKfycbydpkanlBRK3Jlv2trb67rZSVd5J1IhObJ9nTCaSmX0plUsyrPeqc07uBkHWnbqJaf_YA/exec",
  pedidosToken: "troque-este-valor",

  /* Formas de pagamento oferecidas. É apenas uma preferência informada no
     pedido: nenhum pagamento é processado no site. Liste vazia = bloco escondido. */
  formasPagamento: ["Cartão"],

  /* Mensagem já preenchida ao clicar em "Iniciar conversa". */
  mensagemInicial: "Olá! Vim pelo site e gostaria de informações sobre os planos de IPTV.",

  /* E-mail de contato. Deixe "" enquanto não estiver definido. */
  email: "",

  /* Conexões simultâneas.
     "max" = número máximo de conexões no seletor de cada card.
     "multiplicadores[n-1]" = fator aplicado ao preço base para n conexões.
     Os valores abaixo reproduzem a grade usada nos outros sites do portfólio
     (−30 / −35 / −40 / −45 % por conexão adicional). Ajuste se a sua tabela for outra. */
  conexoes: {
    max: 5,
    multiplicadores: [1.00, 1.70, 2.35, 2.95, 3.50]
  },

  /* Planos — os preços ainda estão zerados: rode _sources/definir_precos.py */
  plans: {
    bronze:    { name: "Plano Bronze",    price: "R$ 239,90", duration: "12 meses", bonus: false },
    gold:      { name: "Plano Gold",      price: "R$ 299,90", duration: "15 meses", bonus: true },
    platinium: { name: "Plano Platinium", price: "R$ 359,90", duration: "15 meses", bonus: true },
    exclusivo: { name: "Plano Exclusivo", price: "R$ 509,90", duration: "24 meses", bonus: true }
  }
};
