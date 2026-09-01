#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification du site statique avant déploiement."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
errors, warnings = [], []

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr", "path", "rect", "circle",
        "line", "polyline", "polygon", "stop", "use", "ellipse"}


class Checker(HTMLParser):
    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.stack = []
        self.ids = []
        self.anchors = []
        self.hrefs = []
        self.headings = []
        self.labels = []
        self.controls = []
        self.aria_controls = []
        self.imgs = []
        self.buttons_without_text = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag == "label" and "for" in a:
            self.labels.append(a["for"])
        if tag in ("input", "select", "textarea") and "id" in a:
            self.controls.append(a["id"])
        if "aria-controls" in a:
            self.aria_controls.append(a["aria-controls"])
        if tag == "img":
            self.imgs.append(a)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            errors.append(f"{self.name}: </{tag}> sans ouverture")
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            errors.append(f"{self.name}: <{open_tag}> (ligne {pos[0]}) fermé par </{tag}>")


files = sorted(BASE.rglob("index.html"))
print(f"Páginas analisadas : {len(files)}\n")

for f in files:
    rel = "/" + str(f.relative_to(BASE)).replace("index.html", "")
    html = f.read_text(encoding="utf-8")
    c = Checker(rel)
    c.feed(html)
    c.close()

    if c.stack:
        errors.append(f"{rel}: tags não fechadas → {[t for t, _ in c.stack]}")

    dupes = {i for i in c.ids if c.ids.count(i) > 1}
    if dupes:
        errors.append(f"{rel}: ids duplicados → {sorted(dupes)}")

    # H1 unique
    h1s = html.count("<h1")
    if h1s != 1:
        errors.append(f"{rel}: {h1s} balise(s) H1 (une seule attendue)")

    # Hiérarchie des titres
    prev = 0
    for lvl in c.headings:
        if prev and lvl > prev + 1:
            warnings.append(f"{rel}: salto de nível H{prev} → H{lvl}")
        prev = lvl

    # Ancres internes
    for href in c.hrefs:
        if href.startswith("#"):
            target = href[1:]
            if target and target not in c.ids:
                errors.append(f"{rel}: âncora quebrada {href}")
        elif href.startswith("/") and not href.startswith("//"):
            path = href.split("#")[0].split("?")[0]
            candidate = BASE / path.strip("/") / "index.html" if not path.endswith((".xml", ".txt", ".svg", ".png", ".css", ".js")) else BASE / path.strip("/")
            if path in ("/", ""):
                candidate = BASE / "index.html"
            if not candidate.exists():
                errors.append(f"{rel}: link interno quebrado → {href}")

    # aria-controls
    for ac in c.aria_controls:
        if ac not in c.ids:
            errors.append(f"{rel}: aria-controls={ac} sans cible")

    # label ↔ champ
    for lf in c.labels:
        if lf not in c.controls:
            errors.append(f"{rel}: <label for=\"{lf}\"> sans champ correspondant")

    # Métadonnées
    for needle, msg in [
        ('<html lang="pt-BR">', "atributo lang=pt-BR ausente"),
        ('rel="canonical"', "canonical manquant"),
        ('name="description"', "meta description manquante"),
        ('property="og:title"', "Open Graph manquant"),
        ('name="twitter:card"', "métadonnées Twitter manquantes"),
        ('name="robots"', "meta robots manquante"),
        ('name="viewport"', "meta viewport manquante"),
    ]:
        if needle not in html:
            errors.append(f"{rel}: {msg}")

    title = re.search(r"<title>(.*?)</title>", html, re.S)
    if not title:
        errors.append(f"{rel}: <title> manquant")
    elif rel == "/":
        n = len(title.group(1))
        print(f"  Título da home : {n} caracteres — {title.group(1)}")
        if not 45 <= n <= 62:
            warnings.append(f"/ : titre de {n} caracteres (cible 50–60)")

    # Références d'assets
    for asset in re.findall(r'(?:src|href)="(/assets/[^"]+)"', html):
        if not (BASE / asset.lstrip("/")).exists():
            errors.append(f"{rel}: asset não encontrado → {asset}")

    # JSON-LD
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: JSON-LD inválido → {e}")
        else:
            types = [n.get("@type") for n in data.get("@graph", [data])]
            print(f"  JSON-LD {rel} : {types}")
            for forbidden in ("aggregateRating", "AggregateRating", "Review", "ratingValue"):
                if forbidden in block:
                    errors.append(f"{rel}: schema de avaliação/nota proibido detectado ({forbidden})")

home = (BASE / "index.html").read_text(encoding="utf-8")

# --- Règles tarifaires ---
plans = re.findall(r'<article class="plan(?:[^"]*)" data-plan-card="(\w+)"[^>]*>(.*?)</article>', home, re.S)
print(f"\nPlanos detectados : {[p[0] for p in plans]}")
import re as _re
_cfg = (BASE / "assets/js/config.js").read_text(encoding="utf-8")
_p = {k: _re.search(rf'{k}:\s*{{[^}}]*price:\s*"([^"]+)"', _cfg).group(1).replace("R$", "").strip()
      for k in ["bronze", "gold", "platinium", "exclusivo"]}
