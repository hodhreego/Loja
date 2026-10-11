# Roda no SEU computador (precisa dos PDFs em B e de: pip install pymupdf).
# Extrai das mesmas 4 páginas das miniaturas (capa, índice, 2 interiores) o texto com posição/fonte/cor
# e os retângulos/preenchimentos, para eu reconstruir as miniaturas em HTML.
# Uso:  python extrair_html.py            (todas)   |   python extrair_html.py matematica pedagogo
# Saída: img/_paginas_html.json  (envie/commite esse arquivo)
import fitz, os, sys, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "render_thumbs.py"), encoding="utf-8").read()
exec(src.split("res = {}")[0])          # reaproveita B, OUT, P e pick()

hexa = lambda c: "#%06x" % c if isinstance(c, int) else None
def rgb(t): return "#%02x%02x%02x" % tuple(round(v*255) for v in t[:3]) if t else None

def pagina(pg):
    W, H = pg.rect.width, pg.rect.height
    rects = []
    for d in pg.get_drawings():
        fill, stroke = rgb(d.get("fill")), rgb(d.get("color"))
        if not (fill or stroke): continue
        r = d["rect"]
        if r.width < 0.5 and r.height < 0.5: continue
        rects.append({"x": round(r.x0, 1), "y": round(r.y0, 1), "w": round(r.width, 1), "h": round(r.height, 1),
                      "fill": fill, "fo": d.get("fill_opacity"), "stroke": stroke,
                      "lw": d.get("width"), "radius": bool(d.get("items") and any(i[0] == "c" for i in d["items"]))})
    spans = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if not s["text"].strip(): continue
                x0, y0, x1, y1 = s["bbox"]
                spans.append({"t": s["text"], "x": round(x0, 1), "y": round(y0, 1), "w": round(x1-x0, 1), "h": round(y1-y0, 1),
                              "sz": round(s["size"], 1), "f": s["font"], "fl": s["flags"], "c": hexa(s["color"])})
    imgs = [{"x": round(i["bbox"][0], 1), "y": round(i["bbox"][1], 1), "w": round(i["bbox"][2]-i["bbox"][0], 1),
             "h": round(i["bbox"][3]-i["bbox"][1], 1)} for i in pg.get_image_info()]
    return {"W": round(W, 1), "H": round(H, 1), "rects": rects, "spans": spans, "imgs": imgs}

res = {}
only = sys.argv[1:]
for slug, (folder, fn) in P.items():
    if only and slug not in only: continue
    path = os.path.join(B, folder, fn)
    if not os.path.exists(path): print("FALTA", slug, path); continue
    doc = fitz.open(path); pages, n = pick(doc)
    res[slug] = {"paginas": n, "usadas": [p+1 for p in pages], "pgs": [pagina(doc[p]) for p in pages]}
    print(slug, [len(x["spans"]) for x in res[slug]["pgs"]], "textos")
json.dump(res, open(os.path.join(OUT, "_paginas_html.json"), "w"), ensure_ascii=False)
print("ok ->", os.path.join(OUT, "_paginas_html.json"))
