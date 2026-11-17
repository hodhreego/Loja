# -*- coding: utf-8 -*-
"""Cor da tarja = cor do layout do produto (dominante saturada da capa -1.jpg, escurecida)."""
import os, colorsys
from PIL import Image
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
def cor_produto(slug):
    im = Image.open(os.path.join(IMG, slug + '-1.jpg')).convert('RGB'); im.thumbnail((120, 160))
    cont = {}
    for r, g, b in im.getdata():
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s < 0.45 or v < 0.25 or v > 0.97: continue
        k = (round(h * 24) % 24)           # 24 faixas de matiz
        cont.setdefault(k, []).append((r, g, b))
    k = max(cont, key=lambda x: len(cont[x]))
    px = cont[k]; r = sum(p[0] for p in px) // len(px); g = sum(p[1] for p in px) // len(px); b = sum(p[2] for p in px) // len(px)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    def rgb(vv): return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, min(1, s * 1.05), vv))
    return rgb(min(v, 0.62)), rgb(min(v, 0.62) * 0.55)
if __name__ == '__main__':
    import sys
    for s in sys.argv[1:]: print(s, cor_produto(s))
