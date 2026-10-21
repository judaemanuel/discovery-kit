# -*- coding: utf-8 -*-
"""Pagina HTML autocontida (abas, inspetor, zoom, download SVG)."""
import json
from model import E, R, R1, RC, ADR, ADR_STATE, STATUS, FLOWS, META
from render_svg import svg_view, seq_svg, esc, KIND_LABEL

VIEW_TABS = META['tabs']
OPEN_LIMITS = META['open_limits']


def rels_of(i):
    out, inc = [], []
    for grp in (R, R1, RC):
        for a, b, t, tech, k in grp:
            if a == i:
                out.append((b, t, tech, k))
            if b == i:
                inc.append((a, t, tech, k))
    return out, inc


def data_json():
    d = {}
    for i, e in E.items():
        out, inc = rels_of(i)
        d[i] = dict(id=i, name=e['name'], tech=e['tech'], desc=e['desc'], kind=KIND_LABEL.get(e['kind'], e['kind']),
                    status=STATUS[e['status']]['label'], st=e['status'], adr=e['adr'], open=e['open'],
                    out=[dict(id=b, name=E[b]['name'], t=t, tech=tech) for b, t, tech, k in out if b in E],
                    inc=[dict(id=a, name=E[a]['name'], t=t, tech=tech) for a, t, tech, k in inc if a in E])
    adr = {a[0]: dict(id=a[0], decision=a[1], alt=a[2], ref=a[3], state=a[4], note=a[5]) for a in ADR}
    return json.dumps(dict(ent=d, adr=adr), ensure_ascii=False)


CSS = """
:root{--ink:#0F172A;--ink2:#334155;--ink3:#64748B;--line:#E2E8F0;--bg:#F1F5F9;--navy:#0B1F3A;--blue:#2563EB;--red:#DC2626}
*{box-sizing:border-box}
body{margin:0;font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;color:var(--ink);background:var(--bg)}
header{background:linear-gradient(120deg,#0B1F3A 0%,#15386B 60%,#1D4ED8 130%);color:#fff;padding:18px 28px 0}
header h1{margin:0;font-size:22px;font-weight:800;letter-spacing:.2px}
header p{margin:4px 0 12px;font-size:13px;color:#C7D7F2}
.badge{display:inline-block;background:#FDE68A;color:#78350F;font-weight:700;font-size:11px;border-radius:999px;padding:3px 10px;margin-left:10px;vertical-align:middle}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav button{appearance:none;border:0;background:transparent;color:#C7D7F2;font:600 13px 'Segoe UI',Arial;padding:10px 14px;border-radius:10px 10px 0 0;cursor:pointer}
nav button:hover{background:rgba(255,255,255,.12);color:#fff}
nav button.on{background:var(--bg);color:var(--ink)}
.legend{display:flex;flex-wrap:wrap;gap:18px;align-items:center;padding:10px 28px;background:#fff;border-bottom:1px solid var(--line);font-size:12px;color:var(--ink2)}
.legend .it{display:flex;align-items:center;gap:7px}
.sw{width:22px;height:14px;border-radius:4px;border:1.6px solid}
.ln{width:30px;height:0;border-top:2px solid}
main{padding:16px 28px 40px}
.view{display:none}.view.on{display:block}
.tools{display:flex;gap:8px;align-items:center;margin-bottom:10px}
.tools h2{font-size:17px;margin:0 12px 0 0}.tools .sub{font-size:12.5px;color:var(--ink3);margin-right:auto}
.btn{appearance:none;border:1px solid #CBD5E1;background:#fff;color:var(--ink);font:600 12px 'Segoe UI',Arial;border-radius:8px;padding:6px 11px;cursor:pointer}
.btn:hover{background:#EFF6FF;border-color:#93B4F0}
.stage{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:14px;align-items:start}
.stage.solo{grid-template-columns:minmax(0,1fr)}
.canvas{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:auto;max-height:calc(100vh - 250px);box-shadow:0 1px 3px rgba(15,23,42,.06)}
.canvas svg{display:block}
.node{cursor:pointer}.node:focus{outline:none}
.node:hover rect,.node:focus rect,.node.sel rect{filter:drop-shadow(0 2px 6px rgba(37,99,235,.45))}
.node.sel rect{stroke-width:3}
svg .dim{opacity:.16;transition:opacity .15s}
svg .edge{transition:opacity .15s}
.inspector{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;position:sticky;top:12px;max-height:calc(100vh - 250px);overflow:auto}
.inspector h3{margin:0 0 4px;font-size:17px}
.inspector .tag{font-size:10.5px;letter-spacing:1px;font-weight:800;color:var(--ink3)}
.inspector .tech{font-style:italic;color:var(--ink3);font-size:12.5px;margin:2px 0 8px}
.inspector p{font-size:13.5px;line-height:1.45;color:var(--ink2);margin:6px 0}
.inspector h4{font-size:11px;letter-spacing:1.1px;color:var(--ink3);margin:14px 0 5px;font-weight:800}
.inspector ul{margin:0;padding-left:18px;font-size:13px;color:var(--ink2);line-height:1.45}
.inspector li{margin:3px 0}
.inspector a{color:var(--blue);cursor:pointer;text-decoration:none;font-weight:600}.inspector a:hover{text-decoration:underline}
.open li{color:#7F1D1D}
.chip{display:inline-block;font-size:11px;font-weight:700;border-radius:999px;padding:2px 9px;margin:0 4px 4px 0;border:1px solid}
.chip.adr{background:#FEE2E2;color:#991B1B;border-color:#FCA5A5;cursor:pointer}
.hint{color:var(--ink3);font-size:13px;line-height:1.5}
.doc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 26px;max-width:1200px}
.doc h2{margin:0 0 4px;font-size:20px}.doc .sub{color:var(--ink3);font-size:13px;margin-bottom:16px}
table{border-collapse:collapse;width:100%;font-size:13px}
th{text-align:left;font-size:11px;letter-spacing:1px;color:var(--ink3);padding:8px 10px;border-bottom:2px solid var(--line)}
td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--ink2);line-height:1.4}
td b{color:var(--ink)}
td:first-child{white-space:nowrap}
.pill{display:inline-block;border-radius:999px;font-size:11px;font-weight:800;padding:3px 10px;white-space:nowrap}
.pill.aberto{background:#FEE2E2;color:#991B1B}.pill.tend{background:#FEF3C7;color:#92400E}.pill.nossa{background:#DBEAFE;color:#1E40AF}
tr.hl td{background:#FFFBEB}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.card{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:#FAFBFD}
.card h3{margin:0 0 8px;font-size:14px}.card li{font-size:13px;margin:5px 0;color:var(--ink2);line-height:1.4}
.card ul{padding-left:18px;margin:0}
.slidewrap{background:#CBD5E1;border-radius:14px;padding:18px;overflow:auto}
.slidewrap svg{display:block;margin:0 auto;box-shadow:0 8px 30px rgba(15,23,42,.25);max-width:100%;height:auto}
@media print{header,nav,.legend,.tools,.inspector{display:none}.view{display:none!important}.view.on{display:block!important}.canvas{max-height:none;border:0}}
"""

