# -*- coding: utf-8 -*-
"""Gera as imagens dos 20 'Resumos por conteúdo' (capa limpa + 2 páginas internas com tarja AMOSTRA) em img/res-*-N.jpg/.webp
e a lista produtos_resumos.py (slug, nome, grupo, código Eduzz, preço, descrição) para o build_loja.py."""
import os
import re

import pymupdf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
M = r'A:\Claude.ai\Materiais'
ITENS = []   # (slug, nome, pdf)
for p, rot, ser in [('1-serie-em-matematica', 'Matemática', '1ª série EM'), ('2-serie-em-matematica', 'Matemática', '2ª série EM'), ('3-serie-em-matematica', 'Matemática', '3ª série EM'),
                    ('6-ano-matematica', 'Matemática', '6º ano'), ('7-ano-matematica', 'Matemática', '7º ano'), ('8-ano-matematica', 'Matemática', '8º ano'),
                    ('9-ano-matematica', 'Matemática', '9º ano'), ('6-ano-recomposicao', 'Recomposição da Aprendizagem Matemática', '6º ano'), ('9-ano-recomposicao', 'Recomposição da Aprendizagem Matemática', '9º ano'), ('3-serie-em-recomposicao', 'Recomposição da Aprendizagem Matemática', '3ª série EM')]:
    pref = {'Matemática': 'res-', 'Recomposição da Aprendizagem Matemática': 'res-rec-'}[rot]
    slug = pref + {'1ª série EM': '1em', '2ª série EM': '2em', '3ª série EM': '3em'}.get(ser, ser[0])
    ITENS.append((slug, 'Resumos por conteúdo · %s — %s' % (rot, ser), os.path.join(M, 'Matematica', 'Avaliacoes-Finais', p, 'resumos-se-liga-2026.pdf')))
for p, ser in [('6-ano', '6º ano'), ('7-ano', '7º ano'), ('8-ano', '8º ano'), ('9-ano', '9º ano'), ('1-serie-em', '1ª série EM'), ('2-serie-em', '2ª série EM'), ('3-serie-em', '3ª série EM')]:
    slug = 'res-ef-' + {'1ª série EM': '1em', '2ª série EM': '2em', '3ª série EM': '3em'}.get(ser, ser[0])
    ITENS.append((slug, 'Resumos por conteúdo · Educação Financeira — %s' % ser, os.path.join(M, 'Educacao-Financeira', 'Avaliacoes-Finais', p, 'resumos-se-liga-2026.pdf')))
for g in '6789':
    ITENS.append(('res-ing-' + g, 'Resumos por conteúdo · Inglês — %sº ano' % g, os.path.join(M, 'Ingles', 'Avaliacoes-Finais', '%s-ano-ingles' % g, 'resumos-se-liga-2026.pdf')))

W = 900


def pagina(d, i):
    p = d[i]
    z = W / p.rect.width
    pm = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
    return Image.frombytes('RGB', (pm.width, pm.height), pm.samples)


def amostra(im):
    im = im.convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    try:
        f = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', int(im.width * .16))
    except Exception:
        f = ImageFont.load_default()
    txt = 'AMOSTRA'
    tmp = Image.new('RGBA', (int(im.width * 1.3), int(im.width * .26)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.rectangle([0, 0, tmp.width, tmp.height], fill=(200, 16, 46, 205))
    bb = td.textbbox((0, 0), txt, font=f)
    td.text(((tmp.width - (bb[2] - bb[0])) / 2, (tmp.height - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f, fill=(255, 255, 255, 255))
    tmp = tmp.rotate(32, expand=True, resample=Image.BICUBIC)
    ov.paste(tmp, ((im.width - tmp.width) // 2, (im.height - tmp.height) // 2), tmp)
    return Image.alpha_composite(im, ov).convert('RGB')


def main():
    linhas = []
    for slug, nome, pdf in ITENS:
        d = pymupdf.open(pdf)
        html = open(os.path.splitext(pdf)[0] + '.html', encoding='utf-8', errors='ignore').read()
        nconteudos = len(re.findall(r'<h2 class="th">', html))
        cover = pagina(d, 0)
        outs = [cover]
        for k in (2, 4):
            if k < d.page_count:
                outs.append(amostra(pagina(d, k)))
        for n, im in enumerate(outs, 1):
            base = os.path.join(HERE, 'img', '%s-%d' % (slug, n))
            im.save(base + '.jpg', quality=88)
            im.save(base + '.webp', quality=82)
        mat = re.search(r'(Matem|Recompos|Educa|Ingl)', nome).group(1)
        linhas.append((slug, nome, 'reforco', None, 3, 'Resumo por conteúdo com %d tópicos e exercícios resolvidos passo a passo (%d páginas), alinhado ao Se Liga 2026. PDF em A4 para imprimir ou estudar no celular.' % (nconteudos, d.page_count)))
        print(slug, nconteudos, d.page_count, len(outs))
    with open(os.path.join(HERE, 'produtos_resumos.py'), 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n# gerado por _resumos_assets.py — Resumos por conteúdo (R$ 3,00 pelo WhatsApp)\nRESUMOS = %r\n' % (linhas,))


if __name__ == '__main__':
    main()
