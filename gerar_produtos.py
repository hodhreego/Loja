# -*- coding: utf-8 -*-
"""Gera uma subpagina por produto da loja: /Loja/<codigo>/index.html

O codigo e o campo "av" do item (ex.: Av82 -> /Loja/Av82/). Itens sem codigo usam o slug.
Cada pagina tem galeria (7 imagens), preco, descricao, botao da Eduzz e volta para a loja.
Roda depois de build_loja.py (le os itens direto do index.html).
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://hodhreego.github.io/Loja"
WA = "5545999699444"


def itens():
    t = io.open(os.path.join(HERE, "index.html"), encoding="utf-8", errors="replace").read()
    i = t.index("const ITENS=")
    j = t.index("\n", i)
    s = t[i + len("const ITENS="):j].rstrip().rstrip(";")
    return json.loads(s)


def brl(v):
    return ("%.2f" % float(v)).replace(".", ",")


def codigo(it):
    av = str(it.get("av") or "").strip()
    if re.match(r"^Av\d+$", av, re.I):
        return av
    return it["slug"]


def pagina(it):
    cod = codigo(it)
    imgs = [u.split("?")[0] for u in it["imgs"]]
    capa = imgs[0] if imgs else ""
    interno = imgs[1:]
    preco = it.get("preco") or 0
    de = it.get("de") or None
    link = it.get("link") or ""
    nome = it["nome"]
    sub = it.get("sub") or ""
    grupo = it.get("grupoNome") or ""
    cod_wa = f"{cod} - {nome}"

    previa = "".join(
        f'<img src="../{u}" alt="{nome} - pagina {k+2}" loading="lazy" onclick="ver(this.src)">'
        for k, u in enumerate(interno)
    )
    preco_html = (f'<span class="de">R$ {brl(de)}</span> ' if de else "") + f'<b>R$ {brl(preco)}</b>'
    if link:
        comprar = f'<a class="btn comprar" href="{link}" target="_blank" rel="noopener">Comprar na Eduzz</a>'
    else:
        comprar = f'<a class="btn comprar" href="https://wa.me/{WA}?text={cod_wa}" target="_blank" rel="noopener">Falar no WhatsApp</a>'
    zap = f'<a class="btn zap" href="https://wa.me/{WA}?text={cod_wa}" target="_blank" rel="noopener">Tirar duvida no WhatsApp</a>'

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{nome} - Loja de Matematica</title>
<meta name="description" content="{sub[:150]}">
<link rel="canonical" href="{BASE}/{cod}/">
<meta property="og:title" content="{nome} - Loja de Matematica">
<meta property="og:description" content="{sub[:150]}">
<meta property="og:image" content="{BASE}/img/{os.path.basename(capa)}">
<meta property="og:url" content="{BASE}/{cod}/">
<meta property="og:type" content="product">
<link rel="stylesheet" href="../produto.css">
</head>
<body>
<header>
  <a class="voltar" href="../index.html">&larr; Voltar para a loja</a>
  <span class="grupo">{grupo}</span>
</header>
<main>
  <div class="foto">
    <img id="big" src="../{capa}" alt="{nome}">
  </div>
  <aside>
    <p class="cod">{cod}</p>
    <h1>{nome}</h1>
    <p class="sub">{sub}</p>
    <p class="preco">{preco_html}</p>
    <div class="acoes">{comprar}{zap}</div>
    <p class="aviso">PDF digital. Entrega imediata apos a confirmacao do pagamento.</p>
    <div class="mini">{previa}</div>
  </aside>
</main>
<footer>{cod} &middot; {grupo} &middot; Prof. Rodrigo Goncalves Pereira</footer>
<script>
function ver(u){{document.getElementById('big').src=u;window.scrollTo({{top:0,behavior:'smooth'}})}}
</script>
</body>
</html>"""


CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#0b1226;color:#f4f6ff;min-height:100vh;padding:0 16px 40px}
header{max-width:1100px;margin:0 auto;padding:18px 0 10px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.voltar{color:#a9b4d6;text-decoration:none;font-weight:700;font-size:.95rem}
.voltar:hover{color:#fff}
.grupo{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:#a9b4d6;border:1px solid rgba(255,255,255,.18);border-radius:99px;padding:5px 12px}
main{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,420px);gap:26px;align-items:start}
.foto{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:18px;padding:10px}
.foto img{width:100%;height:auto;display:block;border-radius:10px;background:#fff}
aside{padding-top:8px}
.cod{font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;color:#f472b6;font-weight:900;margin-bottom:6px}
h1{font-size:clamp(1.6rem,3vw,2.4rem);line-height:1.15;margin-bottom:10px}
.sub{color:#c7d0ea;line-height:1.5;margin-bottom:16px}
.preco{font-size:1.6rem;margin-bottom:16px}
.preco .de{color:#a9b4d6;text-decoration:line-through;font-size:1rem;margin-right:8px}
.preco b{color:#fbbf24}
.acoes{display:flex;flex-direction:column;gap:10px;margin-bottom:14px}
.btn{display:block;text-align:center;text-decoration:none;font-weight:900;border-radius:12px;padding:14px 16px;font-size:1rem}
.comprar{background:#16a34a;color:#fff}
.zap{background:#22c55e;color:#052e16}
.aviso{font-size:.82rem;color:#a9b4d6;margin-bottom:18px}
.mini{display:grid;grid-template-columns:repeat(auto-fill,minmax(84px,1fr));gap:8px}
.mini img{width:100%;height:auto;border-radius:8px;border:1px solid rgba(255,255,255,.2);cursor:pointer;background:#fff}
footer{max-width:1100px;margin:34px auto 0;color:#7c88ab;font-size:.82rem;text-align:center}
@media(max-width:820px){main{grid-template-columns:1fr}.foto{order:-1}}
"""


def main():
    its = itens()
    css_path = os.path.join(HERE, "produto.css")
    io.open(css_path, "w", encoding="utf-8").write(CSS)
    n = 0
    for it in its:
        cod = codigo(it)
        d = os.path.join(HERE, cod)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pagina(it))
        n += 1
    print("paginas geradas:", n)


if __name__ == "__main__":
    main()
