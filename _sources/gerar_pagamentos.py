#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera assets/js/pagamentos.js com os logotipos das formas de pagamento.

Os traçados vêm do conjunto Simple Icons (mesma origem dos logotipos de
aparelhos). As marcas pertencem aos seus titulares e aparecem apenas para
indicar a forma de pagamento aceita.

Para atualizar ou acrescentar uma marca, coloque o SVG em
_sources/marcas-pagamento/<slug>.svg e rode este script.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ORIGEM = Path(__file__).resolve().parent / "marcas-pagamento"

# nome exibido -> (arquivo(s) svg, cor de exibição no fundo escuro)
# A cor oficial é usada quando tem contraste suficiente; quando é escura
# demais para um fundo escuro (PayPal 002991, Visa 1A1F71), usamos branco.
METODOS = {
    "Pix": (["pix.svg"], "#7fe3cf"),
    "Cartão": (["visa.svg", "mastercard.svg"], "#ffffff"),
    "Boleto": ([], "#c9dad2"),
    "PayPal": (["paypal.svg"], "#ffffff"),
    "Cripto": (["bitcoin.svg"], "#f7931a"),
}

# Boleto não tem logotipo oficial: usamos um código de barras neutro.
BOLETO = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M2 4h2v16H2zm3.5 0h1v16h-1zM8 4h2v16H8zm3.5 0h1v16h-1zM13 4h2v16h-2z'
          'm3.5 0h1v16h-1zM19 4h3v16h-3z"/></svg>')


def caminho(arquivo: str) -> str:
    svg = (ORIGEM / arquivo).read_text(encoding="utf-8")
    return re.search(r'<path\s+d="([^"]+)"', svg).group(1)


def main() -> int:
    blocos = []
    for nome, (arquivos, cor) in METODOS.items():
        if arquivos:
            svgs = "".join(
                '<svg viewBox=\\"0 0 24 24\\" fill=\\"currentColor\\" aria-hidden=\\"true\\">'
                f'<path d=\\"{caminho(a)}\\"/></svg>'
                for a in arquivos
            )
        else:
            svgs = BOLETO.replace('"', '\\"')
        blocos.append(f'  "{nome}": {{ cor: "{cor}", svg: "{svgs}" }}')

    conteudo = (
        "/* Logotipos das formas de pagamento — gerado por "
        "_sources/gerar_pagamentos.py.\n"
        "   As marcas pertencem aos seus titulares e são exibidas apenas para\n"
        "   indicar a forma de pagamento aceita. */\n"
        "window.PAGAMENTOS = {\n" + ",\n".join(blocos) + "\n};\n"
    )
    (BASE / "assets/js/pagamentos.js").write_text(conteudo, encoding="utf-8")
    print("pagamentos.js gerado:", ", ".join(METODOS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