expected = {
    "bronze": (_p["bronze"], "12 meses", False),
    "gold": (_p["gold"], "15 meses", True),
    "platinium": (_p["platinium"], "15 meses", True),
    "exclusivo": (_p["exclusivo"], "24 meses", True),
}
if any(v == "00,00" for v in _p.values()):
    warnings.append("Preços ainda zerados: rode _sources/definir_precos.py antes de publicar")
if len(plans) != 4:
    errors.append(f"Home: {len(plans)} planos encontrados, 4 esperados")
for key, block in plans:
    price, duration, bonus = expected[key]
    _int, _, _dec = price.partition(",")
    if f'data-preco-int="{key}">{_int}<' not in block or f'data-preco-dec="{key}">,{_dec}<' not in block:
        errors.append(f"Plano {key}: preço {price} ausente dos spans data-preco-int/dec")
    if duration.replace(" ", "&nbsp;") not in block and duration not in block:
        errors.append(f"Plano {key}: duração {duration} ausente")
    has_bonus = '<p class="plan__bonus">' in block
    # a linha da lista deve estar riscada quando o plano não tem o bônus
    linha_off = '<li class="is-off">' in block and "+3 meses grátis" in block
    if not has_bonus and not linha_off:
        errors.append(f"Plano {key}: '+3 meses grátis' deveria aparecer riscado na lista")
    if has_bonus != bonus:
        errors.append(f"Plano {key}: '+3 meses grátis' {'presente indevidamente' if has_bonus else 'ausente'}")
    if 'data-conn aria-live="polite">1<' not in block:
        errors.append(f"Plano {key}: seletor de conexões não inicia em 1")
    print(f"  {key:10s} R$ {price} · {duration} · bônus={has_bonus} · 1 conexão=OK")

if home.count('class="plan__badge"') != 2 or "Mais escolhido" not in home or "Melhor valor" not in home:
    errors.append("Selos dos planos: esperados « Mais escolhido » e « Melhor valor »")
if home.count('data-stepper=') != 4:
    errors.append(f"Seletor de conexões: {home.count('data-stepper=')} encontrados, 4 esperados")
if home.count('data-buy=') != 4:
    errors.append(f"Botões de compra: {home.count('data-buy=')} encontrados, 4 esperados")
for _k in ["bronze", "gold", "platinium", "exclusivo"]:
    for _attr in ["data-preco-int", "data-preco-dec"]:
        if f'{_attr}="{_k}"' not in home:
            errors.append(f"{_attr} ausente para {_k}")
if "#contato" in home or "data-contact-form" in home:
    errors.append("Restos da seção de contato no index.html")
if "Platinum" in home:
    errors.append("Grafia: 'Platinum' encontrado, esperado 'Platinium'")

# --- FAQ : accordéon et cohérence JSON-LD ---
q_buttons = re.findall(r'data-faq-q[^>]*>\s*(.*?)\s*<svg', home, re.S)
q_buttons = [re.sub(r"\s+", " ", q).replace("&nbsp;", " ").strip() for q in q_buttons]
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', home, re.S).group(1))
faq_node = next(n for n in ld["@graph"] if n["@type"] == "FAQPage")
ld_qs = [q["name"].replace("\u202f", " ").strip() for q in faq_node["mainEntity"]]
print(f"\nFAQ : {len(q_buttons)} perguntas visíveis, {len(ld_qs)} no JSON-LD")
if len(q_buttons) != len(ld_qs):
    errors.append("FAQ: número de perguntas difere entre página e JSON-LD")
for a, b in zip(q_buttons, ld_qs):
    if a.replace(" ", "") != b.replace(" ", "").replace("\u00a0", ""):
        errors.append(f"FAQ : question désynchronisée → page « {a} » vs schéma « {b} »")

# --- Formulations interdites ---
banned = ["sem travar garantido", "100% legalizado", "melhor do brasil",
          "lorem ipsum", "estabilidade garantida", "satisfação garantida"]
lower = home.lower()
for phrase in banned:
    # « 100 % légal » est autorisé uniquement dans l'encadré de mise en garde et la FAQ
    if phrase.lower() in lower:
        ctx = [m.start() for m in re.finditer(re.escape(phrase.lower()), lower)]
        for pos in ctx:
            snippet = re.sub(r"\s+", " ", home[max(0, pos - 120):pos + 80])
            if "Desconfie" in snippet or "sem informação clara" in snippet:
                continue
            errors.append(f"Formulação proibida « {phrase} » → …{snippet}…")

# --- Placeholders légaux ---
for slug in ["informacoes-legais", "termos-de-uso", "politica-de-privacidade", "politica-de-reembolso"]:
    p = BASE / slug / "index.html"
    if not p.exists():
        errors.append(f"Página legal ausente : /{slug}/")
        continue
    txt = p.read_text(encoding="utf-8")
    if 'name="robots" content="noindex' not in txt:
        warnings.append(f"/{slug}/ : sem noindex")

# --- Fichiers techniques ---
for f in ["robots.txt", "sitemap.xml", "vercel.json", "assets/img/og-image.png", "assets/img/favicon.svg"]:
    if not (BASE / f).exists():
        errors.append(f"Arquivo ausente : {f}")
json.loads((BASE / "vercel.json").read_text())

print("\n" + "=" * 60)
if warnings:
    print("AVISOS :")
    for w in warnings:
        print("  ⚠", w)
if errors:
    print("ERROS :")
    for e in errors:
        print("  ✗", e)
    sys.exit(1)
print("✓ Todas as verificações passaram.")