JS = """
const DATA=JSON.parse(document.getElementById('data').textContent);
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
let scale={};
function show(id){
  $$('.view').forEach(v=>v.classList.toggle('on',v.id==='v-'+id));
  $$('nav button').forEach(b=>b.classList.toggle('on',b.dataset.t===id));
  history.replaceState(null,'','#'+id); fit(id);
}
function svgOf(id){return $('#v-'+id+' svg')}
function apply(id){const s=svgOf(id); if(!s)return; const vb=s.viewBox.baseVal; s.style.width=(vb.width*scale[id])+'px'; s.style.height=(vb.height*scale[id])+'px'}
function fit(id){const s=svgOf(id); if(!s)return; const c=s.parentElement; const vb=s.viewBox.baseVal;
  const w=c.clientWidth-2; scale[id]=Math.min(1,w/vb.width); if(id==='slide')scale[id]=Math.min(1,(c.clientWidth-40)/vb.width); apply(id)}
function zoom(id,f){scale[id]=Math.max(.25,Math.min(2.5,(scale[id]||1)*f)); apply(id)}
function dl(id){const s=svgOf(id); const blob=new Blob(['<?xml version="1.0" encoding="UTF-8"?>'+s.outerHTML.replace(/ style="[^"]*"/,'')],{type:'image/svg+xml'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='__PFX__'+id+'.svg'; a.click()}
function chipsAdr(ids){return ids.map(a=>`<span class="chip adr" data-adr="${a}" title="${DATA.adr[a]?DATA.adr[a].decision:''}">${a}</span>`).join('')}
function sel(view,id){
  const root=$('#v-'+view); $$('.node',root).forEach(n=>n.classList.toggle('sel',n.dataset.id===id));
  const e=DATA.ent[id]; const box=$('.inspector',root); if(!e||!box)return;
  const li=(a)=>`<li><a data-go="${a.id}">${a.name}</a> — ${a.t}${a.tech?` <i style="color:#64748B">(${a.tech})</i>`:''}</li>`;
  let h=`<div class="tag">${e.kind}${e.st!=='pessoa'?' · '+e.status.toUpperCase():''}</div><h3>${e.name}</h3>`;
  if(e.tech)h+=`<div class="tech">${e.tech}</div>`; h+=`<p>${e.desc}</p>`;
  if(e.adr.length)h+=`<h4>DECISÕES RELACIONADAS</h4><div>${chipsAdr(e.adr)}</div>`+e.adr.map(a=>DATA.adr[a]?`<p><b>${a}</b> — ${DATA.adr[a].decision}</p>`:'').join('');
  if(e.open.length)h+=`<h4>PONTOS EM ABERTO</h4><ul class="open">${e.open.map(o=>`<li>${o}</li>`).join('')}</ul>`;
  if(e.out.length)h+=`<h4>SAI PARA</h4><ul>${e.out.map(li).join('')}</ul>`;
  if(e.inc.length)h+=`<h4>RECEBE DE</h4><ul>${e.inc.map(li).join('')}</ul>`;
  box.innerHTML=h;
  $$('[data-go]',box).forEach(a=>a.onclick=()=>{const t=a.dataset.go; const n=$('.node[data-id="'+t+'"]',root); if(n)sel(view,t); else sel(view,t)});
  $$('.chip.adr',box).forEach(c=>c.onclick=()=>{show('adr'); const r=$('#adr-'+c.dataset.adr); if(r){r.classList.add('hl'); r.scrollIntoView({block:'center'})}});
  hl(root,id);
}
function hl(root,id){
  const edges=$$('.edge',root); const conn=new Set([id]);
  edges.forEach(e=>{if(e.dataset.src===id||e.dataset.dst===id){conn.add(e.dataset.src);conn.add(e.dataset.dst)}});
  edges.forEach(e=>e.classList.toggle('dim',!(e.dataset.src===id||e.dataset.dst===id)));
  $$('.node',root).forEach(n=>n.classList.toggle('dim',!conn.has(n.dataset.id)));
}
function clear(root){$$('.dim',root).forEach(x=>x.classList.remove('dim')); $$('.node.sel',root).forEach(x=>x.classList.remove('sel'));
  const box=$('.inspector',root); if(box)box.innerHTML=box.dataset.hint}
document.addEventListener('DOMContentLoaded',()=>{
  $$('nav button').forEach(b=>b.onclick=()=>show(b.dataset.t));
  $$('.view').forEach(v=>{const id=v.id.slice(2);
    $$('.node[data-id]',v).forEach(n=>{n.onclick=ev=>{ev.stopPropagation();sel(id,n.dataset.id)};n.onkeydown=ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();sel(id,n.dataset.id)}}});
    const cv=$('.canvas',v); if(cv)cv.onclick=()=>clear(v);
    $$('[data-z]',v).forEach(b=>b.onclick=()=>b.dataset.z==='fit'?fit(id):zoom(id,parseFloat(b.dataset.z)));
    $$('[data-dl]',v).forEach(b=>b.onclick=()=>dl(id));
    const box=$('.inspector',v); if(box)box.dataset.hint=box.innerHTML;
  });
  const h=location.hash.slice(1); show($('#v-'+h)?h:'c2');
  window.addEventListener('resize',()=>{const on=$('.view.on'); if(on)fit(on.id.slice(2))});
});
"""


