# -*- coding: utf-8 -*-
"""Gera og.jpg (1200x630): miniaturas das atividades de Volumes para a prévia do link (WhatsApp etc.)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
CAPAS = [('se-liga-9',1), ('saeb-9',2), ('volume-prisma',1)]
W, H = 1200, 630
bg = Image.new('RGB', (W, H), '#0f2547')
d = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(15 + 12 * t), int(37 + 28 * t), int(71 + 50 * t)))
F = lambda n, s: ImageFont.truetype(r'C:\Windows\Fonts\%s' % n, s)
d.text((W // 2, 46), 'Loja de Matemática', font=F('georgiab.ttf', 46), fill='#ffffff', anchor='mm')
d.text((W // 2, 94), 'Se Liga  ·  Simulados SAEB  ·  Atividades de Volumes — A4 com gabarito', font=F('segoeui.ttf', 24), fill='#e3c25a', anchor='mm')
S, G = 340, 36
x0 = (W - (3 * S + 2 * G)) // 2
for i, (c, pg) in enumerate(CAPAS):
    x, y = x0 + i * (S + G), 170
    im = Image.open(os.path.join(HERE, 'img', c + '-%d.jpg' % pg)).convert('RGB').resize((S, S), Image.LANCZOS)
    d.rounded_rectangle((x - 4, y - 4, x + S + 4, y + S + 4), 12, fill='#ffffff')
    bg.paste(im, (x, y))
bg.save(os.path.join(HERE, 'og.jpg'), quality=88)
print('ok og.jpg')
