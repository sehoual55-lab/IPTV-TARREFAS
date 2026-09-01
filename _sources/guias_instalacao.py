#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insere o guia de instalação por aparelho na seção #instalacao (idempotente)."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from marcas import MARCAS  # noqa: E402

ICONES = {
    "tv": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "stick": '<rect x="3" y="9" width="14" height="7" rx="3.5"/><path d="M17 12.5h4"/>',
    "celular": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18.5h2"/>',
    "tablet": '<rect x="4" y="2" width="16" height="20" rx="2.5"/><path d="M10 18.5h4"/>',
    "computador": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M2 20h20"/>',
    "box": '<rect x="3" y="8" width="18" height="9" rx="2.5"/><circle cx="7.5" cy="12.5" r="1"/><path d="M11 12.5h6"/>',
}


def icone(chave: str, tamanho: int = 20) -> str:
    """Ícone neutro, para aparelhos sem logotipo de marca."""
    return (f'<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICONES[chave]}</svg>')


def logo(marca: str, tamanho: int) -> str:
    return (f'<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 24 24" '
            f'aria-hidden="true"><path fill="currentColor" d="{MARCAS[marca]}"/></svg>')


def marca_do_aparelho(g: dict, tamanho: int = 22) -> str:
    """Logotipos oficiais quando existem; senão, o ícone neutro."""
    if not g.get("marcas"):
        return icone(g["icone"], tamanho)
    return "".join(logo(m, tamanho) for m in g["marcas"])


GUIAS = [
    {
        "id": "samsung-lg",
        "marcas": ["Samsung", "LG"],
        "icone": "tv",
        "rotulo": "Samsung / LG Smart TV",
        "app": "IBO Player Pro / Bob Player",
        "passos": [
            'Instale o <strong>IBO Player Pro</strong> ou o <strong>Bob Player</strong> pela loja de aplicativos da sua TV.',
            'Anote o <strong>endereço MAC</strong> mostrado na tela do aplicativo.',
            'No celular ou no computador, acesse <strong>iboplayer.pro</strong> (IBO Player Pro) ou <strong>bobplayer.com</strong> (Bob Player).',
            'Informe o MAC e a chave (<em>key</em>). Depois, no aplicativo: <strong>Gerenciar playlist → Adicionar playlist</strong>, dê o nome «&nbsp;IPTV&nbsp;» e cole a <strong>URL M3U</strong> que você recebeu.',
            'Reinicie o aplicativo: os canais e a VOD aparecem.',
        ],
    },
    {
        "id": "firetv",
        "marcas": ["Amazon", "Android"],
        "icone": "stick",
        "rotulo": "Fire TV Stick / Android TV",
        "app": "IBO Player Pro",
        "passos": [
            'Abra a <strong>Google Play Store</strong> (Android TV) ou a <strong>Amazon Appstore</strong> (Fire TV) e procure o aplicativo.',
            'Se ele não estiver disponível na loja do seu aparelho, instale antes o app <strong>Downloader</strong>.',
            'No Downloader, digite o código <strong>481220</strong> e instale o aplicativo.',
            'No aplicativo: <strong>Trocar playlist → Adicionar playlist</strong>, dê o nome «&nbsp;IPTV&nbsp;» e cole a <strong>URL M3U</strong>.',
            'Reinicie o aplicativo: os canais e a VOD aparecem.',
        ],
    },
    {
        "id": "android",
        "marcas": ["Android"],
        "icone": "tablet",
        "rotulo": "Android / Tablet",
        "app": "TiviMate / IPTV Smarters",
        "passos": [
            'Abra a <strong>Google Play Store</strong> e instale o <strong>TiviMate</strong> ou o <strong>IPTV Smarters</strong>.',
            'No aplicativo, escolha adicionar uma playlist por <strong>URL M3U</strong> (ou por <em>Xtream Codes</em>, se você recebeu usuário e senha).',
            'Dê o nome «&nbsp;IPTV&nbsp;» à playlist e cole a URL que você recebeu.',
            'Reinicie o aplicativo: os canais e a VOD aparecem.',
        ],
    },
    {
        "id": "iphone",
        "marcas": ["Apple"],
        "icone": "celular",
        "rotulo": "iPhone / iPad",
        "app": "IBO Pro Player",
        "passos": [
            'Baixe o <strong>IBO Pro Player</strong> na <strong>App Store</strong>.',
            'No aplicativo: <strong>Trocar playlist → Adicionar playlist</strong>, dê o nome «&nbsp;IPTV&nbsp;» e cole a <strong>URL M3U</strong>.',
        ],
    },
    {
        "id": "windows-mac",
        "marcas": ["Windows", "Apple"],
        "icone": "computador",
        "rotulo": "Windows / macOS",
        "app": "IBO Player Pro",
        "passos": [
            'Instale o <strong>IBO Player Pro</strong> a partir de <strong>iboplayer.pro</strong>.',
            'No aplicativo: <strong>Trocar playlist → Adicionar playlist</strong>, dê o nome «&nbsp;IPTV&nbsp;» e cole a <strong>URL M3U</strong>.',
        ],
    },
    {
        "id": "formuler",
        "icone": "box",
        "rotulo": "Formuler Z",
        "app": "MYTVOnline 2 (Portal)",
        "passos": [
            'Abra o <strong>MYTVOnline 2</strong> e toque em <strong>+ Portal</strong>.',
            'Informe a <strong>URL do portal</strong> que você recebeu.',
            'Salve e reinicie o aparelho.',
        ],
    },
    {
        "id": "mag",
        "icone": "box",
        "rotulo": "MAG Box",
        "app": "Portals",
        "passos": [
            'Vá em <strong>Configurações → Sistema → Servidor → Portais</strong>.',
            'Informe a sua <strong>Portal URL</strong> (a do seu plano).',
            'Reinicie o aparelho: os canais ficam prontos.',
        ],
    },
]

