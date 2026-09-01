#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as 4 páginas legais a partir de um gabarito comum."""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DOMAIN = "https://iptv-tarefas.online"

SHELL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{domain}/{slug}/">
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#060d0a">
<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="IPTV Tarefas">
<meta property="og:url" content="{domain}/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="icon" href="/assets/img/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Sora:wght@700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Sora:wght@700;800&display=swap"></noscript>
<link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
<a class="skip-link" href="#conteudo">Ir para o conteúdo principal</a>

<header class="header">
  <div class="wrap header__inner">
    <a class="logo" href="/" aria-label="IPTV Tarefas — voltar para a página inicial">
      <svg class="logo__mark" width="36" height="36" viewBox="0 0 36 36" fill="none" aria-hidden="true">
        <rect x="1" y="1" width="34" height="34" rx="11" fill="url(#lgl)"/>
        <path d="M13 11.5v13l10-6.5z" fill="#04140e"/>
        <defs><linearGradient id="lgl" x1="1" y1="1" x2="35" y2="35" gradientUnits="userSpaceOnUse"><stop stop-color="#17b47c"/><stop offset="1" stop-color="#7ff0c0"/></linearGradient></defs>
      </svg>
      <span class="logo__text">IPTV Tarefas<small>Brasil</small></span>
    </a>

    <nav class="nav" aria-label="Navegação principal">
      <ul class="nav__list">
        <li><a class="nav__link" href="/">Início</a></li>
        <li><a class="nav__link" href="/#vantagens">Vantagens</a></li>
        <li><a class="nav__link" href="/#planos">Planos</a></li>
        <li><a class="nav__link" href="/#dispositivos">Dispositivos</a></li>
        <li><a class="nav__link" href="/#instalacao">Instalação</a></li>
        <li><a class="nav__link" href="/#faq">FAQ</a></li>
        <li><a class="nav__link" href="#" data-whatsapp>Contato</a></li>
      </ul>
    </nav>

    <a class="btn btn--primary btn--sm header__cta" href="/#planos">Ver os planos</a>

    <button class="burger" type="button" data-burger aria-expanded="false" aria-controls="mobile-nav">
      <span class="burger__bars" aria-hidden="true"></span>
      <span class="sr-only">Abrir ou fechar o menu de navegação</span>
    </button>
  </div>

  <div class="mobile-nav" id="mobile-nav">
    <div class="wrap">
      <ul class="mobile-nav__list">
        <li><a class="mobile-nav__link" href="/">Início</a></li>
        <li><a class="mobile-nav__link" href="/#vantagens">Vantagens</a></li>
        <li><a class="mobile-nav__link" href="/#planos">Planos</a></li>
        <li><a class="mobile-nav__link" href="/#dispositivos">Dispositivos</a></li>
        <li><a class="mobile-nav__link" href="/#instalacao">Instalação</a></li>
        <li><a class="mobile-nav__link" href="/#faq">FAQ</a></li>
        <li><a class="mobile-nav__link" href="#" data-whatsapp>Contato</a></li>
      </ul>
      <a class="btn btn--primary btn--full" href="/#planos">Ver os planos</a>
    </div>
  </div>
</header>

<main id="conteudo" class="legal">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Trilha de navegação">
      <a href="/">Início</a> <span aria-hidden="true">/</span> {h1}
    </nav>
    <h1>{h1}</h1>
    <p class="legal__updated">Última atualização: agosto de 2026</p>
    <div class="legal__body">
{body}
    </div>
  </div>
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <h2>IPTV Tarefas</h2>
        <p class="footer__desc">Compare os planos e consulte as informações para escolher uma assinatura adequada aos seus aparelhos e ao seu uso.</p>
      </div>
      <nav aria-labelledby="fnav">
        <h2 id="fnav">Navegação</h2>
        <ul class="footer__list">
          <li><a href="/">Início</a></li>
          <li><a href="/#vantagens">Vantagens</a></li>
          <li><a href="/#planos">Planos</a></li>
          <li><a href="/#dispositivos">Dispositivos</a></li>
          <li><a href="/#instalacao">Instalação</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="#" data-whatsapp>Contato</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="flegal">
        <h2 id="flegal">Informações legais</h2>
        <ul class="footer__list">
          <li><a href="/termos-de-uso/">Termos de uso</a></li>
          <li><a href="/politica-de-privacidade/">Política de privacidade</a></li>
          <li><a href="/politica-de-reembolso/">Política de reembolso</a></li>
          <li><a href="/informacoes-legais/">Informações legais</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer__bottom">
      <p>© 2026 IPTV Tarefas. Todos os direitos reservados.</p>
      <p>O usuário é responsável por respeitar a legislação aplicável.</p>
    </div>
  </div>
