# Gera loja/index.html a partir do catálogo abaixo (preços/links = produtos já publicados no Eduzz).
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
pag = json.load(open(os.path.join(HERE, "img", "_paginas.json"), encoding="utf-8"))
CHK = "https://chk.eduzz.com/"
WA = "https://wa.me/5545999699444?text="

# slug, título curto, grupo, eduzz código checkout (None = em breve), preço, subtítulo, imagens(4 ou 2)
P = [
 ("matematica", "Matemática", "pss", "xsjteswd", 15, "Conteúdo específico do cargo de Professor de Matemática."),
 ("conhecimentos-basicos", "Conhecimentos Básicos", "pss", "yoeghnxb", 10, "Para todos os cargos do PSS: base comum cobrada na prova."),
 ("pedagogo", "Pedagogo", "pss", "w6tud6n2", 15, "Conteúdo específico do cargo de Pedagogo."),
 ("educacao-especial", "Educação Especial / Inclusiva", "pss", "466hxqqa", 15, "Educação inclusiva e atendimento educacional especializado."),
 ("lingua-inglesa", "Língua Inglesa", "pss", "rfeeo7ig", 15, "Versão normal e versão JUMBO (letra grande)."),
 ("geografia", "Geografia", "pss", "ktkzb34d", 15, "Conteúdo específico do cargo de Professor de Geografia."),
 ("historia", "História", "pss", "xi3bwjtm", 15, "Conteúdo específico do cargo de Professor de História."),
 ("artes", "Artes", "pss", "tgbaqcig", 15, "Conteúdo específico do cargo de Professor de Artes."),
 ("gestao-negocios", "Administração, Gestão e Negócios", "pss", "lbgwlvz3", 15, "Conteúdo do eixo Gestão e Negócios."),
 ("lingua-portuguesa", "Língua Portuguesa", "pss", "ndhizctf", 15, "Conteúdo específico do cargo de Professor de Língua Portuguesa."),
 ("educacao-fisica", "Educação Física", "pss", "zsa3iutj", 15, "Conteúdo específico do cargo de Professor de Educação Física."),
 ("quimica", "Química", "pss", "jg3vxafi", 15, "Conteúdo específico do cargo de Professor de Química."),
 ("informacao-comunicacao", "Informação e Comunicação", "pss", None, 20, "Eixo Informação e Comunicação."),
 ("simulado-matematica", "Simulado de Matemática", "pss", "linutiqk", 10, "Questões para treinar com o estilo da prova."),
 ("pedagogo-abaetetuba", "Pedagogo · Abaetetuba-PA", "outros", "x3khho43", 20, "Apostila completa para a Prefeitura de Abaetetuba-PA 2026."),
 ("cisop-artesao", "Artesão", "cisop", "d2w5agmt", 15, "CISOP Cascavel 2026 · concurso do Consórcio Intermunicipal de Saúde do Oeste do Paraná · banca Fafipa · prova 18/10/2026."),
 ("cisop-agente-administrativo", "Agente Administrativo", "cisop", "4loe6tq7", 15, "CISOP Cascavel 2026 · concurso do Consórcio Intermunicipal de Saúde do Oeste do Paraná · banca Fafipa · prova 18/10/2026."),
 ("cisop-tecnico-enfermagem", "Técnico em Enfermagem", "cisop", "afuewgiv", 15, "CISOP Cascavel 2026 · concurso do Consórcio Intermunicipal de Saúde do Oeste do Paraná · banca Fafipa · prova 18/10/2026."),
 ("cisop-monitor-biblioteca", "Monitor de Biblioteca", "prefeitura", "njnvex3v", 20, "Prefeitura de Cascavel 2026 · teste seletivo · banca Fafipa · prova 29/11/2026."),
 ("cisop-professor-ed-infantil", "Professor de Educação Infantil", "prefeitura", "enxexhh2", 20, "Prefeitura de Cascavel 2026 · teste seletivo · banca Fafipa · prova 29/11/2026."),
 ("cisop-professor-temporario", "Professor Temporário", "prefeitura", "55drvhe3", 20, "Prefeitura de Cascavel 2026 · teste seletivo · banca Fafipa · prova 29/11/2026."),
 ("volume-cone", "Matemática · Volume do Cone · 9º ano", "reforco", "39YN13DQWO", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-cubo", "Matemática · Volume do Cubo · 9º ano", "reforco", "E9OG7NO5WB", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-paralelepipedo", "Matemática · Volume do Paralelepípedo · 9º ano", "reforco", "R9JXP1J80X", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-prisma", "Matemática · Volume do Prisma · 9º ano", "reforco", "KW8Z5RKD01", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-esfera", "Matemática · Volume da Esfera · 9º ano", "reforco", "7WXGXJQY0A", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-piramide", "Matemática · Volume da Pirâmide · 9º ano", "reforco", "KW8Z557B01", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-cilindro", "Matemática · Volume do Cilindro (com π) · 9º ano", "reforco", "G92KQR5KWE", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("volume-cubo-bloco-prisma", "Matemática · Volume — Cubo, Bloco e Prisma · 9º ano", "reforco", "G96RY725W1", 5, "Atividade de volume com figuras, fórmulas e gabarito. A4 pronto para imprimir."),
 ("se-liga-6", "Se Liga 2026 · Matemática — 6º ano + Extraordinário", "reforco", "797Z4NGV0E", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("se-liga-7", "Se Liga 2026 · Matemática — 7º ano + Extraordinário", "reforco", "8WPNKR3Y0P", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("se-liga-8", "Se Liga 2026 · Matemática — 8º ano + Extraordinário", "reforco", "89AX8YDG0D", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("se-liga-9", "Se Liga 2026 · Matemática — 9º ano + Extraordinário", "reforco", "60E2KY73W3", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("se-liga-1em", "Se Liga 2026 · Matemática — 1ª série EM + Extraordinário", "reforco", "Z0B1XY879A", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("se-liga-2em", "Se Liga 2026 · Matemática — 2ª série EM + Extraordinário", "reforco", "E9OG7N4KWB", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("se-liga-3em", "Se Liga 2026 · Matemática — 3ª série EM + Extraordinário", "reforco", "KW8Z5RAO01", 10, "Revisão para as avaliações finais + versão extraordinária, com gabarito."),
 ("saeb-9", "Simulado SAEB de Matemática — 9º ano", "reforco", "69K16VV8WO", 10, "50 questões de Matemática com gabarito e resoluções."),
 ("saeb-3em", "Simulado SAEB de Matemática — 3ª série EM", "reforco", "8WPNKOEN0P", 10, "50 questões de Matemática com gabarito e resoluções."),
 ("sei-6", "Semanas de Estudos · Matemática — 6º ano", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (6º ano) · revisão semanal com gabarito e resoluções."),
 ("sei-7", "Semanas de Estudos · Matemática — 7º ano", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (7º ano) · revisão semanal com gabarito e resoluções."),
 ("sei-8", "Semanas de Estudos · Matemática — 8º ano", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (8º ano) · revisão semanal com gabarito e resoluções."),
 ("sei-9", "Semanas de Estudos · Matemática — 9º ano", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (9º ano) · revisão semanal com gabarito e resoluções."),
 ("sei-1em", "Semanas de Estudos · Matemática — 1ª série EM", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (1ª série EM) · revisão semanal com gabarito e resoluções."),
 ("sei-2em", "Semanas de Estudos · Matemática — 2ª série EM", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (2ª série EM) · revisão semanal com gabarito e resoluções."),
 ("sei-3em", "Semanas de Estudos · Matemática — 3ª série EM", "reforco", "", 10, "Semanas de Estudos Intensivos de Matemática (3ª série EM) · revisão semanal com gabarito e resoluções."),
]
# ---- descrições melhoradas (sobrescrevem o subtítulo acima) ----
_VOL = {"cone": "Volume do cone: V = ⅓·π·r²·h. 12 questões com figuras, do cálculo direto a problemas do dia a dia.",
 "cubo": "Volume do cubo: V = a³. 12 questões com figuras, do cálculo direto a problemas do dia a dia.",
 "paralelepipedo": "Volume do paralelepípedo: V = a·b·c. 12 questões com figuras, caixas, piscinas e reservatórios.",
 "prisma": "Volume do prisma: V = área da base × altura. 12 questões com figuras de prismas de bases variadas.",
 "esfera": "Volume da esfera: V = 4⁄3·π·r³. 12 questões com figuras, bolas, cúpulas e reservatórios.",
 "piramide": "Volume da pirâmide: V = ⅓·área da base × altura. 12 questões com figuras e comparações com o prisma.",
 "cilindro": "Volume do cilindro: V = π·r²·h. 12 questões com figuras, latas, tubos e caixas-d'água.",
 "cubo-bloco-prisma": "Cubo, bloco retangular e prisma em uma só atividade: 12 questões com figuras para comparar as fórmulas."}
_VOLFIM = " Gabarito resolvido incluso. PDF em A4, pronto para imprimir."
_SERIE = lambda n: n.split("— ")[-1].replace(" + Extraordinário", "")
def _desc(slug, nome, sub):
    if slug.startswith("volume-"): return _VOL.get(slug[7:], sub) + _VOLFIM
    if slug.startswith("se-liga-"):
        return ("Revisão completa para as avaliações finais de Matemática do %s. "
                "Inclui a versão extraordinária (recuperação) e gabarito. A4 pronto para imprimir.") % _SERIE(nome)
    if slug.startswith("saeb-"):
        return ("Simulado no estilo SAEB para o %s: 50 questões de Matemática por descritor, folha de respostas (ZipGrade), "
                "gabarito e resoluções. PDF em A4 para imprimir.") % _SERIE(nome)
    if slug.startswith("sei-"):
        return ("Semanas de Estudos Intensivos para o %s: um plano de revisão semana a semana, com atividades, gabarito e resoluções. "
                "Ideal para recomposição de aprendizagem.") % _SERIE(nome)
    if slug.startswith("cisop-") and "Prefeitura" in sub:
        return sub.rstrip(".") + ". Apostila focada no edital: conteúdo organizado por disciplina, com resumos objetivos e questões para treinar."
    if slug.startswith("cisop-"):
        return sub.rstrip(".") + ". Apostila focada no edital: conteúdo organizado por disciplina, com resumos objetivos e questões para treinar."
    return sub
P = [(a, b, c, d, e, _desc(a, b, f)) for a, b, c, d, e, f in P]
GRUPOS = {"pss": "PSS SEED-PR 2027", "cisop": "CISOP Cascavel 2026", "prefeitura": "Prefeitura de Cascavel 2026", "simulado": "Simulados", "reforco": "Reforço e recomposição", "outros": "Outros concursos"}
items = []
def tipo_de(slug):
    if slug.startswith('volume-'): return 'volumes'
    if slug.startswith('sei-'): return 'sei'
    if slug.startswith('se-liga-'): return 'se-liga'
    if slug.startswith('saeb-'): return 'saeb'
    return 'apostilas'

for slug, nome, g, code, preco, sub in P:
    imgs = [f"img/{slug}-{k}.jpg" for k in range(1, 9) if os.path.exists(os.path.join(HERE, "img", f"{slug}-{k}.jpg"))]
    if tipo_de(slug) in ('se-liga', 'sei', 'saeb') or slug == 'volume-cubo-bloco-prisma':   # capas restauradas do catalogo WhatsApp (06/11/2026)
        imgs = [(i + '?v=5') if i.endswith('-1.jpg') else i for i in imgs]
    items.append({"slug": slug, "nome": nome, "grupo": g, "grupoNome": GRUPOS[g], "link": (CHK + code) if code else None,
                  "preco": preco, "sub": sub, "imgs": imgs, "tipo": tipo_de(slug),
                  "de": 15 if slug in ('saeb-9', 'saeb-3em') else None,
                  "paginas": pag.get(slug, {}).get("paginas")})

HTML = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Loja de Matemática — Atividades Educativas, Simulados e Apostilas</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext x='50' y='80' font-size='84' text-anchor='middle'%3E🏛️%3C/text%3E%3C/svg%3E">
<meta name="theme-color" content="#1B3A6B">
<meta name="description" content="Atividades educativas prontas para imprimir (Se Liga, volumes, simulados SAEB) com gabarito, e apostilas para concursos como PSS SEED-PR 2027. Veja as páginas antes de comprar.">
<meta property="og:title" content="Loja de Matemática — Atividades Educativas, Simulados e Apostilas">
<meta property="og:description" content="Atividades educativas prontas para imprimir, simulados SAEB e apostilas para concursos (PSS SEED-PR 2027 e mais).">
<meta property="og:image" content="https://hodhreego.github.io/Loja/og.jpg?v=5">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--navy:#1B3A6B;--navy-deep:#0F2547;--gold:#C9A227;--gold-light:#E9D48E;--bg:#EEF3FB;--ink:#1B2733;--mut:#5b6b80;--card:#fff;--ok:#1f7a4d;--line:#d9e2f1}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Source Sans 3',system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.45}
.wrap{max-width:1180px;margin:0 auto;padding:0 18px}
header.hero{background:linear-gradient(135deg,var(--navy-deep),var(--navy) 60%,#27508f);color:#fff;padding:84px 0 64px;position:relative;overflow:hidden}
header.hero:after{content:"";position:absolute;right:-90px;top:-90px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(201,162,39,.35),transparent 70%)}
.eyebrow{letter-spacing:.22em;font-size:12px;color:var(--gold-light);font-weight:600;text-transform:uppercase}
h1{font-family:'Playfair Display',serif;font-size:clamp(30px,5vw,50px);line-height:1.1;margin:10px 0 12px}
h1 em{color:var(--gold-light);font-style:normal}
.hero p{max-width:620px;color:#d6e1f5;font-size:18px}
.perks{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.perk{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);padding:7px 14px;border-radius:99px;font-size:14px;font-weight:600}
.hero-wa{white-space:nowrap;position:absolute;top:16px;right:16px;z-index:5;background:#1f9d57;color:#fff;border:0;border-radius:99px;padding:10px 18px;font:700 15px 'Source Sans 3';cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.35);display:inline-flex;align-items:center;gap:8px}
.hero-wa small{display:none}.hero-wa:hover{background:#188047}
.tools{margin-top:-30px;position:relative;z-index:2}
.bar{background:#fff;border-radius:16px;box-shadow:0 10px 30px rgba(15,37,71,.15);padding:14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:8px;flex:1}
.chip{border:1.5px solid var(--line);background:#fff;color:var(--navy);font:600 14px 'Source Sans 3';padding:8px 14px;border-radius:99px;cursor:pointer;transition:.15s}
.chip:hover{border-color:var(--navy)}
.chip.on{background:var(--navy);border-color:var(--navy);color:#fff}
.chip small{opacity:.7;font-weight:600;margin-left:4px}
#q{border:1.5px solid var(--line);border-radius:99px;padding:9px 16px;font:500 15px 'Source Sans 3';min-width:220px;outline:none}
#q:focus{border-color:var(--navy)}
section.grupo{margin-top:34px}
section.grupo h2{font-family:'Playfair Display',serif;color:var(--navy);font-size:26px;display:flex;align-items:center;gap:12px}
section.grupo h2:after{content:"";flex:1;height:2px;background:linear-gradient(90deg,var(--gold),transparent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:20px;margin-top:16px}
.card{background:var(--card);border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(15,37,71,.09);display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-4px);box-shadow:0 14px 30px rgba(15,37,71,.18)}
.cover{position:relative;aspect-ratio:3/4;background:#dfe7f5;cursor:pointer;overflow:hidden}
.badge{position:absolute;top:10px;left:10px;font-size:12px;font-weight:700;padding:4px 10px;border-radius:99px;background:var(--ok);color:#fff}
.badge.soon{background:var(--gold);color:#3b2f00}
.peek{position:absolute;bottom:10px;right:10px;background:rgba(15,37,71,.85);color:#fff;font-size:12px;font-weight:600;padding:5px 11px;border-radius:99px}
.info{padding:14px 15px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.info small{color:var(--mut);font-weight:600;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.info h3{font-size:18px;line-height:1.2;color:var(--navy-deep)}
.info p{font-size:14px;color:var(--mut);flex:1}
.row{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:8px}
.price{font-family:'Playfair Display',serif;font-weight:700;font-size:24px;color:var(--navy)}
.price span{font-size:14px;margin-right:2px}
.btn{display:inline-block;text-decoration:none;font:700 14px 'Source Sans 3';padding:10px 16px;border-radius:10px;border:0;cursor:pointer;transition:.15s}
.btn.buy{background:var(--navy-deep);color:#fff;box-shadow:0 0 0 2px var(--gold) inset}.btn.buy:hover{background:#000;color:#fff}
.btn.wa{background:#1f9d57;color:#fff}.btn.wa:hover{background:#188047}
.btn.ghost{background:#fff;color:var(--navy);border:1.5px solid var(--line)}
.empty{display:none;text-align:center;padding:50px 0;color:var(--mut)}
footer{margin-top:60px;background:var(--navy-deep);color:#c5d3ee;padding:34px 0;font-size:14px}
footer b{color:#fff}.warn{margin-top:12px;background:#a1262a;color:#fff;border-radius:10px;padding:10px 14px;font-weight:600}
/* modal */
.modal{position:fixed;inset:0;background:rgba(10,20,40,.82);display:none;align-items:center;justify-content:center;z-index:50;padding:14px}
.modal.open{display:flex}
.box{background:#fff;border-radius:18px;max-width:880px;width:100%;max-height:94vh;overflow:auto;display:grid;grid-template-columns:1.1fr 1fr}
.stage{background:#e6ecf7;padding:14px;display:flex;flex-direction:column;gap:10px;align-items:center}
.stage img.big{width:100%;max-height:68vh;object-fit:contain;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.2);background:#fff}
.thumbs{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.thumbs img{width:56px;height:76px;object-fit:cover;object-position:top;border-radius:5px;border:2px solid transparent;cursor:pointer;opacity:.7}
.thumbs img.on{border-color:var(--gold);opacity:1}
.side{padding:24px;display:flex;flex-direction:column;gap:10px}
.side h3{font-family:'Playfair Display',serif;font-size:26px;color:var(--navy-deep);line-height:1.15}
.side .row{margin-top:auto}
.x{position:absolute;top:12px;right:14px;width:44px;height:36px;display:flex;align-items:center;justify-content:center;color:#000;font:400 30px/1 Arial,sans-serif;cursor:pointer;background:#fff;border:1px solid #000;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.4);z-index:5}.x:hover{background:#e81123;color:#fff;border-color:#e81123}
.lab{font-size:12px;color:var(--mut);text-align:center}

/* whatsapp */
.fab{white-space:nowrap;position:fixed;right:16px;bottom:16px;z-index:40;background:#1f9d57;color:#fff;border:0;border-radius:99px;padding:13px 20px;font:700 15px 'Source Sans 3';box-shadow:0 8px 22px rgba(0,0,0,.28);cursor:pointer;display:flex;gap:8px;align-items:center}
.fab:hover{background:#188047}
/* carrinho */
.cartfab{position:fixed;right:16px;bottom:74px;z-index:41;background:var(--navy);color:#fff;border:0;border-radius:99px;padding:12px 18px;font:700 15px 'Source Sans 3';box-shadow:0 8px 22px rgba(0,0,0,.28);cursor:pointer;display:none;gap:8px;align-items:center}
.cartfab.on{display:flex}
.cartfab b{background:#fff;color:var(--navy);border-radius:99px;min-width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:13px}
.cpanel{position:fixed;right:16px;bottom:132px;z-index:46;width:min(380px,calc(100vw - 32px));max-height:64vh;background:#fff;border-radius:18px;box-shadow:0 18px 44px rgba(10,20,40,.35);display:none;flex-direction:column;overflow:hidden}
.cpanel.open{display:flex}
.cpanel header{background:var(--navy);color:#fff;padding:13px 16px;display:flex;justify-content:space-between;align-items:center}
.cpanel header b{font-size:16px}.cpanel header button{background:none;border:0;color:#fff;font-size:24px;cursor:pointer;line-height:1}
.cbody{padding:12px 14px;overflow:auto;display:flex;flex-direction:column;gap:8px}
.citem{display:flex;gap:10px;align-items:center;border-bottom:1px solid #eef2f9;padding-bottom:8px}
.citem img{width:38px;height:50px;object-fit:cover;object-position:top;border-radius:4px;background:#eef2f9}
.citem .cn{flex:1;min-width:0;font-size:13px;font-weight:600;line-height:1.25}
.citem .cn small{display:block;color:var(--mut);font-weight:500}
.cq{display:flex;align-items:center;gap:5px}
.cq button{width:24px;height:24px;border-radius:6px;border:1px solid var(--line);background:#fff;cursor:pointer;font-weight:700;color:var(--navy);line-height:1}
.cfoot{padding:12px 14px;border-top:1px solid #eef2f9;display:flex;flex-direction:column;gap:8px;background:#fafcff}
.cfoot .tot{display:flex;justify-content:space-between;font-weight:700;color:var(--navy-deep)}
.btn.add{background:#eef3fd;color:var(--navy);border:1px solid #d5e0f5;font-weight:700;padding:8px 10px}
.btn.add:hover{background:#dfe9fb}
.toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,20px);background:var(--navy-deep);color:#fff;padding:10px 18px;border-radius:99px;font-weight:600;font-size:14px;opacity:0;pointer-events:none;transition:.25s;z-index:60}
.toast.on{opacity:1;transform:translate(-50%,0)}
.wpanel{position:fixed;right:16px;bottom:74px;z-index:45;width:min(360px,calc(100vw - 32px));background:#fff;border-radius:18px;box-shadow:0 18px 44px rgba(10,20,40,.35);display:none;overflow:hidden}
.wpanel.open{display:block}
.wpanel header{background:#1f9d57;color:#fff;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.wpanel header b{font-size:16px}.wpanel header button{background:none;border:0;color:#fff;font-size:26px;cursor:pointer;line-height:1}
.wbody{padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px;max-height:72vh;overflow:auto}
.wbody label.t{font-size:12px;font-weight:700;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.opt{display:flex;gap:8px;align-items:flex-start;border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;font-size:14px;cursor:pointer}
.opt:has(input:checked){border-color:#1f9d57;background:#eaf7f0}
.opt input{margin-top:3px;accent-color:#1f9d57}
.wbody select,.wbody textarea{width:100%;border:1.5px solid var(--line);border-radius:10px;padding:9px 10px;font:500 14px 'Source Sans 3';outline:none}
.wbody textarea{min-height:92px;resize:vertical}
.wbody .btn.wa{text-align:center;padding:12px}
.wfoot{position:sticky;bottom:-16px;background:#fff;margin:0 -16px -16px;padding:10px 16px 14px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:6px;box-shadow:0 -8px 14px -10px rgba(0,0,0,.25)}
.tip{background:#fff8e1;border:1.5px solid #ecd58a;border-radius:10px;padding:10px 12px;font-size:13.5px;line-height:1.5;color:#4a3d00}.wbody small{color:var(--mut);font-size:12px}

/* certames */
.certs{display:flex;flex-wrap:wrap;gap:10px;padding:2px 2px 6px;flex:1 1 100%}
.conteudo{display:grid;grid-template-columns:190px 1fr;gap:24px;align-items:start;margin-top:10px}
.indice{position:sticky;top:18px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px;box-shadow:0 6px 18px rgba(15,37,71,.06)}
.indice b{display:block;font:700 12px 'Source Sans 3';text-transform:uppercase;letter-spacing:.08em;color:var(--mut);margin:2px 0 8px}
.indice a{display:block;padding:7px 9px;border-radius:8px;color:var(--navy);font:600 13.5px 'Source Sans 3';cursor:pointer}
.indice a:hover{background:#eef3fb}
.indice hr{border:0;border-top:1px solid var(--line);margin:8px 0}
@media(max-width:900px){.conteudo{grid-template-columns:1fr}.indice{position:static;display:flex;flex-wrap:wrap;gap:4px;align-items:center}.indice b{width:100%;margin:0}.indice a{padding:5px 8px}.indice hr{display:none}}
.cert{flex:0 0 auto;min-width:150px;max-width:210px;scroll-snap-align:start;text-align:left;background:#fff;border:1px solid #e3eaf6;border-radius:14px;padding:9px 13px;cursor:pointer;font:600 14px 'Source Sans 3';color:var(--navy);transition:.15s}
.cert b{display:block;font-size:15px;line-height:1.2}.cert small{display:block;color:var(--mut);font-weight:600;margin-top:3px;font-size:12px}
.cert{display:flex;align-items:center;gap:10px}
.cert .ct{display:block;min-width:0}
.cert .ic{flex:0 0 36px;width:36px;height:36px;border-radius:11px;background:var(--azul-claro,#e8f1ff);display:flex;align-items:center;justify-content:center;color:var(--navy)}
.cert .ic svg{width:22px;height:22px;display:block}
.cert.on .ic{background:rgba(255,255,255,.16);color:#fff}
.cert:hover{border-color:var(--navy)}.cert.on{background:var(--navy);border-color:var(--navy);color:#fff}.cert.on small{color:var(--gold-light)}
.info-cert{margin-top:22px;background:linear-gradient(135deg,#fff,#f4f8ff);border:2px solid var(--line);border-left:6px solid var(--gold);border-radius:16px;padding:20px 22px;display:none;animation:subir .4s ease}
.info-cert.show{display:block}
@keyframes subir{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.info-cert h2{font-family:'Playfair Display',serif;color:var(--navy-deep);font-size:26px;margin-bottom:4px}
.st{display:inline-block;font-size:12.5px;font-weight:700;padding:4px 11px;border-radius:99px;margin:4px 0 10px}
.st.open{background:#dff5e8;color:#14683d}.st.closed{background:#fde8d4;color:#8a4300}.st.soon{background:#e5ecfa;color:var(--navy)}.st.done{background:#eceff3;color:#4b5563}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:8px 0 14px}
.fact{background:#fff;border:1px solid var(--line);border-radius:10px;padding:9px 12px}.fact small{display:block;color:var(--mut);font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}.fact span{font-weight:700;color:var(--navy-deep)}
.links{display:flex;flex-wrap:wrap;gap:8px}.links a{text-decoration:none;font:700 14px 'Source Sans 3';padding:9px 14px;border-radius:10px;background:var(--navy);color:#fff}.links a.alt{background:#fff;color:var(--navy);border:1.5px solid var(--navy)}
.dt{color:#c62828;font-weight:800;font-size:1.16em;white-space:nowrap}
.fact.hot span{font-size:1.3em}
.fact.hot{border-color:#f0b4b4;background:#fff5f5}
.note{font-size:13px;color:var(--mut);margin-top:10px}
/* miniaturas: virada de página como papel de verdade (frente, verso, sombra e dobra) */
.cover{perspective:1300px}
.book{position:absolute;inset:0;z-index:0;transform-style:preserve-3d}
.pg{position:absolute;inset:0;transform-origin:left center;transform-style:preserve-3d;background:#fff}
.pg>.f,.pg>.b{position:absolute;inset:0;width:100%;height:100%;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.pg>.f{object-fit:cover;object-position:top}
.pg>.b{transform:rotateY(180deg);background:linear-gradient(90deg,#d9d2c2,#f6f1e6 18%,#fbf8f0)}
.pg .sh{position:absolute;inset:0;pointer-events:none;opacity:0;background:linear-gradient(90deg,rgba(0,0,0,.55),rgba(0,0,0,.05) 70%)}
.pg>.f::after{content:none}
.pg.flip{animation:turn 1.5s cubic-bezier(.45,.05,.3,1) forwards}
.pg.flip .f+.sh{animation:shf 1.5s ease-in forwards}
@keyframes turn{
 0%{transform:rotateY(0) skewY(0);box-shadow:0 0 0 rgba(0,0,0,0)}
 25%{transform:rotateY(-40deg) skewY(-1.2deg);box-shadow:14px 0 26px rgba(0,0,0,.28)}
 50%{transform:rotateY(-92deg) skewY(-2.5deg);box-shadow:26px 0 38px rgba(0,0,0,.36)}
 75%{transform:rotateY(-142deg) skewY(-1.2deg);box-shadow:18px 0 28px rgba(0,0,0,.26)}
 100%{transform:rotateY(-180deg) skewY(0);box-shadow:0 0 0 rgba(0,0,0,0)}}
@keyframes shf{0%{opacity:0}60%{opacity:.8}100%{opacity:.9}}
.book.nt .pg{animation:none!important}
.book:after{content:"";position:absolute;left:0;top:0;bottom:0;width:7px;background:linear-gradient(90deg,rgba(0,0,0,.35),transparent);z-index:99;pointer-events:none}
.dots{position:absolute;left:0;right:0;bottom:10px;display:flex;gap:5px;justify-content:center;pointer-events:none;z-index:2}
.dots i{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.55);transition:.3s}.dots i.on{background:var(--gold);width:16px;border-radius:4px}
.cover:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,transparent 70%,rgba(15,37,71,.35));pointer-events:none}
.badge,.peek{z-index:2}
@media(prefers-reduced-motion:reduce){.pg.flip{animation:none;transform:rotateY(-180deg)}}
@media(max-width:720px){.certs{display:flex;flex-wrap:nowrap;overflow-x:auto;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch;gap:8px}.cert{flex:none}.cert{min-width:0;max-width:none;min-height:42px;padding:8px 14px;border-radius:99px}.cert .ic,.cert small{display:none}.cert b{font-size:14px;white-space:nowrap}.box{grid-template-columns:1fr}.stage img.big{max-height:52vh}.grid{grid-template-columns:repeat(2,1fr);gap:12px}.info h3{font-size:15px}.price{font-size:20px}.row{flex-direction:column;align-items:stretch;gap:6px}.row .btn{text-align:center}.info{padding:12px}#q{width:100%}.fab{padding:11px 16px}}

/* ---- redesign: topo compacto, catálogo logo na primeira tela, visual mais sóbrio ---- */
header.hero{padding:44px 0 56px}
header.hero:after{display:none}
.eyebrow{font-size:11px;letter-spacing:.2em}
h1{font-size:clamp(26px,4vw,40px);margin:8px 0 10px}
.hero p{font-size:16px;max-width:560px;margin:0}
.perks{gap:8px;margin-top:16px}
.perk{background:transparent;border:0;padding:0 14px 0 0;font-size:13px;font-weight:600;color:#cfe0fb}
.tools{margin-top:-28px}
.bar{border-radius:12px;box-shadow:0 6px 22px rgba(15,37,71,.12);padding:12px 14px}
.card{border-radius:12px;box-shadow:0 2px 10px rgba(15,37,71,.08)}
.card:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(15,37,71,.15)}
section.grupo{margin-top:26px}
section.grupo h2{font-size:22px}
@media(max-width:720px){
 header.hero{padding:20px 0 40px}
 .eyebrow{font-size:10px;margin-right:110px}
 h1{font-size:25px;margin:6px 0 8px}
 .hero p{font-size:14px;max-width:none}
 .perks{display:none}
 .hero-wa{top:12px;right:12px;padding:8px 14px;font-size:14px}
 .tools{margin-top:-22px}
 .bar{padding:10px}
 #tipos{margin-top:8px!important}
 #q{min-width:0;margin-top:2px}
 .indice{display:none}
 section.grupo{margin-top:20px}
 section.grupo h2{font-size:19px}
}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="eyebrow">Prof. Rodrigo Gonçalves Pereira</div>
  <h1>Loja de <em>Matemática</em><br>Atividades Educativas, Simulados &amp; Apostilas</h1>
  <p>Atividades educativas prontas para imprimir, com gabarito, para professores e alunos do 6º ano ao Ensino Médio. E, para quem estuda para concurso, apostilas atualizadas com os editais. Confira as páginas antes de comprar.</p>
  <div class="perks"><span class="perk">✓ Entrega digital em PDF</span><span class="perk">✓ Veja as páginas antes de comprar</span><span class="perk">✓ Versão JUMBO (letra grande)</span><span class="perk">✓ Pagamento seguro pela Eduzz</span></div>
  <button class="hero-wa" onclick="wtoggle(true)"><svg class="wai" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg> Falar no WhatsApp <small>tire dúvidas · peça seu material</small></button>
</div></header>

<div class="wrap tools"><div class="bar">
  <div class="certs" id="chips"></div>
  <div class="certs" id="tipos" style="margin-top:10px"></div>
  <input id="q" type="search" placeholder="Buscar apostila…">
</div></div>

<div class="wrap"><div class="info-cert" id="infoc"></div></div>
<div class="conteudo wrap">
  <aside class="indice">
    <b>Índice</b>
    <a onclick="setTipo('todos')">Todas as atividades</a>
    <a onclick="setTipo('volumes')">Volumes</a>
    <a onclick="setTipo('se-liga')">Se Liga</a>
    <a onclick="setTipo('saeb')">Simulados SAEB</a>
    <a onclick="setTipo('apostilas')">Apostilas</a>
    <hr>
    <b>Certames</b>
    <a onclick="setGrupo('pss')">PSS SEED-PR</a>
    <a onclick="setGrupo('cisop')">CISOP Cascavel</a>
    <a onclick="setGrupo('prefeitura')">Prefeitura de Cascavel</a>
    <a onclick="setGrupo('reforco')">Reforço e recomposição</a>
    <a onclick="setGrupo('outros')">Outros concursos</a>
  </aside>
  <main id="main"></main>
</div>
<div class="wrap empty" id="empty">Nenhum material encontrado.</div>

<footer><div class="wrap">
  <p><b>Loja de Matemática</b> — Prof. Rodrigo Gonçalves Pereira. Dúvidas ou pedidos de novos materiais: <a style="color:var(--gold-light)" href="#" onclick="wtoggle(true);return false">WhatsApp (+55 45 99969-9444)</a>.</p>
  <p class="warn">Proibido o compartilhamento. Cópia não autorizada. Violação sujeita à pena de detenção e multa (Lei 9.610/98 e Art. 184 do Código Penal).</p>
</div></footer>


<button class="fab" id="fab" onclick="wtoggle()"><svg class="wai" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg> Falar no WhatsApp</button>
<div class="wpanel" id="wp" role="dialog" aria-label="Falar no WhatsApp"><header><b>Fale com o Prof. Rodrigo</b><button onclick="wtoggle()" aria-label="Fechar">×</button></header>
 <div class="wbody">
  <label class="t">Sobre o que você quer falar?</label>
  <div id="wopts"></div>
  <div id="wtip" class="tip"></div>
  <label class="t" for="wprod">Material (opcional)</label>
  <select id="wprod"></select>
  <label class="t" for="wmsg">Sua mensagem (você pode editar)</label>
  <textarea id="wmsg"></textarea>
  <div class="wfoot"><a class="btn wa" id="wgo" target="_blank" rel="noopener" href="#">Abrir WhatsApp</a>
  <small>Você será levado ao WhatsApp com a mensagem pronta (o link da loja vai junto no final); só precisa tocar em enviar.</small></div>
 </div></div>
<button class="cartfab" id="cartfab" onclick="ctoggle()"><span>🛒 Carrinho</span><b id="cartn">0</b></button>
<div class="cpanel" id="cp" role="dialog" aria-label="Carrinho">
 <header><b>Seu carrinho</b><button onclick="ctoggle()" aria-label="Fechar">×</button></header>
 <div class="cbody" id="cbody"></div>
 <div class="cfoot">
  <div class="tot"><span>Total</span><span id="ctot">R$ 0,00</span></div>
  <button class="btn buy" onclick="cfinal()">Enviar pedido no WhatsApp</button>
  <small style="color:var(--mut);font-size:12px">O pedido vira um código (ex.: PED-261106-A7K2). O Prof. Rodrigo recebe a lista organizada e devolve o link de pagamento.</small>
 </div>
</div>
<div class="toast" id="toast"></div>
<div class="modal" id="modal" onclick="if(event.target===this)fecha()"><button class="x" onclick="fecha()" aria-label="Fechar">×</button>
  <div class="box"><div class="stage"><img class="big" id="big" alt=""><div class="thumbs" id="th"></div><div class="lab" id="lab"></div></div>
  <div class="side" id="side"></div></div></div>

<script>
const ITENS=__DATA__;
const WA="__WA__";
const GR=[["reforco","Reforço e recomposição"],["pss","PSS SEED-PR 2027"],["cisop","CISOP Cascavel 2026"],["prefeitura","Prefeitura de Cascavel 2026"],["outros","Outros concursos"]];
const TIPOS=[["todos","Todas as atividades"],["se-liga","Se Liga"],["sei","Semanas de Estudos"],["saeb","Simulados SAEB"],["volumes","Volumes"],["apostilas","Apostilas"]];
let filtro="todos",busca="",filtroTipo="todos";{const h=location.hash.slice(1);if(["pss","cisop","prefeitura","simulado","outros"].includes(h))filtro=h}
const $=s=>document.querySelector(s);
const brl=n=>n.toFixed(2).replace(".",",");
function card(it){
  const soon=!it.link;
  const act=soon?`<button class="btn wa" onclick="wabre('${it.slug}',5)">Avisar-me</button>`
                 :`<a class="btn buy" target="_blank" rel="noopener" href="${it.link}">Comprar</a>`;
  const add=`<button class="btn add" onclick="addCart('${it.slug}')" title="Adicionar ao carrinho" aria-label="Adicionar ${it.nome} ao carrinho">🛒 +</button>`;
  const n=it.imgs.length;
  const leaf=(u,k)=>`<div class="pg" style="z-index:${n-k+1}"><img class="f" ${k?'loading="lazy"':''} src="${u}" alt="${k?'Página '+(k+1)+' da':'Capa da'} apostila ${it.nome}"><i class="sh"></i><i class="b"></i></div>`;
  const strip=it.imgs.map(leaf).join("")+`<div class="pg base" style="z-index:0"><img class="f" src="${it.imgs[0]}" alt=""></div>`;
  const dots=it.imgs.length>1?`<div class="dots">${it.imgs.map((_,k)=>`<i class="${k?'':'on'}"></i>`).join("")}</div>`:"";
  return `<article class="card" data-s="${it.slug}"><div class="cover" data-n="${it.imgs.length}" onclick="abre('${it.slug}')"><div class="book">${strip}</div>${dots}<span class="badge ${soon?'soon':''}">${soon?'Em breve':'Disponível'}</span><span class="peek">👁 ver páginas</span></div>
  <div class="info" onmouseenter="const cv=this.parentElement.querySelector('.cover');if(cv&&cv._reset)cv._reset()"><small>${it.grupoNome}</small><h3>${it.nome}</h3><p>${dt(it.sub)}${it.paginas?` · ${it.paginas} págs.`:''}</p>
  <div class="row"><div class="price"><span>R$</span>${brl(it.preco)}</div>${add}${act}</div></div></article>`;
}
const CERT={
 pss:{nome:"PSS SEED-PR 2027",orgao:"Secretaria de Estado da Educação do Paraná (SEED-PR) · organização: NC/UFPR",edital:"Edital nº 52/2026 – GS/SEED",insc:["2026-07-27","2026-08-24"],prova:"2026-10-18",
  desc:"Processo Seletivo Simplificado para contratação temporária de Professor e Professor Pedagogo da rede estadual. Etapas: prova objetiva, prova de títulos e prova prática.",
  links:[["Página oficial do PSS (SEED-PR)","https://www.educacao.pr.gov.br/pss"],["Portal NC/UFPR · edital e inscrições","https://servicos.nc.ufpr.br/PortalNC/Concurso?concurso=SEED2026",1]],
  nota:"As apostilas seguem o conteúdo programático do Edital 52/2026 e incluem as normas do Paraná."},
 cisop:{nome:"CISOP Cascavel 2026",orgao:"Consórcio Intermunicipal de Saúde do Oeste do Paraná · banca: Fundação Fafipa",edital:"Edital nº 01/2026 (13/08/2026)",insc:["2026-08-18","2026-10-01"],prova:"2026-10-18",
  desc:"Concurso para emprego público do CISOP, com 31 vagas imediatas e cadastro de reserva (níveis fundamental, médio, técnico e superior).",
  links:[["Edital de abertura (PDF)","https://anexos-r2.selecao.net.br/uploads/281/concursos/4206/anexos/c60930a2-c3d3-47ae-8add-8087e9987994.pdf"],["Página do concurso e inscrição (Fafipa)","https://fafipa.selecao.net.br/informacoes/4206/",1]],
  nota:"Atenção: este é um concurso diferente do teste seletivo da Prefeitura de Cascavel."},
 prefeitura:{nome:"Prefeitura de Cascavel 2026",orgao:"Prefeitura Municipal de Cascavel/PR · banca: Fundação Fafipa",edital:"Edital nº 354/2026 (01/10/2026)",insc:["2026-10-05","2026-11-03"],prova:"2026-11-29",
  desc:"Teste seletivo para Professor de Educação Infantil (10 vagas), com cadastro de reserva para Monitor de Biblioteca Temporário e Professor Temporário.",
  links:[["Edital de abertura (PDF)","https://anexos-r2.selecao.net.br/uploads/281/concursos/4218/anexos/b1f17c78-013c-4f22-a1bb-01f3f8f7d1fb.pdf"],["Fazer inscrição online (Fafipa)","https://www.fundacaofafipa.org.br/inscricao/4218",1],["Página do certame","https://www.fundacaofafipa.org.br/informacoes/4218/"]],
  nota:"Pedido de isenção da taxa: 05 a 09/10/2026. Este é um edital diferente do CISOP Cascavel."},
 outros:{nome:"Abaetetuba-PA",orgao:"Prefeitura de Abaetetuba/PA",edital:"Concurso 2026",desc:"Apostila completa para o cargo de Pedagogo no concurso da Prefeitura de Abaetetuba.",links:[],nota:"Confira o edital e as datas no site da prefeitura/banca organizadora."},
 simulado:{nome:"Simulados",orgao:"Treino com questões",desc:"Simulados para treinar no estilo da prova e conferir seu desempenho.",links:[]}
};
const fmt=d=>d.split("-").reverse().join("/");
const dt=t=>String(t).replace(/\d{2}\/\d{2}\/\d{4}|\d{2}\/\d{2}(?= a )|\b\d{2} a \d{2}\/\d{2}\/\d{4}/g,m=>`<b class="dt">${m}</b>`);
function status(c){if(!c.insc)return "";const h=new Date().toISOString().slice(0,10);
  if(h<c.insc[0])return `<span class="st soon">Inscrições a partir de ${dt(fmt(c.insc[0]))}</span>`;
  if(h<=c.insc[1])return `<span class="st open">● Inscrições abertas até ${dt(fmt(c.insc[1]))}</span>`;
  if(h<=c.prova)return `<span class="st closed">Inscrições encerradas em ${dt(fmt(c.insc[1]))} · prova em ${dt(fmt(c.prova))}</span>`;
  return `<span class="st done">Prova realizada em ${dt(fmt(c.prova))}</span>`;}
function infoCert(){const el=$("#infoc");const c=CERT[filtro];
  if(!c){el.className="info-cert";el.innerHTML="";return}
  const f=[];if(c.orgao)f.push(["Órgão / banca",c.orgao]);if(c.edital)f.push(["Edital",c.edital]);
  if(c.insc)f.push(["Inscrições",fmt(c.insc[0])+" a "+fmt(c.insc[1]),1]);if(c.prova)f.push(["Prova objetiva",fmt(c.prova),1]);
  el.className="info-cert show";
  el.innerHTML=`<h2>${c.nome}</h2>${status(c)}<p>${dt(c.desc)}</p><div class="facts">${f.map(x=>`<div class="fact ${x[2]?'hot':''}"><small>${x[0]}</small><span>${dt(x[1])}</span></div>`).join("")}</div>
   ${c.links.length?`<div class="links">${c.links.map(l=>`<a class="${l[2]?'':'alt'}" target="_blank" rel="noopener" href="${l[1]}">${l[0]} ↗</a>`).join("")}</div>`:""}
   ${c.nota?`<p class="note">ℹ️ ${dt(c.nota)}</p>`:""}`;}
function render(){
  const q=busca.toLowerCase();let total=0;
  $("#main").innerHTML=GR.map(([g,nome])=>{
    if(filtro!=="todos"&&filtro!==g)return "";
    const RK={"se-liga":0,"saeb":1};const l=ITENS.filter(i=>(filtroTipo==="todos"||i.tipo===filtroTipo)&&i.grupo===g&&(i.nome+" "+i.grupoNome).toLowerCase().includes(q)).map((x,n)=>[x,n]).sort((a,b)=>((RK[a[0].tipo]??2)-(RK[b[0].tipo]??2))||a[1]-b[1]).map(x=>x[0]);
    total+=l.length;if(!l.length)return "";
    return `<section class="grupo"><h2>${nome}</h2><div class="grid">${l.map(card).join("")}</div></section>`;}).join("");
  $("#empty").style.display=total?"none":"block";
  infoCert();anima();
  try{history.replaceState(null,"",filtro==="todos"?location.pathname:"#"+filtro)}catch(e){}
}
function chips(){
  const c=g=>ITENS.filter(i=>g==="todos"||i.grupo===g).length;
  const svg=(p)=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
  const IC={
    todos:svg('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
    pss:svg('<path d="M22 10 12 5 2 10l10 5 10-5Z"/><path d="M6 12v5c0 1.6 3 3 6 3s6-1.4 6-3v-5"/>'),
    cisop:svg('<path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6V3Z"/>'),
    prefeitura:svg('<path d="M3 21h18"/><path d="M5 21V9l7-4 7 4v12"/><path d="M9 21v-6h6v6"/>'),
    reforco:svg('<path d="M4 19V5a2 2 0 0 1 2-2h3v16H6a2 2 0 0 0-2 2Z"/><path d="M9 3h4v16H9z"/><path d="m13 5 3-1 4 15-3 1z"/>'),
    outros:svg('<circle cx="12" cy="12" r="9"/><path d="m16 8-2.5 5.5L8 16l2.5-5.5L16 8Z"/>')
  };
  $("#chips").innerHTML=[["todos","Todos os certames"],...GR].map(([k,n])=>`<button class="cert ${filtro===k?'on':''}" onclick="filtro='${k}';chips();render();document.getElementById('infoc').scrollIntoView({behavior:'smooth',block:'nearest'})"><span class="ic">${IC[k]||IC.outros}</span><span class="ct"><b>${n}</b><small>${c(k)} ${c(k)===1?'material':'materiais'}</small></span></button>`).join("");
}
function tipos(){
  const svg=(p)=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
  const I={
    todos:svg('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
    volumes:svg('<path d="M21 8 12 3 3 8v8l9 5 9-5V8Z"/><path d="m3 8 9 5 9-5"/><path d="M12 13v8"/>'),
    'se-liga':svg('<path d="M12 6c-2-2-5-2-8-1v13c3-1 6-1 8 1 2-2 5-2 8-1V5c-3-1-6-1-8 1Z"/><path d="M12 6v13"/>'),
    saeb:svg('<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9z"/><path d="M9 11h6M9 15h6"/>'),
    apostilas:svg('<path d="M4 19V5a2 2 0 0 1 2-2h3v16H6a2 2 0 0 0-2 2Z"/><path d="M9 3h4v16H9z"/><path d="m13 5 3-1 4 15-3 1z"/>')
  };
  const c=k=>k==='todos'?ITENS.length:ITENS.filter(i=>i.tipo===k).length;
  $("#tipos").innerHTML=TIPOS.map(([k,n])=>`<button class="cert ${filtroTipo===k?'on':''}" onclick="setTipo('${k}')"><span class="ic">${I[k]||I.todos}</span><span class="ct"><b>${n}</b><small>${c(k)} ${c(k)===1?'material':'materiais'}</small></span></button>`).join("");
}
function setTipo(t){filtroTipo=t;tipos();render();document.getElementById('main').scrollIntoView({behavior:'smooth',block:'start'})}
function setGrupo(g){filtro=g;chips();render();document.getElementById('infoc').scrollIntoView({behavior:'smooth',block:'nearest'})}
/* miniaturas animadas: as páginas sobem (scroll vertical) enquanto o card está visível */
let io=null,rolando=false,tRol=null;
const todas=()=>[...document.querySelectorAll(".cover")];
function pararTodas(){todas().forEach(cv=>{if(cv._pause)cv._pause()})}
function voltarTodas(){todas().forEach(cv=>{if(cv._play&&cv._vis&&!cv._p)cv._play(500+Math.random()*900)})}
function rolandoAgora(ms){rolando=true;clearTimeout(tRol);pararTodas();tRol=setTimeout(()=>{rolando=false;voltarTodas()},ms)}
addEventListener("scroll",()=>rolandoAgora(260),{passive:true});
addEventListener("touchmove",()=>rolandoAgora(340),{passive:true});
addEventListener("touchstart",()=>rolandoAgora(340),{passive:true});
function anima(){
  if(io)io.disconnect();
  if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  io=new IntersectionObserver(es=>{
    es.forEach(e=>{const cv=e.target;
      if(e.isIntersecting){cv._vis=1;if(!cv._p&&!rolando)cv._play&&cv._play(600+Math.random()*2600)}
      else{cv._vis=0;cv._pause&&cv._pause()}});
  },{threshold:.18});
  todas().forEach(cv=>{const n=+cv.dataset.n;if(n<2)return;let k=0;
    /* cada card tem seu proprio ritmo: nada de animacoes sincronizadas */
    const CAPA=3200+Math.random()*4200, PAG=1500+Math.random()*2100;
    const bk=cv.querySelector(".book"),pgs=[...bk.querySelectorAll(".pg:not(.base)")],ds=cv.querySelectorAll(".dots i");
    const dot=i=>ds.forEach((d,j)=>d.classList.toggle("on",j===i%n));
    cv._reset=()=>{clearTimeout(cv._t);cv._t=null;if(k||bk.querySelector(".flip")){bk.classList.add("nt");pgs.forEach(p=>p.classList.remove("flip"));void bk.offsetHeight;bk.classList.remove("nt")}k=0;dot(0)};
    cv._pause=()=>{cv._p=1;cv._reset();cv._vis=cv._vis};
    cv._play=d=>{cv._p=0;clearTimeout(cv._t);cv._t=setTimeout(passo,d===undefined?400:d)};
    const passo=()=>{cv._t=null;
      if(rolando||cv._p||!cv._vis)return;
      if(k<n){pgs[k].classList.add("flip");k++;dot(k);
        if(k===n){cv._t=setTimeout(()=>{bk.classList.add("nt");pgs.forEach(p=>p.classList.remove("flip"));void bk.offsetHeight;bk.classList.remove("nt");k=0;dot(0);cv._t=setTimeout(passo,CAPA)},1500);return}}
      cv._t=setTimeout(passo,PAG)};
    /* mouse em cima (card inteiro): congela a animacao */
    const cardEl=cv.closest(".card")||cv;
    cardEl.addEventListener("mouseenter",()=>cv._pause(),{passive:true});
    cardEl.addEventListener("mouseleave",()=>{if(cv._vis&&!rolando)cv._play(400)},{passive:true});
    cv._reset();
    io.observe(cv);
  });
}
const NOMES=["Capa","Índice","Página interna","Página interna"];
let cur=null;
function abre(s){cur=ITENS.find(i=>i.slug===s);
  $("#th").innerHTML=cur.imgs.map((u,k)=>`<img src="${u}" onclick="foto(${k})" alt="">`).join("");
  const soon=!cur.link;
  $("#side").innerHTML=`<small style="color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.06em">${cur.grupoNome}</small><h3>${cur.nome}</h3><p>${cur.sub}</p>
   <p style="font-size:14px;color:var(--mut)">${cur.paginas?cur.paginas+' páginas · ':''}PDF digital${cur.slug.startsWith('cisop')||cur.grupo==='pss'||cur.grupo==='prefeitura'?' · inclui versão JUMBO (letra grande) quando disponível':''}</p>
   <div class="row"><div class="price"><span>R$</span>${brl(cur.preco)}</div>${soon?`<button class="btn wa" onclick="fecha();wabre('${cur.slug}')">Falar no WhatsApp</button>`:`<a class="btn buy" target="_blank" rel="noopener" href="${cur.link}">Comprar agora</a>`}</div>`;
  foto(0);$("#modal").classList.add("open");document.body.style.overflow="hidden";}
function foto(k){$("#big").src=cur.imgs[k];$("#lab").textContent=(cur.imgs.length>2?NOMES[k]:(k?"Índice":"Capa"))+" · "+(k+1)+"/"+cur.imgs.length;
  [...$("#th").children].forEach((e,i)=>e.classList.toggle("on",i===k));}
function fecha(){$("#modal").classList.remove("open");document.body.style.overflow=""}
document.addEventListener("keydown",e=>{if(e.key==="Escape")fecha();
  if($("#modal").classList.contains("open")&&cur){const on=[...$("#th").children].findIndex(x=>x.classList.contains("on"));
    if(e.key==="ArrowRight")foto(Math.min(on+1,cur.imgs.length-1));if(e.key==="ArrowLeft")foto(Math.max(on-1,0));}});
$("#q").addEventListener("input",e=>{busca=e.target.value;render()});
chips();tipos();render();
const WNUM="5545999699444";
const WOPT=[
 ["Tenho uma dúvida sobre um material","Olá, Prof. Rodrigo! Tenho uma dúvida sobre o material{P}.\nMinha dúvida é: ",
  "<b>Talvez já esteja respondido:</b><br>• Todos os materiais são <b>PDF digital</b>, para ler no celular, tablet ou computador.<br>• Antes de comprar, toque em <b>“ver páginas”</b> no card para conferir capa, índice e páginas internas.<br>• A versão <b>JUMBO</b> tem o mesmo conteúdo com letra maior.<br>• Para levar <b>vários materiais</b>, use o <b>🛒 carrinho</b>: ele gera um código de pedido e envia a lista pronta para o WhatsApp.<br>• A entrega é por <b>e-mail</b>, com os links da pasta do Drive, após a confirmação do pagamento.<br>Se ainda restar dúvida, escreva-a na mensagem abaixo."],
 ["Quero ajuda para escolher o material certo para o meu cargo","Olá, Prof. Rodrigo! Quero ajuda para escolher o material certo.\nConcurso: \nCargo/disciplina: ",
  "<b>Para eu indicar o material certo, informe:</b><br>• o <b>concurso</b> (PSS SEED-PR 2027, CISOP Cascavel, Prefeitura de Cascavel ou outro);<br>• o <b>cargo ou disciplina</b>;<br>• Dica: no PSS, a apostila <b>Conhecimentos Básicos</b> serve para todos os cargos, e a específica do seu cargo complementa."],
 ["Já paguei e não recebi o PDF","Olá, Prof. Rodrigo! Já fiz o pagamento{P}, mas ainda não recebi o PDF.\nNome completo: \nE-mail usado na compra: \nForma de pagamento (Pix, cartão ou boleto): \nJá olhei o spam/promoções: ",
  "<b>Antes de enviar, confira (resolve na maioria dos casos):</b><br>1. Olhe a caixa de <b>spam</b>, <b>lixo eletrônico</b> e <b>promoções</b> do e-mail usado na compra.<br>2. Veja se você digitou <b>o e-mail certo</b> no checkout.<br>3. Pix e cartão costumam liberar em poucos minutos; <b>boleto</b> só libera após a compensação, que pode levar alguns dias úteis.<br>4. Entre na sua conta Eduzz (<b>Minhas compras</b>) e baixe o arquivo por lá.<br><b>Se não resolver</b>, envie a mensagem abaixo com os dados preenchidos e, se puder, anexe o <b>comprovante</b> depois."],
 ["Quero comprar vários materiais juntos","Olá, Prof. Rodrigo! Montei um pedido no carrinho da loja{P}.\nCódigo do pedido: \nQuero pagar tudo junto.",
  "<b>Como funciona:</b><br>• Toque em <b>🛒 +</b> nos materiais e abra o <b>Carrinho</b>.<br>• Em <b>Enviar pedido</b>, o site gera um <b>código</b> (ex.: PED-261106-A7K2) e manda a lista organizada para o WhatsApp.<br>• Eu confiro os valores, envio o link de pagamento e, após o pagamento, o material chega no seu <b>e-mail</b> com os links do Drive."],
 ["Quero a versão JUMBO (letra grande)","Olá, Prof. Rodrigo! Gostaria da versão JUMBO (letra grande){P}. Pode me orientar?",
  "<b>O que é:</b> a versão <b>JUMBO</b> tem o mesmo conteúdo da apostila, com letra maior, mais confortável para ler na tela ou imprimir.<br>Em alguns materiais ela já vem junto na compra. Se não vier no seu, é só pedir pela mensagem abaixo."],
 ["Pedir um material de outra disciplina ou concurso","Olá, Prof. Rodrigo! Gostaria de pedir um material de outra disciplina/concurso.\nConcurso: \nCargo/disciplina: \nBanca (se souber): \nEdital (link ou nome): ",
  "<b>Para eu avaliar o pedido, informe:</b><br>• concurso e <b>cargo/disciplina</b>;<br>• <b>banca</b> e data da prova, se souber;<br>• o <b>edital</b> (link ou nome), pois monto o material em cima do conteúdo programático."],
 ["Quero ser avisado de novos materiais","Olá, Prof. Rodrigo! Quero ser avisado(a) quando sair material novo.\nConcurso/cargo de interesse: ",
  "Informe o <b>concurso e o cargo</b> de interesse. Você será avisado(a) assim que o material for publicado. Os itens marcados <b>“Em breve”</b> na loja já estão em produção."],
 ["Mentoria (plano de aula, ação ou atendimento)","Olá, Prof. Rodrigo! Tenho interesse na mentoria para a Prova Prática do PSS.\nQual serviço: (plano de aula, plano de ação, plano de atendimento, vídeo ou cadastro na plataforma)\nMinha disciplina: ",
  "<b>Conte qual serviço você quer:</b> plano de aula, plano de ação, plano de atendimento, orientação para o vídeo ou ajuda com o cadastro na plataforma.<br>Informe também a sua <b>disciplina</b>."],
 ["Outro assunto","Olá, Prof. Rodrigo! ",
  "Escreva sua mensagem abaixo. Se for sobre uma compra, inclua o <b>nome</b> e o <b>e-mail usado</b> no pedido para agilizar."]];
function wprod(){const v=$("#wprod").value;return v?" "+v:""}
function wbuild(){const i=+(document.querySelector('input[name=wo]:checked')||{value:0}).value;$("#wmsg").value=WOPT[i][1].replace("{P}",wprod()?" ("+wprod().trim()+")":"");$("#wtip").innerHTML=WOPT[i][2];wlink()}
const LOJA="https://hodhreego.github.io/Loja/";
function wlink(){const m=$("#wmsg").value.trim()+"\n\n🛒 Enviado pela loja: "+LOJA;$("#wgo").href="https://wa.me/"+WNUM+"?text="+encodeURIComponent(m)}
function winit(){
  $("#wopts").innerHTML=WOPT.map((o,i)=>`<label class="opt"><input type="radio" name="wo" value="${i}" ${i?'':'checked'} onchange="wbuild()"><span>${o[0]}</span></label>`).join("");
  $("#wprod").innerHTML='<option value="">— nenhum / não sei —</option>'+ITENS.map(i=>`<option value="Apostila ${i.nome} · ${i.grupoNome}">${i.nome} · ${i.grupoNome}</option>`).join("");
  $("#wprod").onchange=wbuild;$("#wmsg").oninput=wlink;wbuild();}
function wtoggle(force){const p=$("#wp");const on=force===undefined?!p.classList.contains("open"):force;p.classList.toggle("open",on);}
function wabre(slug,op){const it=ITENS.find(i=>i.slug===slug);if(it)$("#wprod").value="Apostila "+it.nome+" · "+it.grupoNome;const r=document.querySelector('input[name=wo][value="'+(op||0)+'"]');if(r)r.checked=true;wbuild();wtoggle(true);const w=document.querySelector(".wbody");if(w)w.scrollTop=0;}
/* ================= carrinho ================= */
const CKEY="loja.carrinho.v1";
/* URL do Web App do Apps Script (cole aqui depois de publicar); vazio = modo local */
const API_PEDIDOS="";
function cLoad(){try{return JSON.parse(localStorage.getItem(CKEY)||"[]")||[]}catch(e){return []}}
let CART=cLoad();
function cSave(){try{localStorage.setItem(CKEY,JSON.stringify(CART))}catch(e){}}
function cFind(s){return ITENS.find(i=>i.slug===s)}
function cCount(){return CART.reduce((s,x)=>s+x.q,0)}
function cTotal(){return CART.reduce((s,x)=>{const i=cFind(x.slug);return s+(i?i.preco*x.q:0)},0)}
function toast(t){const el=$("#toast");if(!el)return;el.textContent=t;el.classList.add("on");clearTimeout(el._t);el._t=setTimeout(()=>el.classList.remove("on"),1900)}
function addCart(s){const i=cFind(s);if(!i)return;const e=CART.find(x=>x.slug===s);if(e)e.q++;else CART.push({slug:s,q:1});cSave();cPaint();toast(i.nome+" no carrinho")}
function rmCart(s){CART=CART.filter(x=>x.slug!==s);cSave();cPaint()}
function qtyCart(s,d){const e=CART.find(x=>x.slug===s);if(!e)return;e.q+=d;if(e.q<1)CART=CART.filter(x=>x.slug!==s);cSave();cPaint()}
function ctoggle(f){const p=$("#cp");if(!p)return;const on=f===undefined?!p.classList.contains("open"):f;p.classList.toggle("open",on)}
function cPaint(){
  const n=cCount();const fb=$("#cartfab");if(fb){$("#cartn").textContent=n;fb.classList.toggle("on",n>0)}
  $("#ctot").textContent="R$ "+brl(cTotal());
  $("#cbody").innerHTML=CART.length?CART.map(x=>{const i=cFind(x.slug);if(!i)return"";
    return `<div class="citem"><img src="${i.imgs[0]||''}" alt=""><div class="cn">${i.nome}<small>${i.grupoNome} · R$ ${brl(i.preco)}</small></div><div class="cq"><button onclick="qtyCart('${i.slug}',-1)" aria-label="Menos">−</button><span>${x.q}</span><button onclick="qtyCart('${i.slug}',1)" aria-label="Mais">+</button></div></div>`}).join("")
    :`<p style="color:var(--mut);font-size:14px">Carrinho vazio. Toque em <b>🛒 +</b> no material que quiser.</p>`;
}
function cPedido(){
  const itens=CART.map(x=>{const i=cFind(x.slug);return i?{slug:i.slug,nome:i.nome,grupo:i.grupoNome,preco:i.preco,q:x.q}:null}).filter(Boolean);
  const total=itens.reduce((s,i)=>s+i.preco*i.q,0);
  return {criado:new Date().toISOString(),itens:itens,total:Math.round(total*100)/100};
}
function cTexto(p,cod){
  let t="🛒 *PEDIDO "+cod+"*\n\n";
  p.itens.forEach(i=>{t+="• "+i.q+"x "+i.nome+" — R$ "+brl(i.preco*i.q)+"\n"});
  t+="\n*Total: R$ "+brl(p.total)+"*\n\nConfira e me envie o link de pagamento. Depois do pagamento o material vai para o seu e-mail.";
  return t;
}
async function cfinal(){
  if(!CART.length){toast("Carrinho vazio");return}
  const p=cPedido();let cod="";
  if(API_PEDIDOS){
    try{
      const r=await fetch(API_PEDIDOS,{method:"POST",headers:{"Content-Type":"text/plain;charset=utf-8"},body:JSON.stringify({acao:"novo",pedido:p})});
      const j=await r.json();cod=j.codigo||"";
    }catch(e){}
  }
  if(!cod)cod="PED-"+new Date().toISOString().slice(2,10).replace(/-/g,"")+"-"+Math.random().toString(36).slice(2,6).toUpperCase();
  const base=location.origin+location.pathname.replace(/index\.html$/,"");
  const link=base+"pedido.html?p="+encodeURIComponent(cod);
  const txt=cTexto(p,cod)+(API_PEDIDOS?"\n\n🧾 Pedido: "+link:"");
  window.open("https://wa.me/"+WNUM+"?text="+encodeURIComponent(txt),"_blank");
  toast("Pedido "+cod+" enviado");
}
cPaint();
winit();
</script>
</body>
</html>'''
out = HTML.replace("__DATA__", json.dumps(items, ensure_ascii=False)).replace("__WA__", WA)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("ok", len(items), "itens")
