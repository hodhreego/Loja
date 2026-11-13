# -*- coding: utf-8 -*-
"""Refaz as prévias dos cadernos Se Liga de Matemática na loja.

Regra da vitrine (mesma dos cadernos de Educação Financeira):
    1) capa                        — mantida como está
    2) e 3) as duas páginas de questões mais ilustradas
    4) e 5) duas páginas depois das questões (gabarito/resoluções)
Sem tarja AMOSTRA. Sobras antigas (6 e 7) são apagadas.
"""
import glob
import json
import os
import re

import fitz
from PIL import Image, ImageChops

RAIZ = r'A:\Claude.ai\Materiais\Matematica\Avaliacoes-Finais'
OUT = r'A:\Claude.ai\Loja\img'
LARGURA = 1000

P = {
    'se-liga-6': '6-ano-matematica',
    'se-liga-7': '7-ano-matematica',
    'se-liga-8': '8-ano-matematica',
    'se-liga-9': '9-ano-matematica',
    'se-liga-1em': '1-serie-em-matematica',
    'se-liga-2em': '2-serie-em-matematica',
    'se-liga-3em': '3-serie-em-matematica',
}


def cor_score(page):
    pix = page.get_pixmap(dpi=26, colorspace=fitz.csRGB, alpha=False)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    _, s, v = im.convert('HSV').split()
    sat = s.point(lambda x: 255 if x > 72 else 0)
    val = v.point(lambda x: 255 if x > 45 else 0)
    m = ImageChops.multiply(sat, val)
    return m.histogram()[255] / float(m.width * m.height)


def render(doc, idx):
    page = doc[idx]
    z = LARGURA / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def salva(im, slug, k):
    im.save(os.path.join(OUT, '%s-%d.jpg' % (slug, k)), 'JPEG', quality=86, optimize=True)
    try:
        im.save(os.path.join(OUT, '%s-%d.webp' % (slug, k)), 'WEBP', quality=84, method=6)
    except Exception:
        pass


def gera(slug, pasta):
    # o 8º ano tem a versão nova em -atualizado.pdf (o arquivo antigo ficou travado)
    alternativo = os.path.join(RAIZ, pasta, 'se-liga-2026-atualizado.pdf')
    pdf = alternativo if os.path.exists(alternativo) else os.path.join(RAIZ, pasta, 'se-liga-2026.pdf')
    if not os.path.exists(pdf):
        print('FALTA', pdf)
        return None
    doc = fitz.open(pdf)
    n = len(doc)
    texto = [doc[i].get_text() or '' for i in range(n)]

    # as questões terminam onde começa o gabarito
    fim = n - 1
    for i, t in enumerate(texto):
        if 'GABARITO OFICIAL' in t.upper():
            fim = i
            break

    # candidatas: páginas com questão de verdade (têm o código da habilidade),
    # fora a página de instruções "como aplicar" e a folha de respostas
    candidatas = []
    for i in range(1, max(2, fim)):
        t = texto[i].upper()
        if 'COMO APLICAR' in t or 'INSTRUÇÕES AO ALUNO' in t:
            continue
        if not re.search(r'EF0\d|EM\d', texto[i]):
            continue
        desenhos = len(doc[i].get_drawings())
        candidatas.append((cor_score(doc[i]) + min(desenhos, 120) / 4000.0, i))

    if not candidatas:
        candidatas = [(cor_score(doc[i]), i) for i in range(1, max(2, fim))]

    ilustradas = [i for _, i in sorted(candidatas, reverse=True)[:2]]
    ilustradas.sort()

    depois = list(range(max(fim, 1), n))
    amostras = [depois[0], depois[len(depois) // 2]] if depois else [fim]

    k = 1                       # 1 = capa, não mexe
    for i in ilustradas:
        k += 1
        salva(render(doc, i), slug, k)
    for i in amostras:
        k += 1
        salva(render(doc, i), slug, k)
    doc.close()

    # apaga sobras antigas (6, 7, ...)
    for extra in range(k + 1, 12):
        for ext in ('.jpg', '.webp'):
            p = os.path.join(OUT, '%s-%d%s' % (slug, extra, ext))
            if os.path.exists(p):
                os.remove(p)

    print('%-11s %d imagens | questões p.%s | pós-questões p.%s'
          % (slug, k, [i + 1 for i in ilustradas], [i + 1 for i in amostras]))
    return {'paginas': n, 'usadas': [1] + [i + 1 for i in ilustradas + amostras]}


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