ABERTURA = "<!-- GUIAS: início -->"
FECHO = "<!-- GUIAS: fim -->"


def painel(g: dict, primeiro: bool) -> str:
    passos = "\n".join(
        f'''            <li class="guia__passo">
              <span class="guia__num" aria-hidden="true">{i}</span>
              <p>{texto}</p>
            </li>'''
        for i, texto in enumerate(g["passos"], 1)
    )
    oculto = "" if primeiro else " hidden"
    return f'''        <div class="guia" id="guia-{g['id']}" data-guia="{g['id']}"{oculto}>
          <p class="guia__titulo">{g['rotulo']} — {g['app']}</p>
          <ol class="guia__lista">
{passos}
          </ol>
        </div>'''


def opcao(g: dict, primeiro: bool) -> str:
    marca = ' aria-selected="true"' if primeiro else ' aria-selected="false"'
    return f'''            <li class="picker__opt" role="option" id="opt-{g['id']}" data-value="{g['id']}"{marca}>
              <span class="picker__opt-icone" aria-hidden="true">{marca_do_aparelho(g, 21)}</span>
              <span>{g['rotulo']}</span>
              <svg class="picker__check" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 12 5 5L20 6"/></svg>
            </li>'''


def bloco() -> str:
    opcoes = "\n".join(opcao(g, i == 0) for i, g in enumerate(GUIAS))
    paineis = "\n\n".join(painel(g, i == 0) for i, g in enumerate(GUIAS))
    primeiro = GUIAS[0]
    return f'''{ABERTURA}
      <div class="guias" data-guias>
        <div class="guias__seletor">
          <div class="picker" data-picker>
            <span class="sr-only" id="picker-rotulo">Escolha o seu aparelho</span>
            <button class="picker__btn" type="button" id="picker-btn" data-picker-btn
                    aria-haspopup="listbox" aria-expanded="false" aria-labelledby="picker-rotulo picker-btn">
              <span class="picker__icone" data-picker-icone>{marca_do_aparelho(primeiro)}</span>
              <span class="picker__valor" data-picker-label>{primeiro['rotulo']}</span>
              <svg class="picker__chev" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
            </button>

            <ul class="picker__menu" role="listbox" tabindex="-1" aria-labelledby="picker-rotulo" data-picker-menu hidden>
{opcoes}
            </ul>
          </div>
        </div>

        <div class="guias__painel">
{paineis}
        </div>
      </div>

      <div class="btn-row btn-row--center" style="margin-top:28px">
        <a class="btn btn--primary" href="#planos">Ver os planos</a>
        <a class="btn btn--ghost" href="#dispositivos">Ver os aparelhos compatíveis</a>
      </div>
{FECHO}'''


def main() -> int:
    idx = BASE / "index.html"
    h = idx.read_text(encoding="utf-8")
    novo = bloco()

    if ABERTURA in h:
        h = h[: h.index(ABERTURA)] + novo + h[h.index(FECHO) + len(FECHO):]
    else:
        ancora = '''      <div class="notice" style="margin-top:26px">
        <p><strong>Importante:</strong>'''
        pos = h.index(ancora)
        cabecalho = '''      <h3 class="guias__cabecalho">Guia de instalação por aparelho</h3>
      <p class="guias__intro">Escolha o seu equipamento para ver os passos correspondentes. A URL M3U ou a URL de portal é enviada após a confirmação do pedido.</p>

'''
        h = h[:pos] + cabecalho + novo + "\n\n" + h[pos:]

    idx.write_text(h, encoding="utf-8")
    print(f"guias inseridos: {len(GUIAS)} aparelhos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
