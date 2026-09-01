#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstrói a seção de planos (novo layout), a grade de dispositivos com as
marcas fornecidas, e remove a seção de contato do site."""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "_sources"))
from marcas import MARCAS  # noqa: E402

CHECK = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="m4 12 5 5L20 6"/></svg>')
CROSS = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2.2" stroke-linecap="round" aria-hidden="true">'
         '<path d="M6 6l12 12M18 6L6 18"/></svg>')
BOLT = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12z"/></svg>')

# Lista de itens espelhada no site de referência do cliente.
# Duas linhas foram reescritas de propósito (ver README):
#   "Netflix, Prime Video & plus" -> "Conteúdos sob demanda (VOD)"
#   "Servidor estável 100%"       -> "Servidores estáveis e monitorados"
COMUNS = [
    "Qualidade 4K · Full HD · HD",
    "Todos os canais internacionais",
    "Compatível com todos os aparelhos",
    "Guia de programação (EPG)",
    "Conteúdos sob demanda (VOD)",
    "Servidores estáveis e monitorados",
    "Suporte técnico 24/7",
    "Entrega imediata",
]

PLANOS = [
    {"key": "bronze",    "tier": "BRONZE",    "nome": "Plano Bronze",    "meses": "12 meses", "bonus": False, "adultos": False, "canais": "25 000+", "filmes": "100 000+", "badge": None,             "destaque": False},
    {"key": "gold",      "tier": "GOLD",      "nome": "Plano Gold",      "meses": "15 meses", "bonus": True,  "adultos": False, "canais": "25 000+", "filmes": "100 000+", "badge": "Mais escolhido", "destaque": True},
    {"key": "platinium", "tier": "PLATINIUM", "nome": "Plano Platinium", "meses": "15 meses", "bonus": True,  "adultos": True,  "canais": "25 000+", "filmes": "100 000+", "badge": None,             "destaque": False},
    {"key": "exclusivo", "tier": "EXCLUSIVO", "nome": "Plano Exclusivo", "meses": "24 meses", "bonus": True,  "adultos": True,  "canais": "130 000+", "filmes": "140 000+", "badge": "Melhor valor",   "destaque": False},
]


def itens(p: dict) -> list[tuple[bool, str]]:
    return [
        (p["adultos"], "Canais adultos 18+"),
        (p["bonus"], "+3 meses grátis"),
        (True, f'{p["canais"]} canais de TV'),
        (True, f'{p["filmes"]} filmes e séries'),
    ] + [(True, f) for f in COMUNS]


def card(p: dict) -> str:
    cls = "plan plan--featured" if p["destaque"] else "plan"
    badge = f'\n          <span class="plan__badge">{p["badge"]}</span>' if p["badge"] else ""
    bonus = (f'\n          <p class="plan__bonus">{CHECK}<span>+3 meses grátis</span></p>'
             if p["bonus"] else "")
    def linha(ok: bool, rotulo: str) -> str:
        classe = "" if ok else ' class="is-off"'
        marca = CHECK if ok else CROSS
        return f'            <li{classe}>{marca}<span>{rotulo}</span></li>'

    linhas = "\n".join(linha(ok, rotulo) for ok, rotulo in itens(p))

    btn = "btn--primary" if p["destaque"] else "btn--ghost"
    return f"""        <article class="{cls}" data-plan-card="{p['key']}" aria-labelledby="plano-{p['key']}">{badge}
          <p class="plan__tier">{p['tier']}</p>
          <h3 class="plan__name" id="plano-{p['key']}">{p['nome']}</h3>

          <p class="plan__price">
            <span class="plan__cur">R$</span><span class="plan__int" data-preco-int="{p['key']}">0</span><span class="plan__dec" data-preco-dec="{p['key']}">,00</span>
          </p>
          <p class="plan__duration">/ {p['meses']}</p>
{bonus}

          <div class="stepper" data-stepper="{p['key']}">
            <button class="stepper__btn" type="button" data-step="-1" aria-label="Remover uma conexão do {p['nome']}">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>
            </button>
            <span class="stepper__val">
              <b data-conn aria-live="polite">1</b>
              <span>conexões simultâneas</span>
            </span>
            <button class="stepper__btn" type="button" data-step="1" aria-label="Adicionar uma conexão ao {p['nome']}">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
            </button>
          </div>

          <ul class="plan__list">
{linhas}
          </ul>

          <button class="btn {btn} btn--full plan__cta" type="button" data-buy="{p['key']}">{BOLT}<span>Comprar agora</span></button>
        </article>"""


def marca(nome: str, rotulo: str) -> str:
    return (f'        <span class="device"><svg class="device__logo" viewBox="0 0 24 24" '
            f'aria-hidden="true"><path fill="currentColor" d="{MARCAS[nome]}"/></svg>{rotulo}</span>')


def generico(path: str, rotulo: str) -> str:
    return (f'        <span class="device"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{path}</svg>{rotulo}</span>')


TV = '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>'
BOX = '<rect x="3" y="8" width="18" height="9" rx="2.5"/><circle cx="7.5" cy="12.5" r="1"/><path d="M11 12.5h6"/>'
TABLET = '<rect x="4" y="2" width="16" height="20" rx="2.5"/><path d="M10 18.5h4"/>'

DEVICES = [
    generico(TV, "Smart TV"),
    marca("Samsung", "Samsung"),
    marca("LG", "LG"),
    marca("Sony", "Sony"),
    marca("Amazon", "Fire TV Stick"),
    marca("Android", "Android TV"),
    marca("Apple TV", "Apple TV"),
    marca("Apple", "iPhone e iPad"),
    marca("Chromecast", "Chromecast"),
    marca("Roku", "Roku"),
    marca("Xbox", "Xbox"),
    marca("Windows", "Windows"),
    marca("Linux", "Linux"),
    generico(TABLET, "Tablet"),
    generico(BOX, "TV Box Android"),
    generico(BOX, "MAG"),
]


def main() -> int:
    idx = BASE / "index.html"
    h = idx.read_text(encoding="utf-8")

    # ---- 1. Planos ----
    ini = h.index('      <div class="plans">')
    fim = h.index("      </div>\n\n      <div class=\"plans-note\">")
    h = h[:ini] + '      <div class="plans">\n' + "\n\n".join(card(p) for p in PLANOS) + "\n" + h[fim:]

    # ---- 2. Dispositivos ----
    ini = h.index('      <div class="devices">')
    fim = h.index("      </div>\n\n      <div class=\"notice\">")
    h = h[:ini] + '      <div class="devices">\n' + "\n".join(DEVICES) + "\n" + h[fim:]

    # ---- 3. Remoção da seção de contato (idempotente) ----
    marca_contato = "  <!-- ============ CONTATO ============ -->"
    if marca_contato in h:
        h = h[:h.index(marca_contato)] + h[h.index("</main>"):]

    # Links de navegação: "Contato" passa a abrir o WhatsApp
    h = h.replace('<a class="nav__link" href="#contato">Contato</a>',
                  '<a class="nav__link" href="#" data-whatsapp>Contato</a>')
    h = h.replace('<a class="mobile-nav__link" href="#contato">Contato</a>',
                  '<a class="mobile-nav__link" href="#" data-whatsapp>Contato</a>')
    h = h.replace('<li><a href="#contato">Contato</a></li>',
                  '<li><a href="#" data-whatsapp>Contato</a></li>')
    h = h.replace('"url": "https://iptv-tarefas.online/#contato"',
                  '"url": "https://iptv-tarefas.online/#planos"')
    h = h.replace('<a class="btn btn--ghost" href="#dispositivos">Conferir meu aparelho</a>',
                  '<a class="btn btn--ghost" href="#dispositivos">Conferir meu aparelho</a>')

    # ---- 4. Texto sobre conexões (agora ajustável) ----
    h = h.replace("Compare as durações disponíveis. Cada plano abaixo inclui uma conexão.",
                  "Compare as durações disponíveis. Cada plano começa com uma conexão e você "
                  "pode acrescentar conexões simultâneas no próprio card.")
    h = h.replace(
        "<strong>Uma conexão = uma única tela ao mesmo tempo.</strong> Você pode deixar a configuração "
        "salva em mais de um aparelho, mas a reprodução acontece em um aparelho por vez. Os valores são "
        "em reais e correspondem à duração indicada.",
        "<strong>Uma conexão = uma única tela ao mesmo tempo.</strong> Para assistir em mais de um "
        "aparelho simultaneamente, aumente o número de conexões no card: o valor é recalculado na hora. "
        "Os valores são em reais e correspondem à duração indicada.")
    h = h.replace(
        "Os planos exibidos incluem uma conexão e, portanto, permitem uma única tela ao mesmo tempo. "
        "Se mais pessoas querem assistir simultaneamente em aparelhos diferentes, uma conexão não "
        "atende: fale com a gente antes de contratar.",
        "Cada plano começa com uma conexão, que corresponde a uma única tela ao mesmo tempo. Se mais "
        "pessoas querem assistir ao mesmo tempo em aparelhos diferentes, aumente o número de conexões "
        "no card do plano antes de fazer o pedido.")
    velha_faq = ("Os planos exibidos incluem uma conexão. Isso corresponde a uma única tela usada ao "
                 "mesmo tempo.")
    nova_faq = ("Cada plano começa com uma conexão, ou seja, uma única tela ao mesmo tempo. Você pode "
                "acrescentar conexões simultâneas no seletor do card, e o valor é recalculado "
                "automaticamente.")
    h = h.replace(velha_faq, nova_faq)  # texto visível + JSON-LD

    idx.write_text(h, encoding="utf-8")
    print("index.html reconstruído: planos, dispositivos, contato removido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
