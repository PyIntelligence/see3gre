import html
import re
import ssl
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

# Fuso horário oficial da Paraíba (UTC-3)
FUSO_PB = timezone(timedelta(hours=-3))

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

DIAS_SEMANA_PT = {
    0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
    3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"
}

# ==============================================================================
# LINKS ACOPLADOS (Feeds RSS/XML oficiais e regionais)
# Adicione ou remova URLs aqui sempre que quiser acoplar novas fontes de notícias
# ==============================================================================
FONTES_ACOPLADAS = [
    {
        "nome": "SEE-PB (Portal Oficial do Governo da Paraíba)",
        "url": "https://paraiba.pb.gov.br/diretas/secretaria-da-educacao/noticias/RSS",
        "nucleo_padrao": "SEE-PB"
    },
    {
        "nome": "Monitoramento Regional • 3ª GRE e SEE-PB",
        "url": "https://news.google.com/rss/search?q=%223%C2%AA+GRE%22+OR+%22Secretaria+da+Educa%C3%A7%C3%A3o+da+Para%C3%ADba%22+OR+%22SEE-PB%22&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "nucleo_padrao": "SEE-PB"
    },
    {
        "nome": "Rede Estadual Paraíba • Escolas e ECITs",
        "url": "https://news.google.com/rss/search?q=%22Rede+Estadual%22+Para%C3%ADba+educa%C3%A7%C3%A3o+OR+ECIT+Campina+Grande&hl=pt-BR&gl=BR&ceid=BR:pt-419",
        "nucleo_padrao": "NUDEA"
    }
]

# Cache em memória (15 minutos = 900 segundos) para carregamento instantâneo
_CACHE = {
    "timestamp": 0,
    "dados": None
}
CACHE_TTL_SEGUNDOS = 900


def _local_name(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _limpar_html(texto):
    if not texto:
        return ""
    sem_tags = re.sub(r"<[^>]+>", " ", html.unescape(texto))
    return re.sub(r"\s+", " ", sem_tags).strip()


def _classificar_nucleo(titulo, resumo, padrao="SEE-PB"):
    texto = f"{titulo} {resumo}".lower()
    if any(k in texto for k in ["pedagóg", "aprendizagem", "avaliação", "ideb", "enem", "saeb", "alfabetiza", "matrícula", "ecit", "eja", "currículo"]):
        return "NUDEA"
    if any(k in texto for k in ["servidor", "concurso", "processo seletivo", "edital", "merenda", "alimentação", "transporte", "reforma", "obra", "financeiro", "contrato"]):
        return "NUAFS"
    if any(k in texto for k in ["estudant", "grêmio", "jogos escolares", "olimpíada", "juventude", "protagonismo", "intercâmbio", "primeira chance"]):
        return "NUDPE"
    if any(k in texto for k in ["tecnologia", "digital", "computador", "chromebook", "internet", "conectividade", "sistema", "robótica", "ciência", "inovação"]):
        return "NUTCI"
    if any(k in texto for k in ["campanha", "divulgação", "imprensa", "evento", "encontro", "cerimônia"]):
        return "NUCOM"
    return padrao


def _parse_data(raw_date):
    if not raw_date:
        return None
    raw_date = raw_date.strip()
    try:
        dt = parsedate_to_datetime(raw_date)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(FUSO_PB)
    except Exception:
        pass

    try:
        dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=FUSO_PB)
        return dt.astimezone(FUSO_PB)
    except Exception:
        return None


def _requisitar_xml(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Portal-SEE3GRE/1.0; +https://see3gre.pb.gov.br)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.read()
    except urllib.error.URLError:
        # Fallback para cadeias SSL governamentais (ICP-Brasil) em imagens Docker slim
        ctx_inseguro = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=8, context=ctx_inseguro) as resp:
            return resp.read()


