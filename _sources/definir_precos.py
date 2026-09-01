#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define os preços dos 4 planos em todo o site, a partir de uma única fonte.

Uso:
    python3 _sources/definir_precos.py 149,90 189,90 229,90 299,90
    (ordem: bronze gold platinium exclusivo)

Ou sem argumentos: lê os valores já presentes em assets/js/config.js.

Atualiza: os cards de preço, a resposta do FAQ, o JSON-LD (ItemList/Offer),
a página de termos de uso e o próprio config.js.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CHAVES = ["bronze", "gold", "platinium", "exclusivo"]
NOMES = {"bronze": "Plano Bronze", "gold": "Plano Gold",
         "platinium": "Plano Platinium", "exclusivo": "Plano Exclusivo"}
DURACOES = {"bronze": "12 meses", "gold": "15 meses",
            "platinium": "15 meses", "exclusivo": "24 meses"}


def normalizar(valor: str) -> tuple[str, str]:
    """'149,90' ou 'R$ 149,90' ou '149.90' -> ('R$ 149,90', '149.90')"""
    limpo = valor.replace("R$", "").replace(" ", "").replace("\u00a0", "").strip()
    limpo = limpo.replace(".", ",") if limpo.count(",") == 0 and limpo.count(".") == 1 else limpo
    limpo = limpo.replace(".", "")
    if "," not in limpo:
        limpo += ",00"
    inteiro, _, centavos = limpo.partition(",")
    centavos = (centavos + "00")[:2]
    return f"R$ {inteiro},{centavos}", f"{inteiro}.{centavos}"


def ler_config() -> dict:
    txt = (BASE / "assets/js/config.js").read_text(encoding="utf-8")
    return {k: re.search(rf'{k}:\s*{{[^}}]*price:\s*"([^"]+)"', txt).group(1) for k in CHAVES}


def main() -> int:
    args = sys.argv[1:]
    if args and len(args) != 4:
        print(__doc__)
        return 2

    brutos = dict(zip(CHAVES, args)) if args else ler_config()
    precos = {k: normalizar(v) for k, v in brutos.items()}

    for k in CHAVES:
        print(f"  {k:10s} {precos[k][0]}")
    if any(p[1] == "0.00" for p in precos.values()):
        print("\n⚠  Ainda há preços zerados. O site NÃO deve ir ao ar assim.")

    # --- config.js ---
    cfg_path = BASE / "assets/js/config.js"
    cfg = cfg_path.read_text(encoding="utf-8")
    for k in CHAVES:
        cfg = re.sub(rf'({k}:\s*{{[^}}]*price:\s*")[^"]+(")', rf'\g<1>{precos[k][0]}\g<2>', cfg)
    cfg = cfg.replace('/* Planos — "price" ainda está por definir (R$ 00,00 = valor de espera). */',
                      "/* Planos. */") if precos["bronze"][1] != "0.00" else cfg
    cfg_path.write_text(cfg, encoding="utf-8")

    # --- HTML (cards, FAQ, termos) ---
    for rel in ["index.html", "termos-de-uso/index.html"]:
        p = BASE / rel
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        for k in CHAVES:
            inteiro, _, centavos = precos[k][0].replace("R$ ", "").partition(",")
            h = re.sub(rf'(<span[^>]*data-preco="{k}"[^>]*>)[^<]*(</span>)',
                       rf'\g<1>{precos[k][0]}\g<2>', h)
            h = re.sub(rf'(<span[^>]*data-preco-int="{k}"[^>]*>)[^<]*(</span>)',
                       rf'\g<1>{inteiro}\g<2>', h)
            h = re.sub(rf'(<span[^>]*data-preco-dec="{k}"[^>]*>)[^<]*(</span>)',
                       rf'\g<1>,{centavos}\g<2>', h)
        p.write_text(h, encoding="utf-8")

    # --- JSON-LD: Offer.price + texto da resposta do FAQ ---
    idx = BASE / "index.html"
    h = idx.read_text(encoding="utf-8")
    bloco = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', h, re.S)
    dados = json.loads(bloco.group(2))
    for no in dados["@graph"]:
        if no.get("@type") == "ItemList":
            for item in no["itemListElement"]:
                for k in CHAVES:
                    if item["item"]["name"] == NOMES[k]:
                        item["item"]["offers"]["price"] = precos[k][1]
        if no.get("@type") == "FAQPage":
            for q in no["mainEntity"]:
                if q["name"].startswith("Quanto custa"):
                    q["acceptedAnswer"]["text"] = (
                        f"Os planos apresentados começam em {precos['bronze'][0]} por 12 meses. "
                        f"As demais opções são de {precos['gold'][0]} por 15 meses, "
                        f"{precos['platinium'][0]} por 15 meses e {precos['exclusivo'][0]} por 24 meses."
                    )
    novo = json.dumps(dados, ensure_ascii=False, indent=2)
    h = h[:bloco.start(2)] + "\n" + novo + "\n" + h[bloco.end(2):]

    idx.write_text(h, encoding="utf-8")

    print("\n✓ Preços propagados em todo o site.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
