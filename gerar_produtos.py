# -*- coding: utf-8 -*-
"""Gera uma subpagina por produto da loja: /Loja/<codigo>/index.html

O codigo e o campo "av" do item (ex.: Av82 -> /Loja/Av82/). Itens sem codigo usam o slug.
Cada pagina tem galeria com lightbox, preco, descricao, botoes de compra, itens
relacionados, dados estruturados (SEO) e volta para a loja.

Roda depois de build_loja.py (le os itens direto do index.html).
"""
import io
import json
import os
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://eduloja.com"
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


def rel(it, todos):
    mesmo_grupo = [x for x in todos if x is not it and x.get("grupo") == it.get("grupo")]
    mesmo_tipo = [x for x in todos if x is not it and x.get("tipo") == it.get("tipo") and x.get("grupo") != it.get("grupo")]
    out, vistos = [], {it["slug"]}
    for x in mesmo_grupo + mesmo_tipo:
        if x["slug"] in vistos:
            continue
        vistos.add(x["slug"])
        out.append(x)
        if len(out) >= 6:
            break
    return out


def combo(it, todos):
    """Parceiro(s) de combo, com 15% de desconto sobre a soma."""
    por = {x["slug"]: x for x in todos}
    s = it["slug"]
    par = []
    m = re.match(r"^(se-liga|sei)-(.+)$", s)
    if m:
        outro = ("sei-" if m.group(1) == "se-liga" else "se-liga-") + m.group(2)
        if outro in por:
            par = [por[outro]]
    elif s.startswith("volume-"):
        par = [x for x in todos if x["slug"].startswith("volume-") and x["slug"] != s][:6]
    elif s == "matematica" and "simulado-matematica" in por:
        par = [por["simulado-matematica"]]
    elif s == "simulado-matematica" and "matematica" in por:
        par = [por["matematica"]]
    elif s in ("album-multiplicacao", "consciencia-negra"):
        outro = "consciencia-negra" if s == "album-multiplicacao" else "album-multiplicacao"
        if outro in por:
            par = [por[outro]]
    elif it.get("grupo") == "pss" and s != "conhecimentos-basicos" and "conhecimentos-basicos" in por:
        par = [por["conhecimentos-basicos"]]
    par = [p for p in par if p and p["slug"] != s]
    if not par:
        par = rel(it, todos)[:1]
    total = (float(it.get("preco") or 0) + sum(float(p.get("preco") or 0) for p in par)) * 0.85
    return par, round(total, 2)


def card_rel(x):
    cod = codigo(x)
    capa = x["imgs"][0].split("?")[0] if x["imgs"] else ""
    return (f'<div class="rel">'
            f'<a class="rel-link" href="../{cod}/">'
            f'<img src="../{capa}" alt="{x["nome"]}" loading="lazy">'
            f'<span class="rel-nome">{x["nome"]}</span></a>'
            f'<div class="rel-foot"><span class="rel-preco">R$ {brl(x.get("preco") or 0)}</span>'
            f'<button type="button" class="rel-add" onclick="addCart(\'{x["slug"]}\')" '
            f'aria-label="Adicionar {x["nome"]} ao carrinho">+ 🛒</button></div></div>')