def _buscar_feed(fonte):
    itens = []
    xml_bytes = _requisitar_xml(fonte["url"])
    root = ET.fromstring(xml_bytes)

    for elem in root.iter():
        if _local_name(elem.tag) not in ("item", "entry"):
            continue

        titulo = ""
        link = ""
        resumo = ""
        raw_date = ""
        veiculo = fonte["nome"]

        for child in elem:
            nome_tag = _local_name(child.tag)
            texto_tag = (child.text or "").strip()

            if nome_tag == "title" and texto_tag:
                titulo = _limpar_html(texto_tag)
            elif nome_tag == "link":
                link = texto_tag or child.attrib.get("href", "").strip()
            elif nome_tag in ("description", "summary", "content") and texto_tag and not resumo:
                resumo = _limpar_html(texto_tag)
            elif nome_tag in ("pubDate", "date", "published", "updated") and texto_tag and not raw_date:
                raw_date = texto_tag
            elif nome_tag == "source" and texto_tag:
                veiculo = _limpar_html(texto_tag)

        # Separa o nome do veículo caso venha no padrão "Título - Veículo" (Google News)
        if " - " in titulo and veiculo == fonte["nome"]:
            partes = titulo.rsplit(" - ", 1)
            if len(partes[1]) <= 45:
                titulo, veiculo = partes[0].strip(), partes[1].strip()

        if not titulo or not link:
            continue

        dt_pub = _parse_data(raw_date) or datetime.now(FUSO_PB)

        if not resumo or resumo.lower() == titulo.lower():
            resumo = f"Matéria publicada por {veiculo}. Clique para acessar o conteúdo completo na fonte oficial."
        elif len(resumo) > 260:
            resumo = resumo[:257].rsplit(" ", 1)[0] + "..."

        nucleo = _classificar_nucleo(titulo, resumo, fonte["nucleo_padrao"])

        itens.append({
            "titulo": titulo,
            "link": link,
            "resumo": resumo,
            "veiculo": veiculo,
            "nucleo": nucleo,
            "data_formatada": dt_pub.strftime("%d/%m/%Y"),
            "hora_formatada": dt_pub.strftime("%H:%M"),
            "dia": dt_pub.day,
            "mes": dt_pub.month,
            "ano": dt_pub.year,
            "mes_nome": MESES_PT[dt_pub.month],
            "timestamp": dt_pub.timestamp()
        })

    return itens


def obter_noticias_automaticas(forcar_atualizacao=False):
    agora = datetime.now(FUSO_PB)
    agora_ts = time.time()

    if not forcar_atualizacao and _CACHE["dados"] and (agora_ts - _CACHE["timestamp"] < CACHE_TTL_SEGUNDOS):
        resultado = dict(_CACHE["dados"])
        resultado["data_hoje"] = f"{DIAS_SEMANA_PT[agora.weekday()]}, {agora.day:02d} de {MESES_PT[agora.month]} de {agora.year}"
        resultado["mes_atual"] = agora.month
        resultado["ano_atual"] = agora.year
        resultado["mes_atual_nome"] = MESES_PT[agora.month]
        return resultado

    todas_noticias = []
    titulos_vistos = set()
    fontes_ativas = 0

    for fonte in FONTES_ACOPLADAS:
        try:
            encontradas = _buscar_feed(fonte)
            if encontradas:
                fontes_ativas += 1
            for item in encontradas:
                chave = item["titulo"].lower()[:75]
                if chave not in titulos_vistos:
                    titulos_vistos.add(chave)
                    item["do_mes_atual"] = (item["mes"] == agora.month and item["ano"] == agora.year)
                    item["de_hoje"] = (item["do_mes_atual"] and item["dia"] == agora.day)
                    todas_noticias.append(item)
        except Exception:
            continue

    # Ordena da mais recente para a mais antiga
    todas_noticias.sort(key=lambda x: x["timestamp"], reverse=True)

    # Fallback institucional caso o servidor esteja sem acesso externo à internet
    if not todas_noticias:
        todas_noticias = [
            {
                "titulo": "3ª GRE mantém monitoramento contínuo das ações pedagógicas e administrativas nas 94 escolas da regional",
                "link": "https://paraiba.pb.gov.br/diretas/secretaria-da-educacao",
                "resumo": "Acompanhe os editais, portarias e comunicados oficiais da Secretaria de Estado da Educação da Paraíba diretamente no portal institucional.",
                "veiculo": "Portal SEE-PB",
                "nucleo": "SEE-PB",
                "data_formatada": agora.strftime("%d/%m/%Y"),
                "hora_formatada": agora.strftime("%H:%M"),
                "dia": agora.day,
                "mes": agora.month,
                "ano": agora.year,
                "mes_nome": MESES_PT[agora.month],
                "do_mes_atual": True,
                "de_hoje": True,
                "timestamp": agora.timestamp()
            }
        ]

    resultado = {
        "data_hoje": f"{DIAS_SEMANA_PT[agora.weekday()]}, {agora.day:02d} de {MESES_PT[agora.month]} de {agora.year}",
        "mes_atual": agora.month,
        "ano_atual": agora.year,
        "mes_atual_nome": MESES_PT[agora.month],
        "atualizado_em": agora.strftime("%d/%m/%Y às %H:%M"),
        "fontes_ativas": fontes_ativas,
        "total_fontes": len(FONTES_ACOPLADAS),
        "noticias": todas_noticias[:24]
    }

    _CACHE["timestamp"] = agora_ts
    _CACHE["dados"] = resultado
    return resultado