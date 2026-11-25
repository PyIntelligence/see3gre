import os
from flask import current_app

EXTENSOES_SUPORTADAS = (".png", ".jpg", ".jpeg", ".webp", ".svg")

# Mapeamento apenas para módulos com título personalizado, URL externa ou exceção visual
OVERRIDES_MODULOS = {
    "nudea": {
        "quadros_escolares": {
            "title": "Quadros Escolares",
            "url": "/quadro",
            "cardClass": "module-card",
            "showTitle": False
        }
    },
    "nutci": {
        "relatorio-nutci": {
            "title": "Relatório de Projeto - NUTCI",
            "url": "https://makers-bonds-lap-carries.trycloudflare.com/",
            "cardClass": "module-card",
            "showTitle": False
        },
        "relatorio-vt-nutci": {
            "title": "Relatório VT - NUTCI",
            "url": "https://nutci-relatoriovt.onrender.com/",
            "cardClass": "module-card",
            "showTitle": False
        }
    }
}


def _formatar_titulo(nome_arquivo_sem_ext):
    palavras = nome_arquivo_sem_ext.replace("-", " ").replace("_", " ").split()
    siglas = {"nutci", "nudea", "nuafs", "nucom", "nudpe", "see", "gre", "bi", "pnae", "pdde", "eja", "ecit", "vt"}
    return " ".join(p.upper() if p.lower() in siglas else p.capitalize() for p in palavras)


def listar_modulos_nucleo(nucleo):
    nucleo_slug = nucleo.strip().lower()
    pasta_img = os.path.join(current_app.static_folder, "img", nucleo_slug)

    if not os.path.isdir(pasta_img):
        return []

    overrides_nucleo = OVERRIDES_MODULOS.get(nucleo_slug, {})
    modulos = []

    for arquivo in sorted(os.listdir(pasta_img)):
        if not arquivo.lower().endswith(EXTENSOES_SUPORTADAS):
            continue

        slug = os.path.splitext(arquivo)[0]
        custom = overrides_nucleo.get(slug, {})

        modulos.append({
            "id": slug,
            "title": custom.get("title", _formatar_titulo(slug)),
            "icon": f"/static/img/{nucleo_slug}/{arquivo}",
            "url": custom.get("url", f"/{slug}"),
            "cardClass": custom.get("cardClass", "module-card"),
            "showTitle": custom.get("showTitle", False)
        })

    return modulos