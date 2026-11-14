# -*- coding: utf-8 -*-
import io, re
p = 'build_loja.py'
s = io.open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, 'NAO ACHOU: ' + a[:80]
    s = s.replace(a, b)

SV = lambda inner, w=16: '<svg class="ic16" viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, w, inner)
CART = SV('<circle cx="9.5" cy="20.5" r="1.6"/><circle cx="18.5" cy="20.5" r="1.6"/><path d="M2.5 3.5h2.3l2.6 11.8a1.9 1.9 0 0 0 1.9 1.5h8.7a1.9 1.9 0 0 0 1.9-1.5L21.5 7H6.2"/>')
EYE = SV('<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>')
CHECK = SV('<path d="m5 12.5 4.5 4.5L19 7.5"/>', 14)
MENU = SV('<path d="M4 7h16M4 12h16M4 17h16"/>', 16)
CHAT = SV('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/>')

rep("%3Ctext x='50' y='80' font-size='84' text-anchor='middle'%3E🏛️%3C/text%3E%3C/svg%3E", "%3Crect width='100' height='100' rx='18' fill='%231B3A6B'/%3E%3Cpath d='M18 80h64M24 80V44M42 80V44M58 80V44M76 80V44M14 40 50 20l36 20Z' fill='none' stroke='%23fcd34d' stroke-width='7' stroke-linejoin='round' stroke-linecap='round'/%3E%3C/svg%3E")
rep('onclick="mbTog()">☰ <span', 'onclick="mbTog()">' + MENU + ' <span')
rep('<span>🛒 Carrinho</span>', '<span>' + CART + ' Carrinho</span>')
rep('<div class="cupbal">💬 <a', '<div class="cupbal">' + CHAT + ' <a')
rep('<span class="peek">👁 ver</span>', '<span class="peek">' + EYE + ' ver</span>')
rep('"\\n\\n🛒 Enviado pela loja: "', '"\\n\\nEnviado pela loja: "')
s = s.replace('"🎉 Desconto máximo ativo', '"Desconto máximo ativo').replace('"🎉 Desconto máximo de 35%', '"Desconto máximo de 35%')
rep('já está no carrinho 🙂 Cada', 'já está no carrinho. Cada')
rep('`✅ Cupom aplicado', '`' + CHECK + ' Cupom aplicado')
s = s.replace('✓', CHECK)

rep('const CATS=[["todos","Todas as atividades","🗂️"],["consciencia","Dia da Consciência Negra","✊🏾"],["matematica","Matemática","➗"],["financeira","Educação Financeira","💰"],["historia","História","📜"],["portugues","Língua Portuguesa","📚"],["ingles","Inglês","🌍"],["ciencias","Ciências","🔬"]];',
 '''const SVG=p=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
const ICA={todos:SVG('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
 consciencia:SVG('<path d="M12 3 21 12 12 21 3 12Z"/><path d="M12 8 16 12 12 16 8 12Z"/><circle cx="12" cy="12" r=".6" fill="currentColor"/>'),
 matematica:SVG('<circle cx="12" cy="12" r="9"/><path d="M7.5 12h9"/><circle cx="12" cy="8.3" r=".9" fill="currentColor"/><circle cx="12" cy="15.7" r=".9" fill="currentColor"/>'),
 financeira:SVG('<circle cx="12" cy="12" r="9"/><path d="M14.5 8.5c-.6-.8-1.5-1.2-2.6-1.2-1.6 0-2.7.8-2.7 2s1 1.7 2.8 2.1c1.8.4 2.8.9 2.8 2.1 0 1.2-1.1 2-2.8 2-1.2 0-2.2-.5-2.9-1.3M12 5.8v1.5M12 16.7v1.5"/>'),
 historia:SVG('<path d="M7 3h11a2 2 0 0 1 2 2v13a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3v-1h4"/><path d="M7 3v14a2 2 0 0 1-2 2"/><path d="M11 8h5M11 12h5"/>'),
 portugues:SVG('<path d="M12 6c-2-2-5-2-8-1v13c3-1 6-1 8 1 2-2 5-2 8-1V5c-3-1-6-1-8 1Z"/><path d="M12 6v13"/>'),
 ingles:SVG('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>'),
 ciencias:SVG('<path d="M9 3h6M10 3v6L4.5 19a1.6 1.6 0 0 0 1.4 2.4h12.2a1.6 1.6 0 0 0 1.4-2.4L14 9V3"/><path d="M7.5 15h9"/>')};
const CATS=[["todos","Todas as atividades"],["consciencia","Dia da Consciência Negra"],["matematica","Matemática"],["financeira","Educação Financeira"],["historia","História"],["portugues","Língua Portuguesa"],["ingles","Inglês"],["ciencias","Ciências"]];''')
rep('map(([k,n,e])=>`<button class="cert ${filtro===k?\'on\':\'\'}" onclick="setCat(\'${k}\')"><span class="ic" style="font-size:19px">${e}</span>', 'map(([k,n])=>`<button class="cert ${filtro===k?\'on\':\'\'}" onclick="setCat(\'${k}\')"><span class="ic">${ICA[k]}</span>')