</footer>

<!-- Widget de WhatsApp (conteúdo e número vêm de assets/js/config.js) -->
<div class="wa" data-wa-widget>
  <div class="wa__panel" id="wa-panel" hidden>
    <div class="wa__head">
      <span class="wa__avatar" aria-hidden="true">IT</span>
      <span class="wa__id">
        <b>Suporte IPTV Tarefas</b>
        <span>Normalmente responde em minutos</span>
      </span>
      <button class="wa__close" type="button" data-wa-close aria-label="Fechar a janela de conversa">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>

    <div class="wa__body">
      <div class="wa__bubble">
        <p>Olá! 👋 Posso ajudar a <strong>escolher um plano</strong>, <strong>configurar o seu aparelho</strong> ou tirar dúvidas sobre um pedido em andamento. É só mandar uma mensagem.</p>
      </div>

      <a class="wa__cta" href="#" data-wa-start target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.174.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.83 9.83 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.82 11.82 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.88 11.88 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.82 11.82 0 0 0 20.464 3.488"/></svg>
        <span>Iniciar conversa</span>
      </a>

      <p class="wa__note">Você será redirecionado para o WhatsApp.<br><span data-wa-number></span></p>
    </div>
  </div>

  <button class="wa__fab" type="button" data-wa-toggle aria-expanded="false" aria-controls="wa-panel">
    <svg class="wa__icon-chat" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.174.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.83 9.83 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.82 11.82 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.88 11.88 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.82 11.82 0 0 0 20.464 3.488"/></svg>
    <svg class="wa__icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    <span class="sr-only">Abrir ou fechar a janela de conversa no WhatsApp</span>
  </button>
</div>

<script src="/assets/js/config.js" defer></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

TODO = '<span class="legal__todo">[A COMPLETAR]</span>'

