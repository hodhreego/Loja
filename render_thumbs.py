# -*- coding: utf-8 -*-
"""Miniaturas das apostilas PSS/CISOP para a loja.

- 1 capa limpa + ate 6 paginas internas escolhidas por quantidade de cor/ilustracao.
- Renderizadas em alta resolucao (1000 px de largura) e com a faixa AMOSTRA na diagonal.
- Pagina de gabarito recebe persianas ("GABARITO PROTEGIDO").
- Gera .jpg e .webp, e atualiza img/_paginas.json.

Uso:
  python render_thumbs.py                 # todas as apostilas
  python render_thumbs.py pedagogo artes  # so algumas
  python render_thumbs.py --capas         # somente a capa (pagina 1)
"""
import fitz
import os
import sys
import json
import glob

from PIL import Image

from gerar_previews import faixa, persianas

B = r"I:\Meu Drive\##Aulas @hodhreego\#$old1\PSS VENDAS"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

LARGURA = 1000          # largura final das imagens
MAX_INTERNAS = 6        # + capa = 7 imagens por produto
LIMITE_SCAN = 170       # nao varre o PDF inteiro (apostilas tem centenas de paginas)

P = {
 "matematica":        ("Av80 Apostila Matemática PSS Av80", "Apostila PSS Matemática — SEED-PR 2027.pdf"),
 "conhecimentos-basicos": ("Av81 Apostila Conhecimentos Básicos PSS Av81", "Apostila PSS Conhecimentos Básicos — SEED-PR 2027.pdf"),
 "pedagogo":          ("Av82 Apostila Pedagogo Av82", "Apostila PSS Pedagogo — SEED-PR 2027.pdf"),
 "educacao-especial": ("Av83 Apostila Educação Especial - Inclusiva Av83", "Apostila PSS Educação Especial — SEED-PR 2027.pdf"),
 "geografia":         ("Av85 Apostila de Geografia Av85", "Apostila PSS Geografia — SEED-PR 2027.pdf"),
 "artes":             ("Av86 Apostila de Artes Av86", "Apostila PSS Artes — SEED-PR 2027.pdf"),
 "lingua-inglesa":    ("Av87 Apostila de L. Inglesa Inglês PSS Av87", "Apostila PSS Língua Inglesa — SEED-PR 2027.pdf"),
 "educacao-fisica":   ("Av88 Apostila de Ed. Física PSS Av88", "Apostila PSS Educação Física — SEED-PR 2027.pdf"),
 "lingua-portuguesa": ("Av77 Apostila de Língua Portuguesa", "Apostila PSS Língua Portuguesa 2.0 — SEED-PR 2027.pdf"),
 "gestao-negocios":   ("Av89 Apostila de Gestão e Negócios — Administração", "Apostila PSS Gestão e Negócios (Administração) — SEED-PR 2027.pdf"),
 "informacao-comunicacao": ("Av90 Apostila de Infomação e Comunicação", "Apostila PSS INFORMAÇÃO E COMUNICAÇÃO — SEED-PR 2027.pdf"),
 "quimica":           ("Av91 Apostila de Química Av91", "Apostila PSS Química — SEED-PR 2027.pdf"),
 "pedagogo-abaetetuba": ("Abaetetuba/Pedagogo Av90", "Apostila Completa Pedagogo — Concurso Prefeitura de Abaetetuba-PA 2026.pdf"),
 "simulado-matematica": ("Av80 Apostila Matemática PSS Av80", "Simulados PSS Matemática — SEED-PR 2027 Av79.pdf"),
 "cisop-artesao":     ("Av102 Apostila Artesao Av102", "Apostila Artesao CISOP 2026.pdf"),
 "cisop-agente-administrativo": ("Av103 Apostila Agente Administrativo Av103", "Apostila Agente Administrativo CISOP 2026.pdf"),
 "cisop-tecnico-enfermagem": ("Av104 Apostila Tecnico em Enfermagem Av104", "Apostila Tecnico em Enfermagem CISOP 2026.pdf"),
 "cisop-monitor-biblioteca": ("Av105 Apostila Monitor de Biblioteca Av105", "Apostila Monitor de Biblioteca Cascavel 2026.pdf"),
 "cisop-professor-ed-infantil": ("Av106 Apostila Professor Ed Infantil Av106", "Apostila Professor Ed Infantil Cascavel 2026.pdf"),
 "cisop-professor-temporario": ("Av107 Apostila Professor Temporario Av107", "Apostila Professor Temporario Cascavel 2026.pdf"),
}


