# -*- coding: utf-8 -*-
"""Confere se a imagem publicada em eduloja.com é a mesma gerada localmente."""
import hashlib
import io
import urllib.request

LOCAL = r'A:\Claude.ai\Loja\img\se-liga-6-2.jpg'
URL = 'https://eduloja.com/img/se-liga-6-2.jpg'


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()[:16]


local = open(LOCAL, 'rb').read()
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
remoto = urllib.request.urlopen(req, timeout=30).read()
print('local :', len(local), sha_bytes(local))
print('remoto:', len(remoto), sha_bytes(remoto))
print('iguais:', sha_bytes(local) == sha_bytes(remoto))