def pagina(it, todos):
    cod = codigo(it)
    imgs = [u.split("?")[0] for u in it["imgs"]]
    capa = imgs[0] if imgs else ""
    preco = it.get("preco") or 0
    de = it.get("de") or None
    link = it.get("link") or ""
    nome = it["nome"]
    sub = it.get("sub") or ""
    grupo = it.get("grupoNome") or ""
    cod_wa = f"{cod} - {nome}"
    whats = f"https://wa.me/{WA}?text={cod_wa}"

    novas = [u for u in imgs if u]
    mini = "".join(
        f'<button type="button" class="mini-img{" on" if k == 0 else ""}" onclick="troca({k})">'
        f'<img src="../{u}" alt="{nome} - imagem {k+1}" loading="lazy"></button>'
        for k, u in enumerate(novas)
    )
    preco_html = (f'<span class="de">R$ {brl(de)}</span> ' if de else "") + f'R$ {brl(preco)}'
    if link:
        comprar = f'<a class="btn comprar" href="{link}" target="_blank" rel="noopener">Comprar na Eduzz</a>'
        pagamento = "Pagamento seguro pela Eduzz"
    else:
        comprar = f'<a class="btn comprar" href="{whats}" target="_blank" rel="noopener">Pedir pelo WhatsApp</a>'
        pagamento = "Atendimento direto pelo WhatsApp"
    zap = f'<a class="btn zap" href="{whats}" target="_blank" rel="noopener">Tirar dúvida no WhatsApp</a>'
    carrinho = f'<button type="button" class="btn carrinho" onclick="addCart(\'{it["slug"]}\')">Adicionar ao carrinho</button>'
    relacionados = "".join(card_rel(x) for x in rel(it, todos))

    parceiros, total_combo = combo(it, todos)
    combo_html = ""
    if parceiros:
        nomes = " + ".join([nome] + [p["nome"] for p in parceiros])
        cheio = float(preco) + sum(float(p.get("preco") or 0) for p in parceiros)
        texto = f"Quero o combo: {nomes} - R$ {brl(total_combo)} (15% de desconto)"
        wa_combo = "https://wa.me/%s?text=%s" % (WA, quote(texto))
        lista = ", ".join("'%s'" % x for x in [it["slug"]] + [p["slug"] for p in parceiros])
        combo_html = (f'<div class="combo-txt"><span class="selo">-15%</span>'
                      f'<h2>Leve junto e economize</h2>'
                      f'<p><b>{nomes}</b> por <b class="preco-combo">R$ {brl(total_combo)}</b></p>'
                      f'<p class="combo-sub">Separado sairia R$ {brl(cheio)}. O desconto é aplicado no pedido pelo WhatsApp.</p></div>'
                      f'<div class="combo-acoes">'
                      f'<a class="btn comprar" href="{wa_combo}" target="_blank" rel="noopener">Pedir combo no WhatsApp</a>'
                      f'<button type="button" class="btn carrinho" onclick="addCombo([{lista}])">'
                      f'Adicionar os {len(parceiros) + 1} ao carrinho</button></div>')

    ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": nome,
        "sku": cod,
        "description": sub,
        "image": [f"{BASE}/{u}" for u in novas],
        "brand": {"@type": "Brand", "name": "Prof. Rodrigo Gonçalves Pereira"},
        "offers": {
            "@type": "Offer",
            "price": f"{float(preco):.2f}",
            "priceCurrency": "BRL",
            "availability": "https://schema.org/InStock",
            "url": f"{BASE}/{cod}/",
        },
    }
    if link:
        ld["offers"]["url"] = link
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{nome} — Loja de Matemática</title>
<meta name="description" content="{sub[:155]}">
<link rel="canonical" href="{BASE}/{cod}/">
<meta property="og:site_name" content="Loja de Matemática">
<meta property="og:title" content="{nome} — {grupo}">
<meta property="og:description" content="{sub[:155]}">
<meta property="og:image" content="{BASE}/{capa}">
<meta property="og:url" content="{BASE}/{cod}/">
<meta property="og:type" content="product">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="../produto.css?v=wn3">
<script>try{{if(/[?&]embed=1/.test(location.search))document.documentElement.className="emb"}}catch(e){{}}</script>
<base target="_top">
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<div class="wbar" role="banner"><span class="wtit">{nome} — Loja de Matemática</span><span class="wbtns"><span class="wb" aria-hidden="true" title="Minimizar"><svg width="10" height="10" viewBox="0 0 10 10"><path d="M0 5.5h10" stroke="currentColor" stroke-width="1"/></svg></span><span class="wb" aria-hidden="true" title="Maximizar"><svg width="10" height="10" viewBox="0 0 10 10"><rect x=".5" y=".5" width="9" height="9" fill="none" stroke="currentColor" stroke-width="1"/></svg></span><a class="wb wx" href="../index.html" title="Fechar e voltar para a loja" aria-label="Fechar e voltar para a loja"><svg width="10" height="10" viewBox="0 0 10 10"><path d="M0 0l10 10M10 0L0 10" stroke="currentColor" stroke-width="1.1"/></svg></a></span></div>
<header class="topo">
  <a class="voltar" href="../index.html">← Voltar para a loja</a>
  <div class="topo-dir">
    <span class="grupo">{grupo}</span>
    <a class="cart" href="../index.html">VER CARRINHO <b id="cartn">0</b></a>
    <button class="ico" type="button" onclick="compartilhar()" title="Compartilhar" aria-label="Compartilhar">⤴</button>
  </div>
