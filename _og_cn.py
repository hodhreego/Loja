# -*- coding: utf-8 -*-
import fitz, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import tarja_forte_cn as T
M = r'A:\Claude.ai\Materiais\Consciencia-Negra'
def pg(pdf, i, tarja=True):
    d = fitz.open(M + '/' + pdf); im = T.render(d, i)
    return T.tarja_forte(im) if tarja else im
cover = pg('Atividade6-Da-Africa-ao-Brasil.pdf', 0, False)
pgs = [pg('Atividade9-Negros-que-mudaram-o-mundo.pdf', 1), pg('Atividade8-Cientistas-negras-brasileiras.pdf', 4), pg('Atividade16-Brasileiros-negros-que-fizeram-historia.pdf', 3)]
W, H = 1200, 630
bg = Image.new('RGB', (W, H), (27, 58, 107))
d = ImageDraw.Draw(bg)
for y in range(H):
    k = y / H; d.line((0, y, W, y), fill=(int(15 + 20 * k), int(37 + 25 * k), int(71 + 40 * k)))
f1 = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 50); f2 = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 28); f3 = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 34)
d.text((40, 28), 'Dia da Consciência Negra', font=f1, fill=(252, 211, 77))
d.text((40, 92), 'Atividades prontas para imprimir · com gabarito · R$ 5,00 cada', font=f2, fill=(255, 255, 255))
def put(im, h, x, y, ang=0):
    im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS).convert('RGBA')
    sh = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((10, 10, im.width + 12, im.height + 12), fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(7))
    t = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0)); t.alpha_composite(sh); t.alpha_composite(im, (4, 4)); ImageDraw.Draw(t).rectangle((4, 4, 4 + im.width - 1, 4 + im.height - 1), outline=(255, 255, 255, 255), width=3)
    if ang: t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    bg.paste(t, (x, y), t)
put(cover, 385, 55, 150, 0)
xs = [(370, 148, -3), (655, 152, 2), (900, 148, -2)]
for im, (x, y, a) in zip(pgs, xs): put(im, 385, x, y, a)
d.rectangle((0, H - 58, W, H), fill=(15, 37, 71))
d.text((W // 2, H - 29), 'eduloja.com  ·  toque para ver as atividades', font=f3, fill=(252, 211, 77), anchor='mm')
bg.save('og.jpg', quality=88, optimize=True); bg.save('_og_cn_prev.png'); print('ok')
