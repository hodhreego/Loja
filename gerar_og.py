# -*- coding: utf-8 -*-
"""Gera og.jpg (1200x630): miniaturas das atividades de Volumes para a prévia do link (WhatsApp etc.)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
CAPAS = ['volume-cone', 'volume-cubo', 'volume-paralelepipedo', 'volume-prisma',
         'volume-esfera', 'volume-piramide', 'volume-cilindro', None]
W, H = 1200, 630
bg = Image.new('RGB', (W, H), '#0f2547')
d = ImageDraw.Draw(bg)
for y in range(H):  # degradê vertical azul-marinho
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(15 + 12 * t), int(37 + 28 * t), int(71 + 50 * t)))
F = lambda n, s: ImageFont.truetype(r'C:\Windows\Fonts\%s' % n, s)
d.text((W // 2, 44), 'Atividades de Volumes', font=F('georgiab.ttf', 46), fill='#ffffff', anchor='mm')
d.text((W // 2, 92), 'Loja de Matemática  ·  A4 pronto para imprimir, com gabarito', font=F('segoeui.ttf', 24), fill='#e3c25a', anchor='mm')
S, G = 236, 18
x0 = (W - (4 * S + 3 * G)) // 2
for i, c in enumerate(CAPAS):
    x, y = x0 + (i % 4) * (S + G), 126 + (i // 4) * (S + G)
    if c is None:
        d.rounded_rectangle((x - 3, y - 3, x + S + 3, y + S + 3), 10, fill='#e3c25a')
        for k, (t, f, col) in enumerate([('+ Volumes', F('georgiab.ttf', 30), '#0f2547'), ('Apostilas, Se Liga', F('segoeui.ttf', 22), '#0f2547'),
                                         ('e Simulados SAEB', F('segoeui.ttf', 22), '#0f2547'), ('hodhreego.github.io/Loja', F('segoeui.ttf', 15), '#4a3a00')]):
            d.text((x + S // 2, y + 62 + k * 40), t, font=f, fill=col, anchor='mm')
        continue
    im = Image.open(os.path.join(HERE, 'img', c + '-1.jpg')).convert('RGB').resize((S, S), Image.LANCZOS)
    d.rounded_rectangle((x - 3, y - 3, x + S + 3, y + S + 3), 10, fill='#ffffff')
    bg.paste(im, (x, y))
bg.save(os.path.join(HERE, 'og.jpg'), quality=88)
print('ok og.jpg')