rep("function setCat(k){filtro=k;chips();tipos();render();rola('main')}\nfunction setSerie(k){filtroSerie=k;chips();tipos();render();rola('main')}\nfunction setTipo(t){filtroTipo=t;chips();tipos();render();rola('main')}",
'''function limpa(){filtro="todos";filtroSerie="todas";filtroTipo="todos"}
function setCat(k){limpa();filtro=k;chips();tipos();render();rola('main')}
function setSerie(k){limpa();filtroSerie=k;chips();tipos();render();rola('main')}
function setTipo(t){limpa();filtroTipo=t;chips();tipos();render();rola('main')}
function hashDe(){return filtro!=="todos"?"cat-"+filtro:filtroSerie!=="todas"?"serie-"+filtroSerie:filtroTipo!=="todos"?"col-"+filtroTipo:""}
function aplicaHash(h){if(MODO==="concursos")return;limpa();
  if(h.startsWith("cat-")&&CATS.some(c=>c[0]===h.slice(4)))filtro=h.slice(4);
  else if(h.startsWith("serie-")&&SERIES.some(c=>c[0]===h.slice(6)))filtroSerie=h.slice(6);
  else if(h.startsWith("col-")&&COLEC.some(c=>c[0]===h.slice(4)))filtroTipo=h.slice(4);}
addEventListener("hashchange",()=>{const h=location.hash.slice(1);if(/^(cat|serie|col)-/.test(h)){aplicaHash(h);chips();tipos();render();rola('main')}});''')
rep('try{history.replaceState(null,"",filtro==="todos"?location.pathname:"#"+filtro)}catch(e){}\n}\nfunction chipsA', 'try{const hh=hashDe();history.replaceState(null,"",hh?"#"+hh:location.pathname)}catch(e){}\n}\nfunction chipsA')
rep("chips();tipos();render();\nconst WNUM", "aplicaHash(location.hash.slice(1));chips();tipos();render();\nconst WNUM")
s = s.replace(';if(MODO!=="concursos"&&["consciencia","matematica","financeira","historia","portugues","ingles","ciencias"].includes(h))filtro=h}', '}')

i0 = s.index('def _indice_atividades():'); i1 = s.index('def _indice_concursos')
NOVO_IDX = '''def _indice_atividades():
    cn = sorted([x for x in items if x["tipo"] in ("cn",)], key=lambda x: int(x["av"][2:]) if x["av"].startswith("Av") else 0)
    r = ['    <b>Dia da Consciência Negra</b>', '    <a data-cat="consciencia" href="#cat-consciencia">Ver todas as atividades</a>']
    for x in cn:
        nm = x["nome"].replace("Consciência Negra · ", "").replace("Consciência Negra — ", "")
        r.append('    <a class="sub" href="%s/">%s</a>' % (x["av"], nm))
    r.append('    <hr>\\n    <b>Por disciplina</b>')
    for k, n in [("todos", "Todas as atividades"), ("matematica", "Matemática"), ("financeira", "Educação Financeira"), ("historia", "História"), ("portugues", "Língua Portuguesa"), ("ingles", "Inglês"), ("ciencias", "Ciências")]:
        r.append('    <a data-cat="%s" href="%s">%s</a>' % (k, "#cat-" + k if k != "todos" else "#", n))
    r.append('    <hr>\\n    <b>Por série</b>')
    for k, n in [("3", "3º ano"), ("5", "5º ano"), ("6", "6º ano"), ("7", "7º ano"), ("8", "8º ano"), ("9", "9º ano"), ("em", "Ensino Médio")]:
        r.append('    <a data-serie="%s" href="#serie-%s">%s</a>' % (k, k, n))
    r.append('    <hr>\\n    <b>Coleções</b>')
    for k, n in [("se-liga", "Se Liga de Matemática"), ("se-liga-ef", "Se Liga de Educação Financeira"), ("sei", "Semanas de Estudos"), ("saeb", "Simulados SAEB"), ("volumes", "Volumes"), ("album", "Álbuns")]:
        r.append('    <a data-tipo="%s" href="#col-%s">%s</a>' % (k, k, n))
    r.append('    <hr>\\n    <a class="sec-link" style="font-size:12.5px;color:var(--mut);opacity:1" href="concursos.html">Apostilas para concursos →</a>')
    return "\\n".join(r)


'''
s = s[:i0] + NOVO_IDX + s[i1:]
rep(".foot-sec{margin:0 0 8px}", ".indice{max-height:calc(100vh - 36px);overflow:auto}.indice a.sub{font-weight:500;font-size:12.5px;padding:4px 9px 4px 16px;color:var(--mut)}.ic16{vertical-align:-3px}.ck{vertical-align:-2px}\n.foot-sec{margin:0 0 8px}")
io.open(p, 'w', encoding='utf-8').write(s)

g = io.open('gerar_produtos.py', encoding='utf-8').read()
g = g.replace('ao carrinho">+ 🛒</button>', 'ao carrinho">+ ' + CART + '</button>')
g = g.replace('🔍 ampliar', SV('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', 14) + ' ampliar')
g = g.replace('🔒 {pagamento}', SV('<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>', 14) + ' {pagamento}')
g = g.replace('✕', SV('<path d="M6 6l12 12M18 6 6 18"/>', 14)).replace('✓', CHECK)
io.open('gerar_produtos.py', 'w', encoding='utf-8').write(g)
print('ok')
