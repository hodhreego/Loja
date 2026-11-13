# -*- coding: utf-8 -*-
"""Miniaturas dos cadernos Se Liga de Educação Financeira para a loja.

Regra da vitrine:
  1) capa limpa;
  2) e 3) as duas paginas de questoes mais ilustradas;
  4) e 5) duas paginas aleatorias depois das questoes (gabarito/resolucoes).
Sem tarja AMOSTRA.
"""
import glob
import json
import os

import fitz
from PIL import Image, ImageChops

RAIZ = r'A:\Claude.ai\Materiais\Educacao-Financeira\Avaliacoes-Finais'
OUT = r'A:\Claude.ai\Loja\img'
LARGURA = 1000

P = {
    'ef-6': '6-ano',
    'ef-7': '7-ano',
    'ef-8': '8-ano',
    'ef-9': '9-ano',
    'ef-1em': '1-serie-em',
    'ef-2em': '2-serie-em',
    'ef-3em': '3-serie-em',
}


def cor_score(page):
    pix = page.get_pixmap(dpi=26, colorspace=fitz.csRGB, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    h, s, v = im.convert("HSV").split()
    sat = s.point(lambda x: 255 if x > 72 else 0)
    val = v.point(lambda x: 255 if x > 45 else 0)
    m = ImageChops.multiply(sat, val)
    return m.histogram()[255] / float(m.width * m.height)


def render(doc, idx):
    page = doc[idx]
    z = LARGURA / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def salva(im, slug, k):
    im.save(os.path.join(OUT, '%s-%d.jpg' % (slug, k)), 'JPEG', quality=86, optimize=True)
    try:
        im.save(os.path.join(OUT, '%s-%d.webp' % (slug, k)), 'WEBP', quality=84, method=6)
    except Exception:
        pass


def gera(slug, pasta):
    pdf = os.path.join(RAIZ, pasta, 'se-liga-educacao-financeira.pdf')
    if not os.path.exists(pdf):
        print('FALTA', pdf)
        return None
    doc = fitz.open(pdf)
    n = len(doc)
    texto = [doc[i].get_text() or '' for i in range(n)]

    # fim das questoes = primeira pagina com GABARITO
    fim = n - 1
    for i, t in enumerate(texto):
        if 'GABARITO' in t.upper():
            fim = i
            break
    ini_q = 1                      # pagina 0 e a capa
    faixa_q = range(ini_q, max(ini_q + 1, fim))

    notas = sorted(((cor_score(doc[i]), i) for i in faixa_q), reverse=True)
    ilustradas = [i for _, i in notas[:2]]

    # duas paginas aleatorias depois das questoes (gabarito/resolucoes)
    depois = [i for i in range(max(fim, 1), n)]
    aleatorias = []
    if depois:
        passo = max(1, len(depois) // 2)
        aleatorias = [depois[0], depois[min(len(depois) - 1, passo)]]

    # imagem 1 é a CAPA (gerada por capa_se_liga_ef.py) — não sobrescrever aqui
    k = 1
    for i in ilustradas:
        k += 1
        salva(render(doc, i), slug, k)
    for i in aleatorias:
        k += 1
        salva(render(doc, i), slug, k)
    doc.close()
    print('%-8s %d imagens | ilustradas %s | pos-questoes %s'
          % (slug, k, [i + 1 for i in ilustradas], [i + 1 for i in aleatorias]))
    return {'paginas': n, 'usadas': [1] + [i + 1 for i in ilustradas + aleatorias]}


if __name__ == '__main__':
    res = {}
    jf = os.path.join(OUT, '_paginas.json')
    if os.path.exists(jf):
        res = json.load(open(jf, encoding='utf-8'))
    for slug, pasta in P.items():
        r = gera(slug, pasta)
        if r:
            res[slug] = r
    json.dump(res, open(jf, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('ok')
