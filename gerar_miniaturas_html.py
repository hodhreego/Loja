# Gera as miniaturas em HTML (mini/<slug>.json) a partir do HTML-fonte de cada apostila.
# Uso:  python gerar_miniaturas_html.py slug=caminho/apostila.html [slug=outro.html ...]
# Cada JSON guarda o CSS da apostila + as 4 páginas (capa, índice, 2 interiores); a loja monta em Shadow DOM.
import sys, os, re, json
from bs4 import BeautifulSoup
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "mini")
os.makedirs(OUT, exist_ok=True)

# Trocas manuais: slug -> {posição na miniatura (1 a 4): índice da .page no HTML-fonte (0 = primeira)}
TROCAS = {
    "matematica": {2: 8, 3: 5},   # Geometria Espacial (sólidos 3D) e Funções (gráficos) no lugar do índice e de Sistemas Lineares
}

def texto(t): return re.sub(r"\s+", " ", t.get_text(" ")).strip()

def escolhe(pages):
    capa = next((p for p in pages if "cover-page" in p.get("class", [])), pages[0])
    ind = next((p for p in pages if p.get("id") == "indice"), None) or \
          next((p for p in pages if re.match(r"\s*(ÍNDICE|SUMÁRIO)", texto(p), re.I)), None)
    miolo = [p for p in pages if p is not capa and p is not ind
             and not {"cover-page", "divider-page"} & set(p.get("class", [])) and len(texto(p)) > 600]
    if len(miolo) < 2: raise ValueError("poucas páginas de conteúdo (%d)" % len(miolo))
    return [capa, ind or miolo[0], miolo[len(miolo)//3], miolo[2*len(miolo)//3]]

for arg in sys.argv[1:]:
    slug, path = arg.split("=", 1)
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "lxml")
    css = "\n".join(s.get_text() for s in soup.find_all("style"))
    css = re.sub(r"@page\s*\{[^}]*\}", "", css)
    pages = soup.select(".page")
    try: sel = escolhe(pages)
    except ValueError as e: print("PULOU", slug, e); continue
    for pos, i in TROCAS.get(slug, {}).items(): sel[pos - 1] = pages[i]
    for p in sel:
        for s in p.find_all("script"): s.decompose()
        for a in p.find_all("a"): a.attrs.pop("href", None)
    data = {"css": css, "pages": [str(p) for p in sel], "n": len(pages)}
    json.dump(data, open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(slug, len(pages), "páginas ->", round(os.path.getsize(os.path.join(OUT, slug + ".json"))/1024), "KB")