def legend():
    sw = ''.join('<span class="it"><span class="sw" style="background:%s;border-color:%s;%s"></span>%s</span>' % (
        STATUS[k]['fill'], STATUS[k]['stroke'], 'border-style:dashed;' if STATUS[k]['dash'] else '', STATUS[k]['label'])
        for k in ('novo', 'reuso', 'existente'))
    ln = ('<span class="it"><span class="ln" style="border-color:#334155"></span>síncrono</span>'
          '<span class="it"><span class="ln" style="border-color:#7C3AED;border-top-style:dashed"></span>evento (Kafka)</span>'
          '<span class="it"><span class="ln" style="border-color:#0E7490;border-top-style:dotted"></span>arquivo / lote</span>'
          '<span class="it"><span class="pill aberto" style="font-size:10px;padding:1px 8px">ADR-nn</span>decisão arquitetural (ver aba Decisões)</span>')
    return '<div class="legend">%s%s</div>' % (sw, ln)


def view_section(key, title, kind, subtitle, svg, solo=False):
    tools = ('<div class="tools"><h2>%s</h2><span class="sub">%s</span>'
             '<button class="btn" data-z="0.8">−</button><button class="btn" data-z="1.25">+</button>'
             '<button class="btn" data-z="fit">Ajustar</button><button class="btn" data-dl="1">Baixar SVG</button></div>') % (esc(title), esc(subtitle))
    hint = '<div class="hint"><b>Como usar</b><br>Clique em um bloco para ver responsabilidade, decisões relacionadas, pontos em aberto e relações. As demais conexões ficam esmaecidas.<br><br>Clique no fundo para limpar.</div>'
    insp = '' if (solo or kind == 'seq') else '<aside class="inspector">%s</aside>' % hint
    cls = 'stage solo' if (solo or kind == 'seq') else 'stage'
    inner = '<div class="canvas">%s</div>%s' % (svg, insp) if key != 'slide' else '<div class="slidewrap canvas">%s</div>' % svg
    return '<section class="view" id="v-%s">%s<div class="%s">%s</div></section>' % (key, tools, cls, inner)


