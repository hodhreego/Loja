# -*- coding: utf-8 -*-
"""Aplica em build_loja.py a separação: loja principal = atividades (com índice por disciplina/série/coleção);
apostilas/certames = seção secundária em concursos.html. Rodar uma vez (14/11/2026)."""
import io, shutil
p = 'build_loja.py'
shutil.copy(p, 'build_loja.antes-secao-concursos.py')
s = io.open(p, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, 'NAO ACHOU: ' + a[:90]
    s = s.replace(a, b, n)


# ---------- Python: tipos, categorias, séries ----------
rep("def tipo_de(slug):\n", "def tipo_de(slug):\n    if slug.startswith('cn-') or slug == 'consciencia-negra': return 'cn'\n    if slug == 'album-multiplicacao': return 'album'\n")

HELP = '''
import re as _re
CAT_DISC = {
 'cn-da-africa-ao-brasil': ['historia'], 'cn-negros-mundo': ['historia'], 'cn-direitos-civis-eua': ['historia'],
 'cn-apartheid': ['historia'], 'cn-historia-3ano': ['historia'], 'cn-quem-sou-eu': ['historia'],
 'cn-portugues-autoria-negra': ['portugues'], 'cn-portugues-3ano': ['portugues'], 'cn-palavras-herdadas': ['portugues'],
 'cn-gazeta-quilombos': ['ingles'], 'cn-cientistas-negras': ['ciencias'],
 'cn-raizes-africanas': ['matematica'], 'cn-numeros-historia': ['matematica'], 'cn-matematica-3ano': ['matematica'],
 'consciencia-negra': ['matematica'], 'album-multiplicacao': ['matematica']}
SERIE_CN = {'cn-da-africa-ao-brasil': '789', 'cn-negros-mundo': '789', 'cn-direitos-civis-eua': '789', 'cn-apartheid': '789',
 'cn-portugues-autoria-negra': '6789', 'cn-cientistas-negras': '6789', 'cn-raizes-africanas': '6789', 'cn-numeros-historia': '6789',
 'cn-quem-sou-eu': '6789', 'cn-gazeta-quilombos': '6789', 'cn-palavras-herdadas': '6789'}
def cats_de(slug):
    c = list(CAT_DISC.get(slug, []))
    if slug.startswith(('volume-', 'se-liga-', 'sei-', 'saeb-')): c = ['matematica']
    if slug.startswith('ef-'): c = ['financeira']
    if slug.startswith('cn-') or slug == 'consciencia-negra': c.append('consciencia')
    return c
def series_de(slug, nome):
    if slug.endswith('3ano'): return ['3']
    if slug in SERIE_CN: return list(SERIE_CN[slug])
    m = _re.search(r'(\\d)º ano', nome)
    if m: return [m.group(1)]
    if _re.search(r'série EM', nome): return ['em']
    return []

'''
rep("for slug, nome, g, code, preco, sub in P:\n", HELP + "for slug, nome, g, code, preco, sub in P:\n")
rep('"preco": preco, "sub": sub, "imgs": imgs, "tipo": tipo_de(slug),', '"preco": preco, "sub": sub, "imgs": imgs, "tipo": tipo_de(slug), "cat": cats_de(slug), "serie": series_de(slug, nome),')

# ---------- Template: placeholders ----------
rep("<title>Loja de Educação e Matemática — Atividades Educativas, Simulados e Apostilas</title>", "<title>__TITLE__</title>")
rep('<link rel="canonical" href="https://eduloja.com/">\n<meta property="og:url" content="https://eduloja.com/">', '<link rel="canonical" href="__CANON__">\n<meta property="og:url" content="__CANON__">')
rep('<meta name="description" content="Atividades educativas prontas para imprimir (Se Liga, volumes, simulados SAEB) com gabarito, e apostilas para concursos como PSS SEED-PR 2027. Veja as páginas antes de comprar.">', '<meta name="description" content="__DESC__">')
rep('<meta property="og:title" content="Loja de Educação e Matemática — Atividades Educativas, Simulados e Apostilas">', '<meta property="og:title" content="__TITLE__">')
rep('<meta property="og:description" content="Atividades educativas prontas para imprimir, simulados SAEB e apostilas para concursos (PSS SEED-PR 2027 e mais).">', '<meta property="og:description" content="__DESC__">')

rep('''  <div class="eyebrow">Prof. Rodrigo Gonçalves Pereira</div>
  <h1>Loja de <em>Educação e Matemática</em><br>Atividades Educativas, Simulados &amp; Apostilas</h1>
  <p>Atividades educativas prontas para imprimir, com gabarito, para professores e alunos do 6º ano ao Ensino Médio. E, para quem estuda para concurso, apostilas atualizadas com os editais. Confira as páginas antes de comprar.</p>''',
    '''  <div class="eyebrow">Prof. Rodrigo Gonçalves Pereira</div>
  __H1__
  <p>__HP__</p>
  __NAVLINK__''')

rep('''  <div class="certs" id="tipos" style="margin-top:10px"></div>
  <input id="q" type="search" placeholder="Buscar apostila…">''',
    '''  <div class="certs" id="tipos" style="margin-top:10px"></div>
  <div class="certs" id="series" style="margin-top:6px"></div>
  <input id="q" type="search" placeholder="__BUSCA__">''')

# sidebar
i0 = s.index('  <aside class="indice">')
i1 = s.index('  </aside>', i0) + len('  </aside>')
s = s[:i0] + '  <aside class="indice">\n__INDICE__\n  </aside>' + s[i1:]

rep('''<p class="warn">Proibido o compartilhamento.''', '''__FOOTLINK__
  <p class="warn">Proibido o compartilhamento.''')

# CSS
rep("</style>\n</head>\n<body>\n<div class=\"minibar\"", """.sec-link{display:inline-block;margin-top:2px;font:600 13px 'Source Sans 3';color:var(--gold-light,#fde68a);opacity:.9;text-decoration:underline;text-underline-offset:3px}
.sec-link:hover{opacity:1}
.rot{font:800 11px 'Source Sans 3';letter-spacing:.09em;text-transform:uppercase;color:var(--mut);align-self:center;min-width:62px}
#series .chip,#tipos .chip{font-size:13.5px;padding:6px 12px}
.foot-sec{margin:0 0 8px}.foot-sec a{color:var(--gold-light);font-weight:700}
@media(max-width:720px){.rot{display:none}#series .chip,#tipos .chip{flex:none}}
</style>
</head>
<body>
<div class="minibar\"""")

# ---------- JS ----------
rep("const ITENS=__DATA__;", "const ITENS=__DATA__;\nconst MODO=\"__MODO__\";\nconst VIS=ITENS.filter(i=>MODO===\"concursos\"?i.grupo!==\"reforco\":i.grupo===\"reforco\");")
rep('const GR=[["reforco","Reforço e recomposição"],["pss","PSS SEED-PR 2027"]', 'const GR=(MODO==="concursos"?[]:[["reforco","Atividades"]]).concat([["pss","PSS SEED-PR 2027"]')
rep('["prefeitura","Prefeitura de Cascavel 2026"],["outros","Outros concursos"]];', '["prefeitura","Prefeitura de Cascavel 2026"],["outros","Outros concursos"]]);')
rep('if(["pss","cisop","prefeitura","simulado","outros"].includes(h))filtro=h}', 'if(["pss","cisop","prefeitura","simulado","outros"].includes(h))filtro=h;if(MODO!=="concursos"&&["consciencia","matematica","financeira","historia","portugues","ingles","ciencias"].includes(h))filtro=h}')
# renomeia as funções antigas (usadas só no modo concursos)
rep("function render(){\n  const q=busca.toLowerCase();let total=0;", "function renderC(){\n  const q=busca.toLowerCase();let total=0;")
rep("function chips(){\n  const c=g=>ITENS.filter(i=>g===\"todos\"||i.grupo===g).length;", "function chipsC(){\n  const c=g=>VIS.filter(i=>g===\"todos\"||i.grupo===g).length;")
rep("function tipos(){\n  const svg=", "function tiposC(){\n  const svg=")
rep("function setTipo(t){filtroTipo=t;filtro=\"todos\";tipos();chips();render();document.getElementById('main').scrollIntoView({behavior:'smooth',block:'start'})}\n", "")

NOVO = r'''
/* ===== atividades (loja principal) x concursos (seção secundária) ===== */
const CATS=[["todos","Todas as atividades","🗂️"],["consciencia","Dia da Consciência Negra","✊🏾"],["matematica","Matemática","➗"],["financeira","Educação Financeira","💰"],["historia","História","📜"],["portugues","Língua Portuguesa","📚"],["ingles","Inglês","🌍"],["ciencias","Ciências","🔬"]];
const SERIES=[["todas","Todas as séries"],["3","3º ano"],["5","5º ano"],["6","6º ano"],["7","7º ano"],["8","8º ano"],["9","9º ano"],["em","Ensino Médio"]];
const COLEC=[["todos","Todas as coleções"],["cn","Dia da Consciência Negra"],["se-liga","Se Liga de Matemática"],["se-liga-ef","Se Liga de Educação Financeira"],["sei","Semanas de Estudos"],["saeb","Simulados SAEB"],["volumes","Volumes"],["album","Álbuns"]];
const NOMEST={"cn":"Dia da Consciência Negra","se-liga":"Se Liga de Matemática","se-liga-ef":"Se Liga de Educação Financeira","se-liga-ing":"Se Liga de Inglês","sei":"Semanas de Estudos Intensivos","saeb":"Simulados SAEB","volumes":"Volumes","album":"Álbuns de multiplicação"};
const ORD={"cn":0,"se-liga":1,"se-liga-ef":2,"se-liga-ing":3,"sei":4,"saeb":5,"volumes":6,"album":7};
let filtroSerie="todas";
function renderA(){
  const q=busca.toLowerCase();
  const l=VIS.filter(i=>(filtro==="todos"||(i.cat||[]).includes(filtro))&&(filtroSerie==="todas"||(i.serie||[]).includes(filtroSerie))&&(filtroTipo==="todos"||i.tipo===filtroTipo)&&(i.nome+" "+i.sub).toLowerCase().includes(q))
    .map((x,n)=>[x,n]).sort((a,b)=>((ORD[a[0].tipo]??9)-(ORD[b[0].tipo]??9))||a[1]-b[1]).map(x=>x[0]);
  const porTipo={};l.forEach(i=>{(porTipo[i.tipo]=porTipo[i.tipo]||[]).push(i)});
  $("#main").innerHTML=Object.keys(porTipo).map(tp=>`<section class="grupo"><h3 class="subtipo">${NOMEST[tp]||tp} <small>${porTipo[tp].length}</small></h3><div class="grid">${porTipo[tp].map(card).join("")}</div></section>`).join("");
  $("#empty").style.display=l.length?"none":"block";
  const nc=(CATS.find(c=>c[0]===filtro)||CATS[0])[1],ns=(SERIES.find(c=>c[0]===filtroSerie)||SERIES[0])[1];
  const rs=$("#resumo");if(rs)rs.innerHTML=`<b>${l.length}</b> ${l.length===1?"atividade":"atividades"} · <b>${filtro==="todos"?"todas as disciplinas":nc}</b>${filtroSerie!=="todas"?" · <b>"+ns+"</b>":""}${busca?" · “"+busca+"”":""}`;
  document.querySelectorAll(".indice a[data-cat]").forEach(a=>a.classList.toggle("on",a.dataset.cat===filtro));
  document.querySelectorAll(".indice a[data-serie]").forEach(a=>a.classList.toggle("on",a.dataset.serie===filtroSerie));
  document.querySelectorAll(".indice a[data-tipo]").forEach(a=>a.classList.toggle("on",a.dataset.tipo===filtroTipo));
  const el=$("#infoc");if(el){el.className="info-cert";el.innerHTML=""}
  anima();
  try{history.replaceState(null,"",filtro==="todos"?location.pathname:"#"+filtro)}catch(e){}
}
function chipsA(){
  const c=k=>VIS.filter(i=>k==="todos"||(i.cat||[]).includes(k)).length;
  $("#chips").innerHTML=CATS.filter(x=>x[0]==="todos"||c(x[0])).map(([k,n,e])=>`<button class="cert ${filtro===k?'on':''}" onclick="setCat('${k}')"><span class="ic" style="font-size:19px">${e}</span><span class="ct"><b>${n}</b><small>${c(k)} ${c(k)===1?'atividade':'atividades'}</small></span></button>`).join("");
  const mt=document.getElementById("mbt");if(mt){mt.innerHTML=CATS.filter(x=>x[0]==="todos"||c(x[0])).map(([k,n])=>`<button class="${filtro===k?"on":""}" onclick="mbTog(false);setCat('${k}')">${n}<small>${c(k)} ${c(k)===1?"atividade":"atividades"}</small></button>`).join("");const nn=document.getElementById("mbn");if(nn)nn.textContent=(CATS.find(x=>x[0]===filtro)||CATS[0])[1]}
}
function tiposA(){
  const cs=k=>VIS.filter(i=>filtro==="todos"||(i.cat||[]).includes(filtro)).filter(i=>k==="todas"||(i.serie||[]).includes(k)).length;
  $("#series").innerHTML='<span class="rot">Série</span>'+SERIES.filter(x=>x[0]==="todas"||cs(x[0])).map(([k,n])=>`<button class="chip ${filtroSerie===k?'on':''}" onclick="setSerie('${k}')">${n}<small>${cs(k)}</small></button>`).join("");
  const ct=k=>VIS.filter(i=>k==="todos"||i.tipo===k).length;
  $("#tipos").innerHTML='<span class="rot">Coleção</span>'+COLEC.filter(x=>x[0]==="todos"||ct(x[0])).map(([k,n])=>`<button class="chip ${filtroTipo===k?'on':''}" onclick="setTipo('${k}')">${n}<small>${ct(k)}</small></button>`).join("");
}
function chipsM(){chipsC();const mt=document.getElementById("mbt");if(mt){mt.innerHTML=GR.map(([k,n])=>`<button class="${filtro===k?"on":""}" onclick="mbTog(false);setGrupo('${k}')">${n}</button>`).join("");const nn=document.getElementById("mbn");if(nn)nn.textContent=(GR.find(x=>x[0]===filtro)||["","Todos"])[1]}}
function render(){if(MODO==="concursos")renderC();else renderA()}
function chips(){if(MODO==="concursos")chipsM();else chipsA()}
function tipos(){if(MODO==="concursos"){const t=$("#tipos"),s=$("#series");if(t)t.style.display="none";if(s)s.style.display="none"}else tiposA()}
function rola(id){const e=document.getElementById(id);if(e)e.scrollIntoView({behavior:'smooth',block:'nearest'})}
function setCat(k){filtro=k;chips();tipos();render();rola('main')}
function setSerie(k){filtroSerie=k;chips();tipos();render();rola('main')}
function setTipo(t){filtroTipo=t;chips();tipos();render();rola('main')}
'''
# insere antes do bloco de miniaturas animadas (depois de setGrupo)
rep("/* miniaturas animadas: as páginas sobem", NOVO + "/* miniaturas animadas: as páginas sobem")
# o setGrupo antigo fica (usado nos certames); remove a chamada de scroll para #infoc quando ausente
rep("document.querySelectorAll(\".indice a[data-tipo]\").forEach(a=>a.classList.toggle(\"on\",a.dataset.tipo===filtroTipo&&filtro===\"todos\"));", "document.querySelectorAll(\".indice a[data-tipo]\").forEach(a=>a.classList.toggle(\"on\",a.dataset.tipo===filtroTipo&&filtro===\"todos\"));")

# ---------- Saída: duas páginas ----------
FIM_ANT = '''out = HTML.replace("__DATA__", json.dumps(items, ensure_ascii=False)).replace("__WA__", WA)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("ok", len(items), "itens")'''
assert FIM_ANT in s
FIM_NOVO = r'''def _indice_atividades():
    r = ['    <b>Por disciplina</b>']
    for k, n in [("todos", "Todas as atividades"), ("consciencia", "Dia da Consciência Negra"), ("matematica", "Matemática"), ("financeira", "Educação Financeira"), ("historia", "História"), ("portugues", "Língua Portuguesa"), ("ingles", "Inglês"), ("ciencias", "Ciências")]:
        r.append('    <a data-cat="%s" onclick="setCat(\'%s\')">%s</a>' % (k, k, n))
    r.append('    <hr>\n    <b>Por série</b>')
    for k, n in [("todas", "Todas as séries"), ("3", "3º ano"), ("5", "5º ano"), ("6", "6º ano"), ("7", "7º ano"), ("8", "8º ano"), ("9", "9º ano"), ("em", "Ensino Médio")]:
        r.append('    <a data-serie="%s" onclick="setSerie(\'%s\')">%s</a>' % (k, k, n))
    r.append('    <hr>\n    <b>Coleções</b>')
    for k, n in [("todos", "Todas as coleções"), ("cn", "Dia da Consciência Negra"), ("se-liga", "Se Liga de Matemática"), ("se-liga-ef", "Se Liga de Educação Financeira"), ("sei", "Semanas de Estudos"), ("saeb", "Simulados SAEB"), ("volumes", "Volumes"), ("album", "Álbuns")]:
        r.append('    <a data-tipo="%s" onclick="setTipo(\'%s\')">%s</a>' % (k, k, n))
    r.append('    <hr>\n    <a class="sec-link" style="font-size:12.5px;color:var(--mut);opacity:1" href="concursos.html">Apostilas para concursos →</a>')
    return "\n".join(r)


def _indice_concursos():
    r = ['    <b>Certames</b>', '    <a data-grupo="todos" onclick="setGrupo(\'todos\')">Todos os certames</a>']
    for k, n in [("pss", "PSS SEED-PR"), ("cisop", "CISOP Cascavel"), ("prefeitura", "Prefeitura de Cascavel"), ("outros", "Outros concursos")]:
        r.append('    <a data-grupo="%s" onclick="setGrupo(\'%s\')">%s</a>' % (k, k, n))
    r.append('    <hr>\n    <a class="sec-link" style="font-size:12.5px;color:var(--mut);opacity:1" href="index.html">← Atividades para imprimir</a>')
    return "\n".join(r)


MODOS = {
    "atividades": dict(
        arq="index.html", canon="https://eduloja.com/",
        title="Loja de Educação e Matemática — Atividades Educativas para Imprimir",
        desc="Atividades educativas prontas para imprimir, com gabarito, do 3º ano do Fundamental ao Ensino Médio: Matemática, Educação Financeira, História, Língua Portuguesa e mais. Veja as páginas antes de comprar.",
        h1='<h1>Loja de <em>Educação e Matemática</em><br>Atividades Educativas para Imprimir</h1>',
        hp="Atividades prontas para imprimir, com gabarito, para professores e alunos do 3º ano do Fundamental ao Ensino Médio: Matemática, Educação Financeira, História, Língua Portuguesa e mais. Escolha a disciplina ou a série e confira as páginas antes de comprar.",
        nav='<a class="sec-link" href="concursos.html">Estuda para concurso? Veja as apostilas →</a>',
        busca="Buscar atividade…", indice=_indice_atividades(),
        foot='<p class="foot-sec">Estuda para concurso? <a href="concursos.html">Apostilas para concursos (PSS SEED-PR, CISOP e outros) →</a></p>'),
    "concursos": dict(
        arq="concursos.html", canon="https://eduloja.com/concursos",
        title="Apostilas para Concursos — Loja de Educação e Matemática",
        desc="Apostilas atualizadas com os editais para concursos e processos seletivos: PSS SEED-PR 2027, CISOP Cascavel, Prefeitura de Cascavel e outros. Veja as páginas antes de comprar.",
        h1='<h1><em>Apostilas para Concursos</em><br>PSS SEED-PR, CISOP e Prefeituras</h1>',
        hp="Apostilas atualizadas com os editais, para professores e candidatos: PSS SEED-PR 2027, CISOP Cascavel, Prefeitura de Cascavel e outros certames. Confira as páginas antes de comprar.",
        nav='<a class="sec-link" href="index.html">← Atividades educativas para imprimir</a>',
        busca="Buscar apostila…", indice=_indice_concursos(),
        foot='<p class="foot-sec"><a href="index.html">← Voltar às atividades educativas para imprimir</a></p>'),
}
DADOS = json.dumps(items, ensure_ascii=False)
for modo, m in MODOS.items():
    out = (HTML.replace("__TITLE__", m["title"]).replace("__CANON__", m["canon"]).replace("__DESC__", m["desc"])
           .replace("__H1__", m["h1"]).replace("__HP__", m["hp"]).replace("__NAVLINK__", m["nav"])
           .replace("__BUSCA__", m["busca"]).replace("__INDICE__", m["indice"]).replace("__FOOTLINK__", m["foot"])
           .replace("__MODO__", modo).replace("__DATA__", DADOS).replace("__WA__", WA))
    open(os.path.join(HERE, m["arq"]), "w", encoding="utf-8").write(out)
print("ok", len(items), "itens · index.html + concursos.html")'''
s = s.replace(FIM_ANT, FIM_NOVO)
io.open(p, 'w', encoding='utf-8').write(s)
print('patch ok')