</header>

<nav class="migalha" aria-label="Você está em">
  <a href="../index.html">Loja</a> <span>/</span> <span>{grupo}</span> <span>/</span> <b>{nome}</b>
</nav>

<main>
  <section class="galeria">
    <div class="foto" onclick="lightbox(true)">
      <img id="big" src="../{capa}" alt="{nome}">
      <span class="zoom">🔍 ampliar</span>
    </div>
    <div class="mini">{mini}</div>
  </section>

  <aside class="info">
    <p class="cod">{cod}</p>
    <h1>{nome}</h1>
    <p class="sub">{sub}</p>

    <p class="preco">{preco_html}</p>
    <div class="acoes">
      {comprar}
      {carrinho}
      {zap}
    </div>
    <p class="seguro">🔒 {pagamento} · PDF digital · entrega após a confirmação</p>

    <ul class="inclui">
      <li>Material em PDF, com gabarito quando aplicável</li>
      <li>Páginas de amostra com tarja para conferir antes de comprar</li>
      <li>Suporte pelo WhatsApp com o professor</li>
    </ul>

    <p class="mini-titulo">Conteúdo</p>
    <p class="desc">{sub}</p>
  </aside>
</main>

<section class="combo">
  {combo_html}
</section>

<section class="faq">
  <h2>Perguntas frequentes</h2>
  <details><summary>Como recebo o material?</summary><p>É um arquivo em PDF. A entrega é feita após a confirmação do pagamento, pelo mesmo canal da compra.</p></details>
  <details><summary>As páginas de amostra são o material completo?</summary><p>Não. As imagens acima são amostras com tarja, para você conferir o estilo e o nível do conteúdo antes de comprar.</p></details>
  <details><summary>Posso tirar dúvidas antes?</summary><p>Sim. Use o botão do WhatsApp nesta página e fale direto com o professor.</p></details>
</section>

<section class="relacionados">
  <div class="rel-head">
    <h2>Também pode interessar</h2>
    <a class="ver-todos" href="../index.html">Ver todos os materiais →</a>
  </div>
  <div class="rel-grid">{relacionados}</div>
</section>

<footer>
  {cod} · {grupo} · Prof. Rodrigo Gonçalves Pereira<br>
  <a href="../index.html">Voltar para a loja</a>
</footer>

<div class="barra">
  <div><small>{nome}</small><b>R$ {brl(preco)}</b></div>
  {'<a href="' + link + '" target="_blank" rel="noopener">Comprar</a>' if link else '<a href="' + whats + '" target="_blank" rel="noopener">WhatsApp</a>'}
</div>

<div class="lb" id="lb" onclick="if(event.target===this)lightbox(false)">
  <button class="lb-x" type="button" onclick="lightbox(false)" aria-label="Fechar">✕</button>
  <button class="lb-prev" type="button" onclick="passo(-1)" aria-label="Anterior">‹</button>
  <img id="lbimg" src="" alt="">
  <button class="lb-next" type="button" onclick="passo(1)" aria-label="Próxima">›</button>
</div>

<div class="toast" id="toast"></div>