def adr_section():
    rows = ''
    for a in ADR:
        rows += ('<tr id="adr-%s"><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td><span class="pill %s">%s</span><br><span style="font-size:12px;color:#64748B">%s</span></td></tr>' % (
            a[0], a[0], esc(a[1]), esc(a[2]), esc(a[3]), a[4], ADR_STATE[a[4]], esc(a[5])))
    opn = ''.join('<li><b>%s</b> — %s</li>' % (esc(a), esc(b)) for a, b in OPEN_LIMITS)
    pr = '<ul>' + ''.join(META['principles']) + '</ul>'
    return ('<section class="view" id="v-adr"><div class="doc"><h2>Decisões arquiteturais (ADR-lite)</h2>'
            '<div class="sub">' + META['adr_sub'] + '</div>'
            '<table><thead><tr><th>ID</th><th>DECISÃO PROPOSTA</th><th>ALTERNATIVAS</th><th>DEPENDE DE</th><th>SITUAÇÃO</th></tr></thead><tbody>%s</tbody></table>'
            '<div class="grid2"><div class="card"><h3>Princípios de design</h3>%s</div><div class="card"><h3>O que este desenho não resolve</h3><ul>%s</ul></div></div></div></section>') % (rows, pr, opn)


def sobre_section():
    sb = META['sobre']
    cards = ''.join('<div class="card"><h3>%s</h3><ul>%s</ul></div>' % (t, ''.join(li)) for t, li in sb['cards'])
    return ('<section class="view" id="v-sobre"><div class="doc"><h2>Sobre este material</h2>'
            '<div class="sub">' + sb['sub'] + '</div>'
            '<div class="grid2">' + cards + '</div></div></section>')


def build(views):
    secs, tabs = [], []
    meta = {k: (t, kind) for k, t, kind in VIEW_TABS}
    for key, label, kind in VIEW_TABS:
        tabs.append('<button data-t="%s">%s</button>' % (key, esc(label)))
        if kind == 'blk':
            v = views[key]
            secs.append(view_section(key, v.title, kind, v.sub, svg_view(v), solo=(key == 'slide')))
        elif kind == 'seq':
            f = FLOWS[key]
            secs.append(view_section(key, f['title'], kind, META['flow_hint'], seq_svg(f)))
    secs.append(adr_section())
    secs.append(sobre_section())
    # ordenar para que a ordem das secoes siga as abas nao importa (display por aba)
    page = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + esc(META['page_title']) + '</title><style>%s</style></head><body>'
            '<header><h1>' + esc(META['title']) + '<span class="badge">' + esc(META['badge']) + '</span></h1>'
            '<p>' + esc(META['subtitle']) + '</p><nav>%s</nav></header>%s<main>%s</main>'
            '<script id="data" type="application/json">%s</script><script>%s</script></body></html>') % (
        CSS, ''.join(tabs), legend(), ''.join(secs), data_json().replace('</', '<\\/'), JS.replace('__PFX__', META['download_prefix']))
    return page
