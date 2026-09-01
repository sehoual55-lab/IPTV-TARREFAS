# IPTV Tarefas — site estático (pt-BR)

Site HTML/CSS/JS estático, sem build e sem dependências, pronto para a Vercel.

## Deploy na Vercel

Publique a pasta como está (framework preset: **Other**, sem comando de build,
output directory: a raiz do projeto). O `vercel.json` cuida das URLs limpas,
do `trailingSlash` e dos cabeçalhos de cache e segurança.

Domínio canônico configurado nos metadados: `https://iptv-tarefas.online`

## ANTES DE PUBLICAR — 2 itens obrigatórios

1. **Preços — CONFERIR.** Os valores atuais (R$ 239,90 / 299,90 / 359,90 / 509,90)
   são apenas a conversão dos seus preços franceses (39,99 / 49,99 / 59,99 / 84,99 €)
   pela cotação de 29/08/2026, cerca de R$ 6,01 por euro. **Não são preços de
   mercado brasileiros** — uma conversão direta ignora o poder de compra local, e
   no Brasil o IPTV costuma ser vendido bem abaixo disso. Ajuste com:

   ```bash
   python3 _sources/definir_precos.py 149,90 189,90 229,90 299,90
   #                                  bronze  gold    platinium exclusivo
   ```

   O script propaga os valores para os cards, a resposta do FAQ, os termos de uso,
   o JSON-LD (`Offer.price`) e o `config.js`.
   Nunca edite o preço em um lugar só: o schema fica dessincronizado.

2. **Páginas legais.** Cada bloco `[A COMPLETAR]` é uma informação exigida pelo
   Decreto nº 7.962/2013 e pelo CDC: razão social, CNPJ, endereço, e-mail de SAC,
   telefone, dados do hospedeiro e do encarregado (DPO) da LGPD.

## Contato e pedido

Não há formulário no site. O botão **Comprar agora** de cada plano abre o WhatsApp
com o resumo já preenchido (plano, duração e número de conexões escolhido).
O link «Contato» do menu e do rodapé abre o mesmo WhatsApp.

`assets/js/config.js` — WhatsApp `447412836986` (+44 7412 836986). String vazia
esconde os links de contato. Nenhum campo de cartão existe no site.

## Conexões simultâneas

Cada card tem um seletor − / + (1 a 5 conexões) que recalcula o preço na hora.
Em `config.js`:

```js
conexoes: { max: 5, multiplicadores: [1.00, 1.70, 2.35, 2.95, 3.50] }
```

`multiplicadores[n-1]` multiplica o preço base para n conexões — a grade acima é a
usada nos outros sites do portfólio (−30 / −35 / −40 / −45 % por conexão adicional).
**Confirme se é a sua tabela para o Brasil** antes de publicar.

## Lista de itens dos planos

Os cards reproduzem a lista do seu site de referência (canais adultos 18+,
+3 meses grátis, contagem de canais e filmes, canais internacionais,
compatibilidade, EPG, VOD, servidores, suporte 24/7, entrega imediata).
Ela é gerada por `_sources/reconstruir_planos.py` (constantes `COMUNS` e `PLANOS`).

Duas linhas foram reescritas de propósito:

| Site de referência | Aqui | Motivo |
|---|---|---|
| Netflix, Prime Video & plus | Conteúdos sob demanda (VOD) | Anunciar serviços licenciados por nome equivale a declarar redistribuição de conteúdo de terceiros |
| Servidor estável 100% | Servidores estáveis e monitorados | Garantia absoluta, contradita pelo próprio aviso da seção de confiabilidade |

## SEO

Foco comercial: *assinatura IPTV*, *IPTV Brasil*, *lista IPTV*, *melhor IPTV*,
*IPTV 4K*, *IPTV Smart TV*, *IPTV Fire TV Stick*, *servidor IPTV*.

O site **não** é otimizado para «iptv tarefas» / «cmsp». Essa consulta pertence
ao Centro de Mídias da Educação de São Paulo (cmspweb.ip.tv), plataforma escolar
encerrada em dezembro de 2024: o público é de estudantes procurando lição de
casa, não de compradores.

## Estrutura

```
index.html                        página única (todas as seções)
termos-de-uso/                    \
politica-de-privacidade/           > páginas legais (noindex)
politica-de-reembolso/            /
informacoes-legais/               /
assets/css/styles.css             design system completo
assets/js/config.js               preços, WhatsApp, e-mail
assets/js/main.js                 menu, FAQ, seleção de plano, formulário
assets/img/                       ícones + imagem Open Graph 1200×630
  favicon.svg / favicon.ico       aba do navegador (SVG moderno, ICO de reserva)
  apple-touch-icon.png            180×180, tela de início do iOS
  favicon-32.png / icon-512.png   PNG para o manifesto
site.webmanifest                  nome, cores e ícones do app instalado
assets/img/marcas/                12 logotipos de marca (Samsung, LG, Sony, Amazon,
                                  Android, Apple, Apple TV, Roku, Xbox, Chromecast,
                                  Windows, Linux) — uso apenas para indicar compatibilidade
robots.txt · sitemap.xml · vercel.json
_sources/definir_precos.py        propaga os preços por todo o site
_sources/reconstruir_planos.py    regenera os cards de plano e a grade de dispositivos
_sources/guias_instalacao.py      regenera os 7 guias de instalação
_sources/marcas.py                caminhos SVG das 12 marcas fornecidas
_sources/gerar_paginas_legais.py  regenera as 4 páginas legais
_sources/verificar.py             confere links, âncoras, preços, JSON-LD, metadados
```

