# -*- coding: utf-8 -*-
"""Tarja AMOSTRA FORTE para as atividades do Dia da Consciencia Negra.

Faixa diagonal marrom-avermelhada 100% opaca (gasta muita tinta se imprimir),
com as letras VAZADAS (transparentes): da para ler a pagina por tras das letras,
mas a faixa inutiliza a folha. Imagens 2..4 de cada produto = paginas 2..4 do PDF.
Uso: python tarja_forte_cn.py
"""
import os, shutil
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(AQUI, 'img')
BKP = os.path.join(IMG, 'versao-anterior-tarja-fraca')
M = r'A:\Claude.ai\Materiais\Consciencia-Negra'
FONT = r'C:\Windows\Fonts\arialbd.ttf'
MARROM = (112, 38, 14)        # marrom avermelhado forte
BORDA = (60, 18, 6)
LARG = 827

PDFS = {
    'cn-raizes-africanas': 'Atividade1-Matematica-raizes-africanas.pdf',
    'cn-numeros-historia': 'Atividade2-Os-numeros-contam-a-historia.pdf',
    'cn-quem-sou-eu': 'Atividade3-Quem-sou-eu.pdf',
    'cn-gazeta-quilombos': 'Atividade4-Gazeta-dos-Quilombos.pdf',
    'cn-palavras-herdadas': 'Atividade5-Palavras-que-o-Brasil-herdou.pdf',
    'cn-da-africa-ao-brasil': 'Atividade6-Da-Africa-ao-Brasil.pdf',
    'cn-portugues-autoria-negra': 'Atividade7-Portugues-autoria-negra.pdf',
    'cn-cientistas-negras': 'Atividade8-Cientistas-negras-brasileiras.pdf',
    'cn-negros-mundo': 'Atividade9-Negros-que-mudaram-o-mundo.pdf',
    'cn-direitos-civis-eua': 'Atividade10-Direitos-civis-nos-EUA.pdf',
    'cn-apartheid': 'Atividade11-Apartheid-Africa-do-Sul.pdf',
    'cn-portugues-3ano': 'Atividade12-Portugues-3ano-O-baoba-e-o-leao.pdf',
    'cn-historia-3ano': 'Atividade13-Historia-3ano-Minha-familia.pdf',
    'cn-matematica-3ano': 'Atividade14-Matematica-3ano-Tambores.pdf',
    'cn-gazette-2': 'Atividade15-Quilombos-Gazette-II-ingles.pdf',
    'cn-brasileiros-historia': 'Atividade16-Brasileiros-negros-que-fizeram-historia.pdf',
}


def fonte(t):
    return ImageFont.truetype(FONT, t)


def _cobertura(w, h, angulo, frac):
    W, H = w * 2, h * 2
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rectangle((0, H // 2 - int(h * frac) // 2, W, H // 2 + int(h * frac) // 2), fill=255)
    m = m.rotate(angulo)
    c = m.crop((W // 2 - w // 2, H // 2 - h // 2, W // 2 - w // 2 + w, H // 2 - h // 2 + h))
    return sum(1 for v in c.getdata() if v) / float(w * h)


def achar_frac(w, h, angulo, alvo=0.25):
    lo, hi = 0.05, 0.60
    for _ in range(14):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _cobertura(w, h, angulo, mid) < alvo else (lo, mid)
    return (lo + hi) / 2


def tarja_forte(img, angulo=35, frac=None, offs=(0,)):
    w, h = img.size
    if frac is None:
        frac = achar_frac(w // 4, h // 4, angulo)
    W, H = w * 2, h * 2
    hb = int(h * frac)
    faixa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(faixa)
    furo = Image.new('L', (W, H), 255)
    t = 'AMOSTRA'
    f = fonte(int(hb * 0.80))
    while d.textlength(t, font=f) > w * 0.80:
        f = fonte(int(f.size * 0.95))
    for o in offs:
        cy = H // 2 + int(o * h)
        d.rectangle((0, cy - hb // 2, W, cy + hb // 2), fill=MARROM + (255,))
        d.rectangle((0, cy - hb // 2, W, cy - hb // 2 + 6), fill=BORDA + (255,))
        d.rectangle((0, cy + hb // 2 - 6, W, cy + hb // 2), fill=BORDA + (255,))
        ImageDraw.Draw(furo).text((W // 2, cy), t, font=f, fill=0, anchor='mm')
    a = ImageChops.multiply(faixa.getchannel('A'), furo)
    faixa.putalpha(a)
    faixa = faixa.rotate(angulo, resample=Image.BICUBIC)
    cx, cyy = faixa.width // 2, faixa.height // 2
    faixa = faixa.crop((cx - w // 2, cyy - h // 2, cx - w // 2 + w, cyy - h // 2 + h))
    out = img.convert('RGBA')
    out.alpha_composite(faixa)
    return out.convert('RGB')


def render(doc, idx):
    page = doc[idx]
    z = LARG / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def main():
    os.makedirs(BKP, exist_ok=True)
    import sys
    for slug, pdf in PDFS.items():
        if len(sys.argv) > 1 and slug not in sys.argv[1:]: continue
        doc = fitz.open(os.path.join(M, pdf))
        # miniatura 5 = pagina de gabarito (mais rosa) com TRES faixas
        rosa = []
        for i, pg in enumerate(doc):
            pm = pg.get_pixmap(dpi=30); sm = pm.samples; n = pm.n
            rosa.append(sum(1 for q in range(0, len(sm), n) if sm[q] > 200 and sm[q+2] > 100 and sm[q+1] < 110))
        gab = max(range(len(doc)), key=lambda i: rosa[i])
        # miniaturas 2..6 MISTURAM letra normal e letra grande, para ninguem achar que e tudo letra grande:
        # 2 = normal p.2 · 3 = grande p.2 · 4 = normal p.3 · 5 = grande p.3 · 6 = gabarito (normal) com 3 faixas
        gdoc = fitz.open(os.path.join(M, pdf.replace('.pdf', '-LETRA-GRANDE.pdf')))
        plano = ((2, doc, 1), (3, gdoc, 1), (4, doc, 2), (5, gdoc, 2), (6, doc, gab))
        for k, d_, idx in plano:
            dst = os.path.join(IMG, '%s-%d.jpg' % (slug, k))
            bk = os.path.join(BKP, '%s-%d.jpg' % (slug, k))
            if os.path.exists(dst) and not os.path.exists(bk):
                shutil.copy2(dst, bk)
            (tarja_forte(render(d_, idx), frac=0.105, offs=(-0.30, 0, 0.30)) if k == 6 else tarja_forte(render(d_, idx))).save(dst, 'JPEG', quality=86, optimize=True)
        gdoc.close()
        print('ok', slug)
        doc.close()


if __name__ == '__main__':
    main()
