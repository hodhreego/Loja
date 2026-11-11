# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import tempfile

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
saida = r'C:\Users\i5\AppData\Local\Temp\opencode\loja_live2.png'
prof = tempfile.mkdtemp(prefix='loja-live-')
cmd = [CHROME, '--headless=new', '--disable-gpu', '--no-sandbox', '--user-data-dir=' + prof,
       '--hide-scrollbars', '--window-size=1200,2000', '--force-device-scale-factor=1',
       '--virtual-time-budget=8000', '--screenshot=' + saida,
       'https://hodhreego.github.io/Loja/?v=' + str(os.urandom(3).hex())]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
shutil.rmtree(prof, ignore_errors=True)
print('ok' if os.path.exists(saida) else 'falhou')