## Guias de instalação por aparelho

Dentro da seção `#instalacao`: um seletor personalizado (padrão ARIA `listbox`,
com os logotipos das marcas, marca de seleção e navegação por teclado — setas,
Home, End, Enter, Escape) troca entre 7 guias — Samsung/LG, Fire TV Stick/Android TV,
Android/Tablet, iPhone/iPad, Windows/macOS, Formuler Z e MAG Box.
Todos os passos ficam no HTML, então são indexáveis.

Editar em `_sources/guias_instalacao.py` (lista `GUIAS`) e rodar:

```bash
python3 _sources/guias_instalacao.py
```

Os logotipos vêm de `_sources/marcas.py` (os mesmos SVGs usados na grade de
dispositivos): Samsung + LG, Amazon + Android, Android, Apple, Windows + Apple.
Formuler Z e MAG Box não têm logotipo no conjunto, então usam um ícone neutro.

O script é idempotente: pode ser executado quantas vezes quiser.

## Popup de pedido

O botão «Comprar agora» abre uma janela em duas colunas:

- **Esquerda — resumo**: plano, duração, bônus, seletor de conexões, linha de
  conexões adicionais, total em destaque e a nota do art. 49 do CDC.
- **Direita — dados**: plano (dá para trocar de pacote ali mesmo), nome completo
  (obrigatório), telefone com **seletor de país buscável** (82 países, busca por
  nome, sigla ou código), e-mail e forma de pagamento preferida.

«Finalizar pedido» valida os obrigatórios, abre o WhatsApp com o resumo e mostra
o **popup de confirmação** com o recibo do pedido e um link para reabrir o
WhatsApp caso o navegador tenha bloqueado o pop-up.

Fecham pelo X, por Escape ou clicando no fundo; o foco fica preso dentro da janela.
**Nenhum campo de cartão ou dado de pagamento existe no site** — a forma de
pagamento é apenas uma preferência informada, editável em `config.js`:

```js
formasPagamento: ["Cartão", "PayPal"]   // opções prontas: Pix, Cartão, Boleto, PayPal, Cripto
```

Lista vazia esconde o bloco. A lista de países fica em `assets/js/paises.js`.

Os logotipos das formas de pagamento ficam em `assets/js/pagamentos.js`, gerado por:

```bash
python3 _sources/gerar_pagamentos.py
```

Os traçados vêm do conjunto Simple Icons (mesma origem dos logotipos de aparelhos);
os SVGs de origem estão em `_sources/marcas-pagamento/`. Para trocar uma marca,
substitua o SVG lá e rode o script. Boleto não tem logotipo oficial: usa um
código de barras neutro. As marcas pertencem aos seus titulares e aparecem apenas
para indicar a forma de pagamento aceita.

## Registro dos pedidos no Google Sheets (opcional)

`_sources/apps-script/Codigo.gs` é o backend em Google Apps Script que grava cada
pedido na planilha e manda um e-mail de aviso para xyz905391@gmail.com
(constante `NOTIFICAR` no topo do arquivo).

1. script.google.com → Novo projeto → cole o `Codigo.gs`
2. Execute `setup()` uma vez (cria a aba «Pedidos», cabeçalho, formatos e o
   menu suspenso de Status)
3. Implantar → App da Web → executar como **Eu**, acesso **Qualquer pessoa**
4. Cole a URL `/exec` em `pedidosEndpoint` e repita o mesmo `TOKEN` em
   `pedidosToken`, ambos no `config.js`

O endpoint já está preenchido no `config.js`. Com `pedidosEndpoint: ""` nada é
enviado e o pedido segue apenas pelo WhatsApp. O envio é feito em paralelo: se a planilha estiver fora do ar, o
pedido continua chegando pelo WhatsApp normalmente.

> **TOKEN:** o valor `troque-este-valor` está tanto no `Codigo.gs` quanto no
> `config.js`. Ele é público (qualquer visitante lê o `config.js`), então serve
> só para barrar robôs que descubram a URL — não é segredo. Troque-o nos dois
> arquivos por um valor seu e crie uma nova versão de implantação.
>
> **Privacidade:** com o endpoint ativo, a política de privacidade já foi
> reescrita para declarar o registro em planilha do Google, a finalidade, o prazo
> de guarda e a transferência internacional, como exige a LGPD.

## Widget de WhatsApp

Presente nas 5 páginas. O botão flutuante abre um painel com avatar, título,
mensagem de saudação, botão «Iniciar conversa» e o número escrito por extenso.
Fecha pelo X, pela tecla Escape ou clicando fora.

Em `config.js`:

```js
whatsapp: "447412836986",                  // número técnico, sem "+" nem espaços
whatsappExibicao: "+44 7412 836986",       // como aparece escrito no painel
mensagemInicial: "Olá! Vim pelo site…"     // texto já preenchido no WhatsApp
```

Se `whatsapp` ficar vazio, o widget e os links «Contato» são removidos
automaticamente pelo `main.js` — nenhum link quebrado fica na página.

O texto do painel (título, saudação) está no HTML, gerado por
`_sources/gerar_paginas_legais.py` para as páginas legais e escrito
diretamente em `index.html`.

## Verificação

```bash
python3 _sources/verificar.py
```
