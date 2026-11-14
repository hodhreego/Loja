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


def tarja_forte(img, angulo=35, frac=None):
    w, h = img.size
    if frac is None:
        frac = achar_frac(w // 4, h // 4, angulo)
    W, H = w * 2, h * 2
    cy, hb = H // 2, int(h * frac)
    # camada da faixa (opaca) e mascara das letras (vazadas)
    faixa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(faixa)
    d.rectangle((0, cy - hb // 2, W, cy + hb // 2), fill=MARROM + (255,))
    d.rectangle((0, cy - hb // 2, W, cy - hb // 2 + 8), fill=BORDA + (255,))
    d.rectangle((0, cy + hb // 2 - 8, W, cy + hb // 2), fill=BORDA + (255,))
    t = 'AMOSTRA'
    f = fonte(int(hb * 0.80))
    while d.textlength(t, font=f) > w * 0.80:
        f = fonte(int(f.size * 0.95))
    furo = Image.new('L', (W, H), 255)
    ImageDraw.Draw(furo).text((W // 2, cy), t, font=f, fill=0, anchor='mm')
    a = ImageChops.multiply(faixa.getchannel('A'), furo)       # letras = alfa 0
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
    for slug, pdf in PDFS.items():
        doc = fitz.open(os.path.join(M, pdf))
        for k, idx in ((2, 1), (3, 2), (4, 3), (5, 4)):
            dst = os.path.join(IMG, '%s-%d.jpg' % (slug, k))
            bk = os.path.join(BKP, '%s-%d.jpg' % (slug, k))
            if os.path.exists(dst) and not os.path.exists(bk):
                shutil.copy2(dst, bk)
            tarja_forte(render(doc, idx)).save(dst, 'JPEG', quality=86, optimize=True)
        print('ok', slug)
        doc.close()


if __name__ == '__main__':
    main()
