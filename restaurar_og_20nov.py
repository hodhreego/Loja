# -*- coding: utf-8 -*-
"""Volta a miniatura do WhatsApp (og.jpg) para a versao anterior ao Dia da Consciencia Negra.
Agendado para 20/11/2026 as 08:00. Restaura og.antes-cn.jpg, sobe a versao do og para v=8, rebuilda e publica."""
import shutil, subprocess, re, io, os
os.chdir(r'A:\Claude.ai\Loja')
shutil.copy2('og.antes-cn.jpg', 'og.jpg')
s = io.open('build_loja.py', encoding='utf-8').read()
s = s.replace('og.jpg?v=7', 'og.jpg?v=8')
io.open('build_loja.py', 'w', encoding='utf-8').write(s)
for c in (['python', 'build_loja.py'], ['python', 'gerar_produtos.py']):
    subprocess.run(c, check=True)
subprocess.run(['git', 'add', 'og.jpg', 'build_loja.py', 'index.html', 'concursos.html'], check=True)
subprocess.run(['git', 'add', '-u', '.'], check=True)
subprocess.run(['git', 'commit', '-q', '-m', 'Loja: volta a miniatura do WhatsApp anterior (fim do Dia da Consciencia Negra)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'], check=True)
subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:main'], check=True)
print('og restaurado')