def cor_score(page):
    """Fracao de pixels coloridos (ilustracoes) na pagina."""
    pix = page.get_pixmap(dpi=28, colorspace=fitz.csRGB, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    h, s, v = im.convert("HSV").split()
    sat = s.point(lambda x: 255 if x > 72 else 0)
    val = v.point(lambda x: 255 if x > 45 else 0)
    from PIL import ImageChops
    m = ImageChops.multiply(sat, val)
    n = m.width * m.height
    return m.histogram()[255] / float(n)


def eh_gabarito(txt):
    return "GABARITO OFICIAL" in txt.upper()


def escolher(doc):
    """Paginas internas espalhadas pelo caderno, com texto e (de preferencia) figuras."""
    n = len(doc)
    if n < 4:
        return list(range(1, n))
    alvos = [0.12, 0.25, 0.38, 0.52, 0.66, 0.80]
    sel = []
    for f in alvos:
        base = max(1, min(n - 2, int(n * f)))
        melhor = None
        for d in range(0, 14):
            for j in (base + d, base - d):
                if j < 1 or j > n - 2 or j in sel:
                    continue
                txt = doc[j].get_text().strip()
                if len(txt) < 200:
                    continue
                pontos = 2 if doc[j].get_images() else 0
                if melhor is None or pontos > melhor[1]:
                    melhor = (j, pontos)
            if melhor and melhor[1] > 0:
                break
        if melhor:
            sel.append(melhor[0])
    return sorted(sel)[:MAX_INTERNAS]


def ultimo_pdf(pasta, padrao):
    """PDF salvo por ultimo na pasta, ignorando JUMBO, Simulado e Resumo Mapa Mental."""
    pdfs = glob.glob(os.path.join(pasta, "*.pdf"))
    sim = "simulado" in padrao.lower()          # apostila e simulado dividem a mesma pasta
    base = lambda p: os.path.basename(p).lower()
    pdfs = [p for p in pdfs if ("simulado" in base(p)) == sim]
    ruins = ("jumbo", "resumo", "mapa mental")
    bons = [p for p in pdfs if not any(r in base(p) for r in ruins)]
    pdfs = bons or pdfs
    return max(pdfs, key=os.path.getmtime) if pdfs else os.path.join(pasta, padrao)


def render(doc, idx):
    page = doc[idx]
    z = LARGURA / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def salva(im, slug, k):
    jpg = os.path.join(OUT, "%s-%d.jpg" % (slug, k))
    im.save(jpg, "JPEG", quality=86, optimize=True)
    try:
        im.save(os.path.join(OUT, "%s-%d.webp" % (slug, k)), "WEBP", quality=84, method=6)
    except Exception:
        pass


def limpar_sobras(slug, ate):
    for k in range(ate + 1, 12):
        for ext in (".jpg", ".webp"):
            p = os.path.join(OUT, "%s-%d%s" % (slug, k, ext))
            if os.path.exists(p):
                os.remove(p)


def gera(slug, pasta, nome_pdf):
    path = ultimo_pdf(os.path.join(B, pasta), nome_pdf)
    if not os.path.exists(path):
        print("FALTA", slug, path)
        return None
    doc = fitz.open(path)
    n = len(doc)
    salva(render(doc, 0), slug, 1)          # capa limpa (sem tarja)
    paginas = escolher(doc)
    k = 1
    for idx in paginas:
        im = render(doc, idx)
        im = persianas(im) if eh_gabarito(doc[idx].get_text()) else faixa(im)
        k += 1
        salva(im, slug, k)
    limpar_sobras(slug, k)
    doc.close()
    print("%-28s %d imagens  paginas=%s  <- %s" % (slug, k, [p + 1 for p in paginas], os.path.basename(path)))
    return {"paginas": n, "usadas": [p + 1 for p in paginas]}


if __name__ == "__main__":
    CAPAS = "--capas" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    jf = os.path.join(OUT, "_paginas.json")
    res = json.load(open(jf, encoding="utf-8")) if os.path.exists(jf) else {}
    for slug, (pasta, fn) in P.items():
        if only and slug not in only:
            continue
        if CAPAS:
            path = ultimo_pdf(os.path.join(B, pasta), fn)
            if not os.path.exists(path):
                print("FALTA", slug, path)
                continue
            doc = fitz.open(path)
            salva(render(doc, 0), slug, 1)
            doc.close()
            print(slug, "capa atualizada")
        else:
            r = gera(slug, pasta, fn)
            if r:
                res[slug] = r
    if not CAPAS:
        json.dump(res, open(jf, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
