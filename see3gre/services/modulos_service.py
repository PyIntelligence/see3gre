import os
from flask import current_app

EXTENSOES_SUPORTADAS = (".png", ".jpg", ".jpeg", ".webp", ".svg")

# Mapeamento para módulos com título personalizado, URL externa, ícone padrão ou exceção visual
OVERRIDES_MODULOS = {
    "nudea": {
        "quadros_escolares": {
            "title": "Quadros Escolares",
            "default_file": "quadros_escolares.png",
            "url": "/quadro",
            "cardClass": "module-card",
            "showTitle": False
        }
    },
    "nutci": {
        "relatorio-nutci": {
            "title": "Relatório de Projeto - NUTCI",
            "default_file": "relatorio-nutci.png",
            "url": "https://makers-bonds-lap-carries.trycloudflare.com/",
            "cardClass": "module-card",
            "showTitle": False
        },
        "relatorio-vt-nutci": {
            "title": "Relatório VT - NUTCI",
            "default_file": "relatorio-vt-nutci.png",
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


def _resolver_pasta_img(nucleo_slug):
    base_service = os.path.dirname(os.path.abspath(__file__))

    candidatos = [
        # 1. Caminho padrão do Flask (Docker: /app/static/img/<nucleo> e execução local)
        os.path.join(current_app.static_folder, "img", nucleo_slug) if current_app.static_folder else "",
        # 2. Caminho relativo à pasta services/ (Vercel quando Root Directory = see3gre -> /var/task/static/img/<nucleo>)
        os.path.abspath(os.path.join(base_service, "..", "static", "img", nucleo_slug)),
        # 3. Caminho relativo à raiz do repositório (Vercel quando Root Directory = raiz -> /var/task/see3gre/static/img/<nucleo>)
        os.path.abspath(os.path.join(base_service, "..", "..", "see3gre", "static", "img", nucleo_slug)),
        # 4. Caminho via diretório de trabalho atual (os.getcwd())
        os.path.abspath(os.path.join(os.getcwd(), "static", "img", nucleo_slug)),
        os.path.abspath(os.path.join(os.getcwd(), "see3gre", "static", "img", nucleo_slug)),
    ]

    for caminho in candidatos:
        if caminho and os.path.isdir(caminho):
            return caminho

    return None


def listar_modulos_nucleo(nucleo):
    nucleo_slug = nucleo.strip().lower()
    pasta_img = _resolver_pasta_img(nucleo_slug)
    overrides_nucleo = OVERRIDES_MODULOS.get(nucleo_slug, {})
    modulos = []

    if pasta_img:
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

    # Garante fallback na Vercel mesmo se a CDN estática separar a pasta img do bundle Python
    if not modulos and overrides_nucleo:
        for slug, custom in overrides_nucleo.items():
            arquivo = custom.get("default_file", f"{slug}.png")
            modulos.append({
                "id": slug,
                "title": custom.get("title", _formatar_titulo(slug)),
                "icon": f"/static/img/{nucleo_slug}/{arquivo}",
                "url": custom.get("url", f"/{slug}"),
                "cardClass": custom.get("cardClass", "module-card"),
                "showTitle": custom.get("showTitle", False)
            })

    return modulos