PAGES = [
    {
        "slug": "informacoes-legais",
        "title": "Informações legais | IPTV Tarefas",
        "desc": "Informações legais do site IPTV Tarefas: identificação do responsável, hospedagem, propriedade intelectual e limites de responsabilidade.",
        "h1": "Informações legais",
        "body": f"""
      <p>Estas informações se aplicam ao site&nbsp;<strong>{DOMAIN}</strong>, operado sob o nome «&nbsp;IPTV Tarefas&nbsp;».</p>

      <h2>Responsável pelo site</h2>
      <ul>
        <li>Nome ou razão social: {TODO}</li>
        <li>CNPJ ou CPF do responsável: {TODO}</li>
        <li>Endereço: {TODO}</li>
        <li>E-mail de atendimento (SAC): {TODO}</li>
        <li>Telefone de atendimento: {TODO}</li>
      </ul>
      <p>O Código de Defesa do Consumidor e o Decreto nº 7.962/2013 exigem que esses dados de identificação estejam visíveis em site de comércio eletrônico. Preencha os campos acima antes de colocar o site no ar.</p>

      <h2>Hospedagem</h2>
      <p>O site é hospedado na plataforma Vercel. Dados completos do provedor de hospedagem (razão social, endereço e contato): {TODO}</p>

      <h2>Propriedade intelectual</h2>
      <p>A estrutura do site, a identidade visual, os textos e os elementos de interface são protegidos pela legislação de propriedade intelectual. Reprodução total ou parcial sem autorização prévia por escrito é proibida.</p>
      <p>Marcas, nomes de produtos e nomes de aparelhos citados no site aparecem apenas a título informativo, para indicar compatibilidade técnica. Pertencem aos seus respectivos titulares e a menção não implica parceria, afiliação ou aprovação.</p>

      <h2>Responsabilidade</h2>
      <p>As informações publicadas têm caráter indicativo. As recomendações de velocidade, compatibilidade e configuração são gerais: o desempenho real depende da conexão de internet, do equipamento, do aplicativo utilizado e da qualidade da fonte do sinal. Não constituem garantia de resultado.</p>
      <p>Não nos responsabilizamos por danos decorrentes de uso indevido do serviço, de incompatibilidade de equipamento ou de interrupções ligadas à rede do usuário.</p>

      <h2>Direitos de transmissão</h2>
      <p>A tecnologia IPTV é lícita em si mesma. A transmissão ou a consulta de conteúdos protegidos sem autorização dos titulares dos direitos pode configurar infração, nos termos da Lei nº 9.610/1998. O usuário se compromete a respeitar a legislação aplicável e os direitos dos titulares de conteúdo.</p>

      <h2>Links externos</h2>
      <p>O site pode remeter a aplicativos ou recursos de terceiros. Não exercemos controle sobre esses recursos e não respondemos pelo seu conteúdo nem pelas suas condições de uso.</p>

      <h2>Legislação aplicável</h2>
      <p>Estas informações são regidas pela legislação brasileira. Fica eleito o foro do domicílio do consumidor para dirimir eventuais controvérsias, conforme o Código de Defesa do Consumidor.</p>
"""
    },
    {
        "slug": "termos-de-uso",
        "title": "Termos de uso | IPTV Tarefas",
        "desc": "Termos de uso do site e das assinaturas IPTV Tarefas: pedido, duração, conexões, requisitos técnicos e obrigações do usuário.",
        "h1": "Termos de uso",
        "body": f"""
      <p>Estes termos regem o uso do site&nbsp;<strong>{DOMAIN}</strong> e das assinaturas nele apresentadas. Ao fazer um pedido, o usuário declara ter lido e aceito estas condições.</p>

      <h2>1. Objeto</h2>
      <p>O site apresenta planos de assinatura de televisão por protocolo de internet (IPTV), suas durações, seus preços e as condições técnicas de uso. Também traz informações sobre compatibilidade de aparelhos e instalação.</p>

      <h2>2. Planos e preços</h2>
      <p>Os planos apresentados são: Plano Bronze por <span data-preco="bronze">R$ 00,00</span> (12 meses), Plano Gold por <span data-preco="gold">R$ 00,00</span> (15 meses), Plano Platinium por <span data-preco="platinium">R$ 00,00</span> (15 meses) e Plano Exclusivo por <span data-preco="exclusivo">R$ 00,00</span> (24 meses). Os planos Gold, Platinium e Exclusivo incluem 3 meses grátis. Os valores são em reais e correspondem à duração indicada.</p>
      <p>Os preços podem ser alterados a qualquer momento para pedidos futuros. Vale o preço exibido no momento da confirmação do pedido.</p>

      <h2>3. Número de conexões</h2>
      <p>Cada plano é apresentado com <strong>uma conexão</strong>, ou seja, uma única tela reproduzindo ao mesmo tempo. É possível contratar conexões simultâneas adicionais pelo seletor do card do plano, com acréscimo no valor. A configuração pode ficar salva em mais de um aparelho, mas o número de telas simultâneas é limitado ao de conexões contratadas. Uso além desse limite pode acarretar a suspensão do acesso.</p>

      <h2>4. Pedido</h2>
      <p>O pedido é feito após contato pelo WhatsApp, a partir do botão de compra do plano escolhido. Nenhum dado bancário ou de cartão é digitado ou tratado neste site. As informações necessárias à configuração são enviadas após a confirmação do pedido.</p>

      <h2>5. Requisitos técnicos</h2>
      <p>O uso do serviço pressupõe conexão de internet suficiente, aparelho compatível e aplicativo de reprodução disponível para esse aparelho. O aplicativo e a assinatura são serviços distintos: alguns aplicativos cobram a própria taxa de ativação, independente do preço da assinatura.</p>
      <p>As velocidades recomendadas são de 5 a 10 Mbps para HD, de 10 a 15 Mbps para Full HD e 25 Mbps ou mais para 4K. Esses valores são indicativos e não constituem garantia de desempenho.</p>

      <h2>6. Obrigações do usuário</h2>
      <ul>
        <li>Fornecer informações corretas no momento do pedido.</li>
        <li>Não compartilhar, revender ou redistribuir seus dados de acesso ou sua configuração.</li>
        <li>Usar o serviço em âmbito privado e pessoal.</li>
        <li>Respeitar a legislação aplicável e os direitos dos titulares de conteúdo.</li>
        <li>Não tentar contornar medidas técnicas de proteção ou de controle de acesso.</li>
      </ul>

      <h2>7. Disponibilidade do serviço</h2>
      <p>Podem ocorrer interrupções por manutenção, atualização, saturação da rede ou causas alheias à nossa vontade. Não são garantidas disponibilidade permanente, estabilidade absoluta nem qualidade 4K contínua em todos os conteúdos.</p>

      <h2>8. Suspensão e rescisão</h2>
      <p>O acesso pode ser suspenso, sem reembolso, em caso de uso fraudulento, compartilhamento não autorizado, tentativa de contorno técnico ou descumprimento destes termos.</p>

      <h2>9. Suporte</h2>
      <p>Oferecemos suporte para a escolha de um aplicativo compatível e para a configuração do aparelho. O suporte não cobre reparo de equipamento nem a qualidade da conexão de internet do usuário.</p>

      <h2>10. Alteração dos termos</h2>
      <p>Estes termos podem ser atualizados. Vale a versão publicada nesta página na data do pedido.</p>

      <h2>11. Contato e legislação aplicável</h2>
      <p>Dúvidas sobre estes termos podem ser enviadas pelo <a href="#" data-whatsapp>nosso WhatsApp</a>. Dados do responsável: {TODO}. Estes termos são regidos pela legislação brasileira, incluindo o Código de Defesa do Consumidor.</p>
"""
    },
    {
        "slug": "politica-de-privacidade",
        "title": "Política de privacidade | IPTV Tarefas",
        "desc": "Política de privacidade do IPTV Tarefas conforme a LGPD: dados tratados, finalidades, prazos de guarda e direitos do titular.",
        "h1": "Política de privacidade",
        "body": f"""
      <p>Esta política explica quais dados são tratados quando você usa o site&nbsp;<strong>{DOMAIN}</strong>, conforme a Lei Geral de Proteção de Dados (Lei nº 13.709/2018 – LGPD).</p>

      <h2>Controlador dos dados</h2>
      <p>Controlador: {TODO}. Contato para assuntos de proteção de dados (encarregado/DPO): {TODO}</p>

      <h2>Dados tratados</h2>
      <p>Ao clicar em «&nbsp;Comprar agora&nbsp;», abre-se uma janela de pedido no próprio navegador, onde você informa nome, telefone, e-mail e a forma de pagamento preferida. Ao confirmar, esses dados são usados de duas maneiras: preenchem previamente uma mensagem de WhatsApp com o resumo do pedido, que só é enviada se você quiser, e são registrados em uma planilha do Google Sheets sob nosso controle, para que possamos atender e acompanhar o pedido.</p>
      <p>Nenhum dado de pagamento — número de cartão, senha ou dados bancários — é solicitado ou tratado neste site em momento algum.</p>
      <ul>
        <li><strong>Dados de identificação</strong>: nome e demais informações que você mesmo informar na janela de pedido ou na conversa de WhatsApp.</li>
        <li><strong>Dados do pedido</strong>: plano, duração, número de conexões, aparelho utilizado e forma de pagamento preferida.</li>
        <li><strong>Registro do pedido</strong>: os dados acima, mais a data e a hora, uma referência interna do pedido e o domínio de origem, gravados em planilha do Google Sheets. Um aviso por e-mail com o mesmo conteúdo é enviado à nossa equipe.</li>
        <li><strong>Dados técnicos</strong>: registros de conexão gerados pelo provedor de hospedagem (endereço IP, data e hora da requisição, tipo de navegador), para segurança e funcionamento. O Marco Civil da Internet (Lei nº 12.965/2014) prevê a guarda de registros de acesso a aplicações por seis meses.</li>
      </ul>

      <h2>Finalidades e bases legais</h2>
      <ul>
        <li>Responder às suas solicitações e processar um pedido: execução de contrato e procedimentos preliminares (art. 7º, V, LGPD).</li>
        <li>Garantir funcionamento e segurança do site: legítimo interesse (art. 7º, IX).</li>
        <li>Cumprir obrigações legais e regulatórias: art. 7º, II.</li>
      </ul>

      <h2>Aplicativo de mensagens de terceiros</h2>
      <p>A conversa pelo WhatsApp também fica sujeita à política de privacidade do provedor desse aplicativo, sobre a qual não temos controle.</p>

      <h2>Cookies e medição de audiência</h2>
      <p>Este site não instala cookies publicitários e não usa ferramentas de rastreamento comportamental. As fontes tipográficas são carregadas de um serviço de terceiros (Google Fonts), que pode receber o seu endereço IP para entregar os arquivos. Se uma ferramenta de medição de audiência for adicionada no futuro, esta página será atualizada e o consentimento será solicitado quando a legislação exigir.</p>

      <h2>Compartilhamento</h2>
      <p>Seus dados não são vendidos nem alugados. Podem ser tratados por prestadores de serviço atuando por nossa conta e apenas no necessário para a sua função: a hospedagem do site, o Google (Google Sheets, Google Apps Script e e-mail, onde o pedido fica registrado) e o aplicativo de mensagens usado no atendimento.</p>

      <h2>Prazo de guarda</h2>
      <p>Os pedidos registrados na planilha são mantidos enquanto durar a assinatura contratada e, depois, pelo prazo exigido pelas obrigações legais aplicáveis, sobretudo as fiscais e contábeis. As trocas de mensagens ligadas a uma solicitação seguem o mesmo critério. Os registros técnicos seguem a política do provedor de hospedagem e o prazo legal. Você pode pedir a eliminação dos seus dados a qualquer momento, ressalvado o que a lei nos obrigue a conservar.</p>

      <h2>Transferência internacional</h2>
      <p>O Google e o provedor de hospedagem tratam dados em servidores fora do Brasil, o que implica transferência internacional. Essas transferências seguem as hipóteses e garantias previstas nos artigos 33 a 36 da LGPD, incluindo as cláusulas contratuais adotadas por esses fornecedores.</p>

      <h2>Seus direitos</h2>
      <p>Você pode solicitar confirmação de tratamento, acesso, correção, anonimização, bloqueio ou eliminação de dados, portabilidade, informação sobre compartilhamentos e revogação do consentimento, nos termos do art. 18 da LGPD. Para exercer esses direitos, escreva para o contato indicado acima. Você também pode apresentar reclamação à Autoridade Nacional de Proteção de Dados (ANPD).</p>

      <h2>Segurança</h2>
      <p>O site é servido em HTTPS. Adotamos medidas técnicas e organizacionais razoáveis para proteger as informações trocadas.</p>

      <h2>Atualização</h2>
      <p>Esta política pode ser alterada para refletir mudanças técnicas ou regulatórias. A data da última atualização consta no topo da página.</p>
"""
    },
    {
        "slug": "politica-de-reembolso",
        "title": "Política de reembolso | IPTV Tarefas",
        "desc": "Política de reembolso do IPTV Tarefas: direito de arrependimento de 7 dias, casos cobertos, casos excluídos, prazos e procedimento.",
        "h1": "Política de reembolso",
        "body": f"""
      <p>Esta página descreve as condições em que um pedido de reembolso pode ser analisado para as assinaturas apresentadas em&nbsp;<strong>{DOMAIN}</strong>.</p>

      <h2>Natureza do serviço</h2>
      <p>Uma assinatura IPTV é um conteúdo digital fornecido sem suporte físico. A disponibilização é imediata assim que os dados de configuração são enviados.</p>

      <h2>Direito de arrependimento (7 dias)</h2>
      <p>Nas compras feitas fora do estabelecimento comercial, incluindo pela internet, o artigo 49 do Código de Defesa do Consumidor garante o direito de desistir da contratação no prazo de 7 dias corridos, contados da contratação ou do recebimento do serviço. Exercido esse direito dentro do prazo, os valores pagos são devolvidos, monetariamente atualizados.</p>
      <p>Se o serviço já tiver sido utilizado durante esse período, poderá ser considerada a proporção efetivamente usufruída na apuração do valor a devolver. Em caso de divergência, prevalece a interpretação mais favorável ao consumidor.</p>

      <h2>Outras situações que podem gerar reembolso</h2>
      <ul>
        <li>O serviço nunca foi ativado e nenhum dado de configuração foi enviado.</li>
        <li>Um problema técnico persistente é de nossa responsabilidade e não foi resolvido após as tentativas de suporte.</li>
        <li>Erro de cobrança ou pagamento em duplicidade.</li>
      </ul>

      <h2>Situações não cobertas</h2>
      <ul>
        <li>Conexão de internet insuficiente, Wi-Fi instável ou equipamento incompatível.</li>
        <li>Aparelho sem aplicativo de reprodução compatível disponível.</li>
        <li>Indisponibilidade pontual de um conteúdo, de uma categoria ou de uma fonte de terceiros.</li>
        <li>Compartilhamento de acessos, revenda ou uso em desacordo com os termos de uso.</li>
        <li>Recusa em participar das verificações técnicas necessárias ao diagnóstico.</li>
      </ul>
      <p>Nenhuma cláusula desta política afasta os direitos assegurados ao consumidor pelo Código de Defesa do Consumidor, inclusive quanto a vício ou defeito do serviço (artigo 20).</p>

      <h2>Como solicitar</h2>
      <ol>
        <li>Entre em contato pelo <a href="#" data-whatsapp>nosso WhatsApp</a> descrevendo o problema com precisão.</li>
        <li>Informe o aparelho, o aplicativo de reprodução e o tipo de conexão.</li>
        <li>Siga as etapas de diagnóstico propostas: a maior parte das dificuldades se resolve com reconfiguração ou troca de aplicativo.</li>
        <li>Se não houver solução, o pedido de reembolso é analisado.</li>
      </ol>

      <h2>Prazos</h2>
      <p>Quando o reembolso é concedido, ele é feito pelo mesmo meio de pagamento usado na compra, salvo acordo em contrário. O prazo de crédito também depende da instituição financeira ou do meio de pagamento utilizado.</p>

      <h2>Reembolso proporcional</h2>
      <p>Quando parte do período de assinatura já foi utilizada, pode ser proposto o reembolso proporcional ao tempo restante.</p>

      <h2>Contato</h2>
      <p>Dúvidas sobre esta política pelo <a href="#" data-whatsapp>nosso WhatsApp</a>. Dados do responsável: {TODO}</p>
"""
    },
]

for page in PAGES:
    out = BASE / page["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        SHELL.format(title=page["title"], desc=page["desc"], slug=page["slug"],
                     h1=page["h1"], body=page["body"].rstrip(), domain=DOMAIN),
        encoding="utf-8",
    )
    print("escrito:", out)