<script>
const IMGS={json.dumps(['../' + u for u in novas], ensure_ascii=False)};
const CKEY='loja.carrinho.v1';
function cartRead(){{try{{return JSON.parse(localStorage.getItem(CKEY)||'[]')||[]}}catch(e){{return []}}}}
function cartBadge(){{const e=document.getElementById('cartn');if(e)e.textContent=cartRead().reduce((s,x)=>s+(Number(x.q)||1),0)}}
function toast(t){{
  const el=document.getElementById('toast');
  el.textContent=t;el.classList.add('on');
  clearTimeout(toast.t);toast.t=setTimeout(()=>el.classList.remove('on'),1800);
}}
function addCart(slug,quiet){{
  const c=cartRead();const f=c.find(x=>x.slug===slug);
  if(f)f.q=(Number(f.q)||1)+1;else c.push({{slug:slug,q:1}});
  try{{localStorage.setItem(CKEY,JSON.stringify(c))}}catch(e){{}}
  cartBadge();
  if(!quiet)toast('Adicionado ao carrinho');
}}
function addCombo(lista){{
  lista.forEach(s=>addCart(s,true));
  toast(lista.length+' itens no carrinho');
}}
cartBadge();
let atual=0;
function troca(k){{
  atual=k;
  document.getElementById('big').src=IMGS[k];
  document.querySelectorAll('.mini-img').forEach((b,i)=>b.classList.toggle('on',i===k));
}}
function lightbox(abrir){{
  const lb=document.getElementById('lb');
  if(!abrir){{lb.classList.remove('on');return}}
  document.getElementById('lbimg').src=IMGS[atual];
  lb.classList.add('on');
}}
function passo(d){{
  atual=(atual+d+IMGS.length)%IMGS.length;
  troca(atual);
  document.getElementById('lbimg').src=IMGS[atual];
}}
document.addEventListener('keydown',e=>{{
  const lb=document.getElementById('lb');
  if(!lb.classList.contains('on'))return;
  if(e.key==='Escape')lightbox(false);
  if(e.key==='ArrowRight')passo(1);
  if(e.key==='ArrowLeft')passo(-1);
}});
function compartilhar(){{
  const u=location.href, t=document.title;
  if(navigator.share){{navigator.share({{title:t,url:u}}).catch(()=>{{}});return}}
  navigator.clipboard.writeText(u).then(()=>alert('Link copiado!')).catch(()=>alert(u));
}}
</script>
</body>
</html>"""


CSS = """*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0b1226;--bg2:#121a33;--bd:rgba(255,255,255,.14);--tx:#f4f6ff;--dim:#a9b4d6;--ac:#f472b6;--gold:#fbbf24}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:radial-gradient(900px 420px at 15% -10%,#27408f55,transparent),#0b1226 url("fundo-matematica.svg") repeat;background-size:auto,auto,600px 600px;color:var(--tx);min-height:100vh;padding:0 16px 96px}
a{color:inherit}
.topo{max-width:1120px;margin:0 auto;padding:16px 0 8px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.wbar{position:sticky;top:0;z-index:60;display:flex;align-items:stretch;height:34px;margin:0 -16px 10px;padding:0 0 0 12px;background:#202020;border-bottom:1px solid #3a3a3a;user-select:none;font-family:"Segoe UI",system-ui,sans-serif}
.wic{align-self:center;font-size:14px;margin-right:9px}
.wtit{flex:1;min-width:0;align-self:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:12px;font-weight:400;color:#fff}
.wbtns{display:flex;align-items:stretch}
.wb{width:46px;display:flex;align-items:center;justify-content:center;background:transparent;border:0;color:#fff;text-decoration:none;cursor:default;line-height:0}
.wb:hover{background:rgba(255,255,255,.1)}
.wx{cursor:pointer}.wx:hover,.wx:focus-visible{background:#c42b1c;color:#fff;outline:0}
@media(max-width:520px){.wb{width:40px}}
html.emb .wbar{display:none!important}
html.emb .topo,html.emb .migalha,html.emb footer{display:none!important}
html.emb body{padding-top:14px;background-color:#0b1226}
.voltar{display:inline-block;background:#fbbf24;color:#111;text-decoration:none;font-weight:700;font-size:1rem;padding:9px 16px;border-radius:6px}
.voltar:hover{background:#f59e0b;color:#111}
.topo-dir{display:flex;align-items:center;gap:10px}
.grupo{font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);border:1px solid var(--bd);border-radius:99px;padding:5px 12px;background:rgba(255,255,255,.05)}
.ico{background:rgba(255,255,255,.08);border:1px solid var(--bd);color:var(--tx);width:34px;height:34px;border-radius:10px;cursor:pointer;font-size:1rem}
.migalha{max-width:1120px;margin:0 auto 14px;font-size:.82rem;color:var(--dim);display:flex;gap:8px;flex-wrap:wrap}
.migalha a{text-decoration:none;color:var(--dim)}
.migalha a:hover{color:#fff}
.migalha b{color:var(--tx);font-weight:700}
main{max-width:1120px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,400px);gap:28px;align-items:start}
.foto{position:relative;background:rgba(255,255,255,.05);border:1px solid var(--bd);border-radius:20px;padding:10px;cursor:zoom-in}
.foto img{width:100%;height:auto;display:block;border-radius:12px;background:#fff}
.zoom{position:absolute;right:20px;bottom:20px;background:rgba(11,18,38,.82);border:1px solid var(--bd);border-radius:99px;padding:6px 12px;font-size:.76rem;font-weight:700;color:#fff}
.mini{display:grid;grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:8px;margin-top:10px}
.mini-img{padding:0;border:2px solid transparent;border-radius:10px;background:none;cursor:pointer;overflow:hidden}
.mini-img img{width:100%;height:100%;display:block;border-radius:8px;background:#fff}
.mini-img.on{border-color:var(--ac)}
.info{padding-top:4px}
.cod{font-size:.74rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ac);font-weight:900;margin-bottom:6px}
h1{font-size:clamp(1.7rem,3.2vw,2.6rem);line-height:1.12;margin-bottom:10px;letter-spacing:-.01em}
.sub{color:var(--dim);line-height:1.55;margin-bottom:16px}
.preco{font-size:2rem;font-weight:900;margin-bottom:14px}
.preco .de{color:var(--dim);text-decoration:line-through;font-size:1rem;font-weight:600;margin-right:10px}
.acoes{display:flex;flex-direction:column;gap:10px;margin-bottom:12px}
.btn{display:block;text-align:center;text-decoration:none;font-weight:900;border-radius:12px;padding:15px 16px;font-size:1rem;transition:transform .15s,filter .15s}
.btn:active{transform:scale(.98)}
.comprar{background:#ffbc00;color:#3a2500}
.comprar:hover{filter:brightness(1.06)}
.zap{background:rgba(34,197,94,.14);border:1px solid rgba(34,197,94,.5);color:#bbf7d0}
.seguro{font-size:.8rem;color:var(--dim);margin-bottom:18px}
.inclui{list-style:none;display:grid;gap:8px;margin-bottom:20px}
.inclui li{position:relative;padding-left:24px;font-size:.92rem;color:#dbe2f5;line-height:1.4}
.inclui li::before{content:"✓";position:absolute;left:0;color:#34d399;font-weight:900}
.mini-titulo{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-bottom:6px;font-weight:800}
.desc{color:#cdd6ee;line-height:1.6;font-size:.95rem}
.relacionados{max-width:1120px;margin:40px auto 0}
.relacionados h2{font-size:1.2rem;margin-bottom:14px}
.rel-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px}
.rel{display:flex;flex-direction:column;gap:6px;text-decoration:none;background:rgba(255,255,255,.05);border:1px solid var(--bd);border-radius:14px;padding:10px;transition:transform .15s,background .15s}
.rel:hover{transform:translateY(-2px);background:rgba(255,255,255,.09)}
.rel img{width:100%;height:auto;border-radius:8px;background:#fff}
.rel-nome{font-size:.88rem;font-weight:800;line-height:1.25}
.rel-preco{font-size:.85rem;color:var(--gold);font-weight:800}
.rel-link{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:inherit}
.rel-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:2px}
.rel-add{background:#16a34a;color:#fff;border:3px solid #000;border-radius:10px;padding:6px 12px;font-weight:900;cursor:pointer;font-size:1rem;line-height:1;box-shadow:0 3px 10px rgba(0,166,80,.35)}
.rel-add:hover{background:#15803d;transform:translateY(-1px)}
.cart{display:inline-flex;align-items:center;gap:8px;background:#16a34a;border:2px solid #fff;border-radius:10px;padding:0 12px;height:36px;text-decoration:none;color:#fff;font-weight:900;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase}
.cart b{background:rgba(0,0,0,.25);border-radius:99px;padding:2px 8px;color:#fff;font-size:.8rem;letter-spacing:0}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%) translateY(20px);background:#111a33;border:1px solid var(--bd);color:#fff;padding:11px 18px;border-radius:12px;font-weight:800;opacity:0;pointer-events:none;transition:.25s;z-index:90;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.toast.on{opacity:1;transform:translateX(-50%)}
.combo{max-width:1120px;margin:34px auto 0;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap;background:linear-gradient(120deg,rgba(251,191,36,.14),rgba(244,114,182,.10));border:1px solid rgba(251,191,36,.35);border-radius:18px;padding:18px 20px}
.combo h2{font-size:1.15rem;margin-bottom:6px}
.combo p{font-size:.95rem;color:#e6ebfb;line-height:1.45}
.selo{display:inline-block;background:#ffbc00;color:#3a2500;font-weight:900;border-radius:99px;padding:3px 10px;font-size:.78rem;margin-bottom:8px}
.preco-combo{color:#ffbc00}
.combo-sub{color:var(--dim)!important;font-size:.82rem!important;margin-top:4px}
.combo-acoes{display:flex;flex-direction:column;gap:8px;min-width:250px}
.carrinho{background:#00a650;border:1px solid #009247;color:#fff;font-weight:800;box-shadow:0 3px 10px rgba(0,166,80,.28)}
.carrinho:hover{background:#009247;transform:translateY(-1px)}
.faq{max-width:1120px;margin:40px auto 0}
.faq h2{font-size:1.2rem;margin-bottom:12px}
.faq details{background:rgba(255,255,255,.05);border:1px solid var(--bd);border-radius:12px;padding:12px 14px;margin-bottom:8px}
.faq summary{cursor:pointer;font-weight:800;font-size:.95rem}
.faq p{color:var(--dim);font-size:.9rem;line-height:1.55;margin-top:8px}
.rel-head{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px}
.rel-head h2{margin:0}
.ver-todos{color:var(--dim);font-size:.86rem;font-weight:700;text-decoration:none}
.ver-todos:hover{color:#fff}
footer{max-width:1120px;margin:44px auto 0;color:#7c88ab;font-size:.82rem;text-align:center;line-height:1.7}
footer a{color:var(--dim)}
.barra{display:none}
.lb{position:fixed;inset:0;z-index:99;background:rgba(3,7,18,.94);display:none;align-items:center;justify-content:center;padding:20px}
.lb.on{display:flex}
.lb img{max-width:92vw;max-height:90vh;border-radius:8px;background:#fff}
.lb-x,.lb-prev,.lb-next{position:absolute;background:rgba(255,255,255,.12);border:1px solid var(--bd);color:#fff;width:46px;height:46px;border-radius:50%;font-size:1.3rem;cursor:pointer}
.lb-x{top:18px;right:18px}
.lb-prev{left:14px;top:50%;transform:translateY(-50%)}
.lb-next{right:14px;top:50%;transform:translateY(-50%)}
@media(max-width:860px){
  main{grid-template-columns:1fr}
  body{padding-bottom:110px}
  .barra{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:50;background:rgba(11,18,38,.96);border-top:1px solid var(--bd);padding:10px 16px;align-items:center;justify-content:space-between;gap:12px;backdrop-filter:blur(10px)}
  .barra div{display:flex;flex-direction:column;line-height:1.2;min-width:0}
  .barra small{font-size:.72rem;color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:52vw}
  .barra b{color:var(--gold);font-size:1.05rem}
  .barra a{background:#ffbc00;color:#3a2500;text-decoration:none;font-weight:900;border-radius:10px;padding:12px 18px;white-space:nowrap}
  .foto{border-radius:16px}
}
@media print{.barra,.lb,.acoes,.ico{display:none!important}}
"""


def sitemap(its):
    urls = [BASE + "/"] + [f"{BASE}/{codigo(x)}/" for x in its]
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    body += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    body += "</urlset>\n"
    io.open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8").write(body)
    io.open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\nSitemap: " + BASE + "/sitemap.xml\n")


def main():
    its = itens()
    io.open(os.path.join(HERE, "produto.css"), "w", encoding="utf-8").write(CSS)
    n = 0
    for it in its:
        cod = codigo(it)
        d = os.path.join(HERE, cod)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pagina(it, its))
        n += 1
    sitemap(its)
    print("paginas geradas:", n)


if __name__ == "__main__":
    main()
