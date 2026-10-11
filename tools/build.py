"""Bouwt de plantenreels (Pilea, Sansevieria, Chlorophytum) als losse HTML-pagina's.
Gebruik: python3 build.py <uitvoermap> [--artifact]
--artifact: zonder doctype/head-skelet en zonder terugknop (voor claude.ai-preview)."""
import sys, os, math

OUT = sys.argv[1]
ARTIFACT = '--artifact' in sys.argv
ORDER = ['rubberboom', 'pannenkoekenplant', 'vrouwentong', 'graslelie']  # volgorde voor swipen tussen planten; nieuwe plant hier toevoegen
import json
INK = '#141414'

BASE_CSS = r"""
:root{
  --desk:#FFD60A; --ink:#141414; --paper:#FFFDF6;
  --leaf:#2E9E4F; --leaf-lt:#8ED19B; --teal:#0F8A8F; --sun:#F5C400;
  --blue:#2F6FD6; --purple:#5B2A9E; --red:#D8263A; --pot:#FFE24A;
  --display:"Bricolage Grotesque",system-ui,sans-serif;
  --hand:"Caveat","Comic Sans MS",cursive;
  color-scheme:light;
}
html,body{height:100%}
body{background:var(--desk);color:var(--ink);font-family:var(--display);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding-inline:16px;padding-block:12px;box-sizing:border-box;margin:0}
.stage{position:relative;width:min(100%,calc((100dvh - __OFF__px)*9/16));aspect-ratio:9/16;max-width:100%;border:3px solid var(--ink);border-radius:22px;overflow:hidden;background:var(--paper);box-shadow:8px 8px 0 var(--ink);cursor:pointer;container-type:inline-size}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:7cqw 6cqw 8cqw;box-sizing:border-box;opacity:0;visibility:hidden;transition:opacity .35s;color:var(--ink)}
.scene.on{opacity:1;visibility:visible}
.scene.dk{color:var(--paper)}
.tag{font:800 3.6cqw/1 var(--display);letter-spacing:.14em;text-transform:uppercase;background:var(--ink);color:var(--paper);padding:1.6cqw 3cqw;border-radius:99px;align-self:flex-start}
.dk .tag{background:var(--paper);color:var(--ink)}
h2{font:800 11cqw/.95 var(--display);margin:0;text-wrap:balance;letter-spacing:-.02em;text-align:center}
.sub{font:700 8cqw/1.05 var(--hand);text-align:center;margin:0;text-wrap:balance}
.note{font:700 8.8cqw/1.05 var(--hand);text-align:center;margin:0}
.col{display:flex;flex-direction:column;gap:3cqw;align-items:center;width:100%;text-align:center}
svg.art{width:86cqw;height:auto;overflow:visible}
.scene .a{opacity:0}
.scene.on .a{animation:pop .55s cubic-bezier(.3,1.6,.5,1) forwards}
.scene.on .d1{animation-delay:.25s}.scene.on .d2{animation-delay:.6s}.scene.on .d3{animation-delay:1s}.scene.on .d4{animation-delay:1.5s}.scene.on .d5{animation-delay:2.1s}.scene.on .d6{animation-delay:2.7s}.scene.on .d7{animation-delay:3.3s}
@keyframes pop{0%{opacity:0;transform:translateY(14px) scale(.6)}100%{opacity:1;transform:none}}
.grow{transform-box:fill-box;transform-origin:50% 100%}
.scene.on .grow{animation:grow .6s cubic-bezier(.3,1.7,.5,1) both}
@keyframes grow{0%{transform:scale(0) rotate(-20deg)}100%{transform:none}}
.rise{transform-box:fill-box;transform-origin:50% 100%}
.scene.on .rise{animation:rise .7s cubic-bezier(.3,1.5,.5,1) both}
@keyframes rise{0%{transform:scaleY(0)}100%{transform:none}}
.chip{display:inline-block;border:3px solid currentColor;border-radius:14px;padding:1cqw 3cqw;font:700 8cqw/1 var(--hand)}
/* afstoffen */
.dust circle{fill:#9a8f7a}
.scene.on .dust{animation:fade 2.6s 1.2s forwards}
@keyframes fade{to{opacity:0;transform:translateX(30px)}}
.scene.on .wipe{animation:wipe 1.6s 1.1s ease-in-out forwards}
@keyframes wipe{0%{transform:translate(-90px,40px)}50%{transform:translate(40px,-10px)}100%{transform:translate(160px,-60px);opacity:0}}
.shine{opacity:0}
.scene.on .shine{animation:show 1s 2.6s forwards}
@keyframes show{to{opacity:1}}
/* water */
.mist{transform-box:fill-box;transform-origin:100% 50%;opacity:0}
.scene.on .mist{animation:mist 1s .5s 4 ease-out}
@keyframes mist{0%{opacity:0;transform:scale(.3)}40%{opacity:1}100%{opacity:0;transform:scale(1.2)}}
.drop{transform-box:fill-box;opacity:0}
.scene.on .drop{animation:fall 1.4s ease-in infinite}
@keyframes fall{0%{transform:translateY(-30px);opacity:0}20%{opacity:1}100%{transform:translateY(70px);opacity:0}}
.cal{display:grid;gap:1.5cqw;width:100%}
.cal span{aspect-ratio:1;border:2.5px solid currentColor;border-radius:8px;display:grid;place-items:center;font:800 3.4cqw var(--display)}
.cal span.w{background:currentColor}
.cal span.w b{color:var(--paper)}
/* licht */
.rays{transform-box:fill-box;transform-origin:center}
.scene.on .rays{animation:spin 8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.in{display:inline-block;text-decoration:underline;text-decoration-thickness:.12em;text-underline-offset:.08em}
.scene.on .in{animation:slam .5s 1.2s cubic-bezier(.3,1.8,.5,1) both}
@keyframes slam{0%{transform:translateY(-120%) scale(2);opacity:0}100%{transform:none;opacity:1}}
.dir{color:#B58F00}
.glow{transform-box:fill-box;transform-origin:center}
.scene.on .glow{animation:glow 1.1s ease-in-out infinite alternate}
@keyframes glow{from{opacity:.35}to{opacity:1}}
/* tekenen */
.cross{stroke-dasharray:400;stroke-dashoffset:400}
.scene.on .cross{animation:draw .5s var(--cd,2s) forwards}
.tick{stroke-dasharray:200;stroke-dashoffset:200}
.scene.on .tick{animation:draw .5s var(--cd,2s) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.flash{transform-box:fill-box;transform-origin:center}
.scene.on .flash{animation:flash .5s .4s 6 alternate}
@keyframes flash{from{transform:scale(1)}to{transform:scale(1.18)}}
/* lucht */
.src{display:flex;flex-direction:column;gap:2cqw;width:100%}
.need{background:var(--leaf);color:var(--paper);border-radius:16px;padding:3cqw 5cqw;font:800 6.2cqw/1.1 var(--display);text-align:center;width:100%;box-sizing:border-box}
.need small{display:block;font:700 6cqw/1 var(--hand);margin-top:1cqw}
.mol{font:800 22px var(--display);fill:var(--red)}
.pair{display:grid;grid-template-columns:24cqw 1fr;gap:3cqw;align-items:center;width:100%}
.pair svg{width:100%;height:auto}
.pair b{font:800 7.4cqw/1 var(--display);color:var(--red);display:block}
.pair span{font:700 7cqw/1 var(--hand)}
/* recap */
.recap{display:grid;grid-template-columns:1fr 1fr;gap:2.5cqw;width:100%}
.recap div{border-radius:14px;padding:3cqw;font:700 6.6cqw/1.02 var(--hand);color:var(--ink);text-align:left}
.recap b{display:block;font:800 3.2cqw var(--display);letter-spacing:.1em;text-transform:uppercase;margin-bottom:1cqw}
/* balk + knoppen */
.bars{position:absolute;top:2.4cqw;left:4cqw;right:4cqw;display:flex;gap:1.2cqw;z-index:5}
.bars i{flex:1;height:5px;border-radius:9px;background:rgba(20,20,20,.18);overflow:hidden}
.bars i b{display:block;height:100%;width:0;background:var(--ink)}
.dark .bars i{background:rgba(255,253,246,.3)}.dark .bars i b{background:var(--paper)}
.ctrl{display:flex;gap:10px;align-items:center}
.ctrl button{font:800 15px var(--display);background:var(--paper);color:var(--ink);border:3px solid var(--ink);border-radius:99px;padding:8px 16px;box-shadow:3px 3px 0 var(--ink);cursor:pointer}
.ctrl button:active{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--ink)}
.ctrl button:focus-visible{outline:3px solid var(--purple);outline-offset:3px}
#play{min-width:96px}
.home{position:fixed;top:calc(10px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);z-index:10;width:min(calc(100% - 32px),420px);box-sizing:border-box;display:flex;align-items:center;justify-content:center;gap:10px;padding:11px 18px;background:var(--paper);color:var(--ink);font:800 18px/1 var(--display);text-decoration:none;border:3px solid var(--ink);border-radius:99px;box-shadow:4px 4px 0 var(--ink);transition:transform .1s,box-shadow .1s}.home svg{width:28px;height:22px;flex:none}.home:hover{background:#FFF1A8}.home:active{transform:translateX(-50%) translate(3px,3px);box-shadow:1px 1px 0 var(--ink)}.home:focus-visible{outline:3px solid var(--purple);outline-offset:3px}
.stage{touch-action:none;user-select:none;-webkit-user-select:none}
.hint{font:600 13px/1.3 var(--display);margin:0;text-align:center;opacity:.75}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important}.scene .a,.shine{opacity:1}*{animation-delay:0s!important}}
"""

JS = r"""
(function(){
  const stage=document.getElementById('stage');
  const scenes=[...stage.querySelectorAll('.scene')];
  const bars=document.getElementById('bars');
  scenes.forEach(()=>{const i=document.createElement('i');i.appendChild(document.createElement('b'));bars.appendChild(i)});
  const fills=[...bars.querySelectorAll('b')];
  const playBtn=document.getElementById('play');
  let idx=0,playing=true,elapsed=0,last=performance.now(),ended=false;
  function show(n){
    idx=(n+scenes.length)%scenes.length;elapsed=0;ended=false;
    scenes.forEach(s=>s.classList.remove('on'));
    void stage.offsetWidth;
    scenes[idx].classList.add('on');
    stage.classList.toggle('dark',scenes[idx].classList.contains('dk'));
    fills.forEach((f,i)=>f.style.width=i<idx?'100%':'0%');
    document.dispatchEvent(new CustomEvent('reel:scene',{detail:idx}));
  }
  function setPlay(p){playing=p;playBtn.textContent=p?'Pauze':'Speel';stage.querySelectorAll('.scene.on *').forEach(el=>el.style.animationPlayState=p?'running':'paused')}
  window.__reel={go:i=>{show(i);setPlay(true)}};
  function tick(t){
    const dt=t-last;last=t;
    if(playing&&!ended){
      elapsed+=dt;const d=+scenes[idx].dataset.dur;
      fills[idx].style.width=Math.min(100,elapsed/d*100)+'%';
      if(elapsed>=d){ if(idx===scenes.length-1){ended=true;playing=false;playBtn.textContent='Opnieuw';} else show(idx+1); }
    }
    requestAnimationFrame(tick);
  }
  playBtn.addEventListener('click',()=>{ if(ended){show(0);setPlay(true);} else setPlay(!playing); });
  let swiped=false;
  stage.addEventListener('click',()=>{if(swiped){swiped=false;return;}playBtn.click();});
  const nav=JSON.parse(stage.dataset.nav||'{}');
  let sx=0,sy=0,down=false;
  stage.addEventListener('pointerdown',e=>{sx=e.clientX;sy=e.clientY;down=true});
  stage.addEventListener('pointercancel',()=>{down=false});
  stage.addEventListener('pointerup',e=>{
    if(!down)return;down=false;
    const dx=e.clientX-sx,dy=e.clientY-sy;
    if(Math.max(Math.abs(dx),Math.abs(dy))<40)return;
    swiped=true;
    if(Math.abs(dx)>Math.abs(dy)){
      if(dx<0){ if(idx===scenes.length-1&&nav.next){location.href=nav.next;return;} show(idx+1);setPlay(true); }
      else { show(idx-1);setPlay(true); }
    } else { const u=dy<0?nav.next:nav.prev; if(u) location.href=u; }
  });

  document.getElementById('prev').addEventListener('click',()=>{show(idx-1);setPlay(true)});
  document.getElementById('next').addEventListener('click',()=>{show(idx+1);setPlay(true)});
  document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')document.getElementById('next').click();if(e.key==='ArrowLeft')document.getElementById('prev').click();if(e.key===' '){e.preventDefault();playBtn.click()}});
  show(0);requestAnimationFrame(tick);
})();
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Caveat:wght@600;700&display=swap">'


def page(slug, title, desc, scenes, extra_css=''):
    css = BASE_CSS.replace('__OFF__', '134' if ARTIFACT else '198')
    if not ARTIFACT:
        css += 'body{padding-top:calc(66px + env(safe-area-inset-top,0px))}'
    body = ''.join(
        f'<section class="scene{" dk" if s.get("dark") else ""}" data-dur="{s["dur"]}" style="background:{s["bg"]}">{s["html"]}</section>\n'
        for s in scenes)
    _here = os.path.dirname(os.path.abspath(__file__))
    LAYOUT_CSS = open(os.path.join(_here, 'layout.css')).read()
    LAYOUT_JS = open(os.path.join(_here, 'layout.js')).read()
    core = f"""<title>{title}</title>
{FONTS}
<style>{css}{extra_css}</style>
<style id="layout">{LAYOUT_CSS}</style>
"""
    navattr = ''
    hint = 'Veeg ← → door de fiche'
    if not ARTIFACT and slug in ORDER:
        i = ORDER.index(slug); n = len(ORDER)
        nav = json.dumps({'prev': '../'+ORDER[(i-1)%n]+'/', 'next': '../'+ORDER[(i+1)%n]+'/'}).replace('"', '&quot;')
        navattr = f' data-nav="{nav}"'
        hint += ' · ↑ ↓ naar een andere plant'
    main = f"""<div class="stage" id="stage" aria-live="polite"{navattr}>
<div class="bars" id="bars"></div>
{body}</div>
<div class="ctrl">
<button id="prev" type="button" aria-label="Vorige scène">◀</button>
<button id="play" type="button">Pauze</button>
<button id="next" type="button" aria-label="Volgende scène">▶</button>
</div>
<p class="hint">{hint}</p>
<script>{JS}</script>
<script id="layout-js">{LAYOUT_JS}</script>
"""
    if ARTIFACT:
        html = core + main
        path = os.path.join(OUT, slug + '.html')
    else:
        html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FFD60A">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Plantplek">
<link rel="manifest" href="../manifest.webmanifest">
<link rel="icon" href="../icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../icons/apple-touch-icon.png">
{core}</head>
<body>
<a class="home" href="../"><span aria-hidden="true" style="font-size:24px;line-height:1">&larr;</span><svg viewBox="0 0 28 22" aria-hidden="true"><path d="M5 9V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4" fill="#9BB9EE" stroke="#141414" stroke-width="2"/><path d="M2 10h24v7H2Z" fill="#7FA4E6" stroke="#141414" stroke-width="2" stroke-linejoin="round"/><path d="M5 17v3M23 17v3" stroke="#141414" stroke-width="2.4" stroke-linecap="round"/></svg>Terug naar de kamer</a>
{main}</body>
</html>
"""
        os.makedirs(os.path.join(OUT, slug), exist_ok=True)
        path = os.path.join(OUT, slug, 'index.html')
    open(path, 'w').write(html)
    print('geschreven', path)

# ---------- gedeelde tekenstukjes ----------

def sun(cx, cy, r, half=False, ray=26):
    rays = ''.join(
        f'<path d="M{cx+math.cos(a)*(r+8):.1f} {cy+math.sin(a)*(r+8):.1f}L{cx+math.cos(a)*(r+8+ray):.1f} {cy+math.sin(a)*(r+8+ray):.1f}"/>'
        for a in [i*math.pi/4 for i in range(8)])
    core = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#F5C400" stroke="{INK}" stroke-width="6"/>'
    if half:
        core += f'<path d="M{cx} {cy-r}A{r} {r} 0 0 0 {cx} {cy+r}Z" fill="{INK}"/>'
    else:
        core += f'<circle cx="{cx}" cy="{cy}" r="{r*0.42:.0f}" fill="{INK}"/>'
    return f'<g class="rays"><g stroke="{INK}" stroke-width="6" stroke-linecap="round">{rays}</g></g>{core}'

def dust_wipe():
    return f'''<g class="dust"><circle cx="110" cy="120" r="4"/><circle cx="130" cy="90" r="3"/><circle cx="150" cy="140" r="5"/><circle cx="170" cy="100" r="3.5"/><circle cx="120" cy="160" r="3"/><circle cx="160" cy="70" r="4"/><circle cx="185" cy="130" r="3"/><circle cx="100" cy="190" r="4"/></g>
<g class="shine"><path d="M205 60l6 14 14 6-14 6-6 14-6-14-14-6 14-6Z" fill="#FFD60A" stroke="{INK}" stroke-width="3"/><path d="M90 80l4 9 9 4-9 4-4 9-4-9-9-4 9-4Z" fill="#FFD60A" stroke="{INK}" stroke-width="3"/></g>
<g class="wipe"><rect x="100" y="130" width="70" height="56" rx="6" fill="#fff" stroke="{INK}" stroke-width="4" transform="rotate(-12 135 158)"/></g>'''

def spray(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">
<path d="M0 0h40v-24c22 0 30 14 30 30v8h-16v-8c0-6-4-10-10-10" fill="{INK}"/>
<rect x="0" y="-14" width="16" height="20" fill="{INK}"/>
<path d="M20 6L-30 110h110Z" fill="#2F6FD6" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
<g class="mist"><path d="M-4 -4l-40-26M-4 -4l-46-6M-4 -4l-44 14M-4 -4l-36 30M-4 -4l-28-38" stroke="#2F6FD6" stroke-width="4" stroke-linecap="round"/></g></g>'''

def drop(x, y, s=1, cls='', fill='#0F8A8F', style=''):
    return f'<g class="{cls}" style="{style}"><path transform="translate({x} {y}) scale({s})" d="M0 0c-10 15-10 25 0 25s10-10 0-25Z" fill="{fill}" stroke="{INK}" stroke-width="{2.5/s:.2f}"/></g>'

def ghs(x, y, s, inner):
    return f'''<g transform="translate({x} {y}) scale({s})"><rect x="-38" y="-38" width="76" height="76" transform="rotate(45)" fill="#fff" stroke="#D8263A" stroke-width="9" stroke-linejoin="round"/>{inner}</g>'''

SKULL = f'<g fill="{INK}"><path d="M-16 -22a16 15 0 1 1 32 0c0 8-4 11-6 13v6h-20v-6c-2-2-6-5-6-13Z"/><path d="M-26 6l52 18M-26 24l52-18" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></g><circle cx="-7" cy="-21" r="4.5" fill="#fff"/><circle cx="7" cy="-21" r="4.5" fill="#fff"/>'
FLAME = f'<path d="M0 20c-16 0-22-10-18-22 3-8 9-10 8-20 9 5 12 13 10 20 3-3 5-7 4-12 8 7 12 15 10 22-3 8-8 12-14 12Z" fill="{INK}"/><path d="M-22 26h44" stroke="{INK}" stroke-width="5"/>'

def formaldehyde(x, y):
    return f'''<g transform="translate({x} {y})" class="mol-g"><text x="-8" y="-46" class="mol">O</text>
<path d="M-4 -40v26M6 -40v26" stroke="#D8263A" stroke-width="4"/>
<text x="-8" y="10" class="mol">C</text>
<path d="M-12 6l-22 16M16 6l22 16" stroke="#D8263A" stroke-width="4"/>
<text x="-50" y="40" class="mol">H</text><text x="36" y="40" class="mol">H</text></g>'''

def benzene(x, y, r=26):
    pts = ' '.join(f'{x+r*math.cos(math.pi/6+i*math.pi/3):.1f},{y+r*math.sin(math.pi/6+i*math.pi/3):.1f}' for i in range(6))
    return f'<polygon points="{pts}" fill="none" stroke="#D8263A" stroke-width="4"/><circle cx="{x}" cy="{y}" r="{r*0.55:.1f}" fill="none" stroke="#D8263A" stroke-width="3"/>'

def light_scene(note, half=False, extra=''):
    return f'''<span class="tag a">Licht</span>
<svg class="art" viewBox="0 0 300 240" aria-hidden="true" style="width:62cqw">{sun(150,120,58,half)}{extra}</svg>
<div class="col"><h2><span class="in">in</span><span class="dir">direct</span><br>zonlicht</h2>{note}</div>'''

def recap(items):
    cells = ''.join(f'<div class="a d{2+i//2}" style="background:{c}"><b>{k}</b>{v}</div>' for i,(k,v,c) in enumerate(items))
    return f'''<span class="tag a" style="background:var(--desk);color:var(--ink);align-self:center">Samengevat</span>
<div class="recap">{cells}</div>'''

# ---------- PILEA ----------

PL_LEAF = f'<g id="pl"><circle r="24" fill="#5DBB72" stroke="#1E7A3C" stroke-width="3.5"/><path d="M0 0V-19M0 0l17-9M0 0l13 14M0 0l-13 14M0 0l-17-9" stroke="#1E7A3C" stroke-width="2.2" stroke-linecap="round"/><circle r="3" fill="#1E7A3C"/></g>'

def pilea_plant(stand=True, babies=False, cut=False):
    leaves = [(55,150,.9),(95,85,1),(150,48,1.1),(210,92,1),(248,150,.9),(110,150,.85),(190,150,.85),(150,190,.8)]
    out = ''
    for i,(lx,ly,s) in enumerate(leaves):
        out += f'<g class="grow" style="animation-delay:{.15+i*.12:.2f}s"><path d="M150 228Q{(150+lx)/2:.0f} {ly+70} {lx} {ly}" stroke="#1E7A3C" stroke-width="5" fill="none"/><use href="#pl" transform="translate({lx} {ly}) scale({s})"/></g>'
    pot = f'<path d="M108 222h84l-8 60h-68Z" fill="#FFE24A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/><path d="M102 214h96v12h-96Z" fill="#FFE24A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    legs = f'<path d="M110 282h80v8h-80Z" fill="#B5654A" stroke="{INK}" stroke-width="4"/><path d="M116 290l-4 30M184 290l4 30M150 290v26" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><path d="M116 290l-4 30M184 290l4 30M150 290v26" stroke="#B5654A" stroke-width="5" stroke-linecap="round"/>' if stand else ''
    return f'<ellipse cx="170" cy="324" rx="80" ry="9" fill="{INK}" opacity=".3"/>{legs}{out}{pot}'

def build_pilea():
    defs = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{PL_LEAF}</defs></svg>'
    baby = lambda x,y,s,cls,st='': f'<g class="{cls}" style="{st}"><g transform="translate({x} {y}) scale({s})"><path d="M0 0v-18" stroke="#1E7A3C" stroke-width="4"/><use href="#pl" transform="translate(-9 -22) scale(.45)"/><use href="#pl" transform="translate(9 -26) scale(.5)"/></g></g>'
    scenes = [
      dict(dur=5200, bg='#2E9E4F', dark=True, html=f'''{defs}<span class="tag a">Plantenfiche</span>
<svg class="art" viewBox="0 0 300 335" aria-hidden="true" style="width:80cqw">{pilea_plant()}</svg>
<div class="col"><h2 class="a d3" style="font-size:12cqw">Pilea peperomioides</h2><p class="note a d4" style="font-size:10cqw;color:var(--pot)">de pannenkoekenplant</p></div>'''),
      dict(dur=4800, bg='#F4EEFF', html=f'''<span class="tag a">Verzorging</span>
<svg class="art" viewBox="0 0 300 260" aria-hidden="true"><use href="#pl" transform="translate(150 130) scale(4.2)"/>{dust_wipe()}</svg>
<div class="col"><h2 class="a d2" style="font-size:15cqw">Afstoffen</h2></div>'''),
      dict(dur=6200, bg='#DDF4F3', html=f'''<span class="tag a">Water</span>
<svg class="art" viewBox="44 4 212 104" aria-hidden="true">
{drop(150,10,3.2,'flash','#7FC8E8')}
{drop(70,40,1,'drop','#0F8A8F')}{drop(230,30,1,'drop','#0F8A8F','animation-delay:.6s')}</svg>
<div class="col" style="color:var(--teal)">
<span class="chip a d1">1x / week</span>
<div class="cal a d2" style="grid-template-columns:repeat(7,1fr)"><span><b>ma</b></span><span><b>di</b></span><span class="w"><b>wo</b></span><span><b>do</b></span><span><b>vr</b></span><span><b>za</b></span><span><b>zo</b></span></div>
<h2 class="a d3" style="color:var(--ink);font-size:10cqw">≋ licht vochtig</h2>
<p class="note a d4" style="color:var(--blue)">in kleine hoeveelheden</p></div>'''),
      dict(dur=5600, bg='#FFE7E9', html=f'''<span class="tag a">Let op</span>
<svg class="art" viewBox="0 0 300 236" aria-hidden="true">
<g class="flash"><path d="M150 4L192 80H108Z" fill="#FFD60A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M150 30v24" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="67" r="4.5" fill="{INK}"/></g>
<g transform="translate(70 120)"><rect x="-38" y="0" width="76" height="60" rx="6" fill="#E8C9A0" stroke="{INK}" stroke-width="5"/><path d="M-26 20l10 6M-6 14l8 8M14 24l12-4M-20 42l14-2M10 44l12 4" stroke="#9B7A4E" stroke-width="3" stroke-linecap="round"/>
<path class="tick" style="--cd:1.6s" d="M-22 30l14 14 30-34" stroke="#1E7A3C" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(230 120)"><rect x="-38" y="0" width="76" height="60" rx="6" fill="#4A3424" stroke="{INK}" stroke-width="5"/><path d="M-30 10h60" stroke="#2F6FD6" stroke-width="7"/>
<path class="cross" style="--cd:2.2s" d="M-24 8l48 46M24 8l-48 46" stroke="#D8263A" stroke-width="9" stroke-linecap="round"/></g>
<text x="70" y="226" text-anchor="middle" style="font:700 30px var(--hand)">te droog</text><text x="230" y="226" text-anchor="middle" style="font:700 30px var(--hand)">te nat</text></svg>
<div class="col"><h2 class="a d2" style="font-size:13cqw">Beter te droog</h2><p class="note a d4" style="font-size:10cqw;color:var(--red)">dan te nat!</p></div>'''),
      dict(dur=5200, bg='#FFF6C2', html=light_scene('<p class="note a d5" style="font-size:9cqw">maar wel véél</p>', extra='<g class="glow"><circle cx="150" cy="120" r="112" fill="none" stroke="#F5C400" stroke-width="6" stroke-dasharray="4 14"/></g>')),
      dict(dur=7400, bg='#E6F6E3', html=f'''<span class="tag a">Stekken</span>
<svg class="art" viewBox="0 0 300 260" aria-hidden="true">
<g transform="translate(-20 -10) scale(.8)">{pilea_plant(stand=False)}</g>
{baby(88,205,1.1,'a d2')}{baby(162,206,1,'a d3')}
<g class="a d5"><path d="M190 150l50-22" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><path d="M240 128l22-10 4 8-22 10Z" fill="#cfd8dc" stroke="{INK}" stroke-width="3"/></g>
<g class="a d6"><path d="M228 200h50l-6 34h-38Z" fill="#B5654A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>{baby(253,200,1.3,'grow','animation-delay:3s')}</g></svg>
<div class="col"><h2 class="a d1" style="font-size:10cqw">Stekken via<br>baby'tjes</h2><p class="note a d4" style="color:var(--leaf)">lossnijden</p></div>'''),
      dict(dur=6500, bg=INK, dark=True, html=f'''{recap([('Blad','afstoffen','var(--leaf-lt)'),('Water','1x/week, kleine beetjes','#8FD3D5'),('Grond','licht vochtig, beter te droog','#E8C9A0'),('Licht','indirect, maar wel veel','var(--sun)'),('Stekken',"baby'tjes lossnijden",'#CDB4F5'),('Bijnaam','pannenkoekenplant','#F59AA5')])}
<p class="note a d6" style="color:var(--desk);font-size:9cqw">Pilea peperomioides</p>'''),
    ]
    page('pannenkoekenplant', 'Pannenkoekenplant in een minuutje',
         'Geanimeerde explainer over de pannenkoekenplant (Pilea peperomioides), gemaakt op basis van een handgetekende plantenfiche.', scenes)

# ---------- SANSEVIERIA ----------

def sword(h):
    w = h*0.11
    leaf = f'M0 0C{-w:.1f} {-h*.25:.1f} {-w*.8:.1f} {-h*.7:.1f} 0 {-h}C{w*.8:.1f} {-h*.7:.1f} {w:.1f} {-h*.25:.1f} 0 0Z'
    bands = ''
    y = 14
    while y < h*0.85:
        f = 1 - y/h
        hw = w*0.75*(0.55+0.45*min(1, f*1.4))
        bands += f'M{-hw:.1f} {-y:.1f}q{hw:.1f} -5 {hw*2:.1f} 0'
        y += 15
    return leaf, bands

def sans_leaf(x, y, h, rot, delay):
    leaf, bands = sword(h)
    return f'<g class="rise" style="animation-delay:{delay:.2f}s"><g transform="translate({x} {y}) rotate({rot})"><path d="{leaf}" fill="#3FAE5A" stroke="#E8C21A" stroke-width="6" stroke-linejoin="round"/><path d="{leaf}" fill="none" stroke="#1E7A3C" stroke-width="2"/><path d="{bands}" stroke="#1E7A3C" stroke-width="3" fill="none" stroke-linecap="round"/></g></g>'

def sans_plant():
    ls = [(-34,170,-16),(-18,220,-7),(0,250,2),(18,205,9),(34,165,17),(-8,150,-2),(12,140,5)]
    leaves = ''.join(sans_leaf(150+dx, 238, h, r, .15+i*.13) for i,(dx,h,r) in enumerate(ls))
    return f'''<ellipse cx="170" cy="330" rx="74" ry="9" fill="{INK}" opacity=".3"/>{leaves}
<path d="M92 232h116l-14 92h-88Z" fill="#FFE24A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
<ellipse cx="150" cy="234" rx="58" ry="10" fill="#A65E4A" stroke="{INK}" stroke-width="5"/>'''

def build_sans():
    cal = ''.join(f'<span class="{"w" if i==3 else ""}"><b>W{i+1}</b></span>' for i in range(4))
    scenes = [
      dict(dur=5200, bg='#2E9E4F', dark=True, html=f'''<span class="tag a">Plantenfiche</span>
<svg class="art" viewBox="0 0 300 340" aria-hidden="true" style="width:74cqw">{sans_plant()}</svg>
<div class="col"><h2 class="a d3" style="font-size:14cqw">Sansevieria</h2><p class="note a d4" style="font-size:10cqw;color:var(--pot)">de vrouwentong</p></div>'''),
      dict(dur=4800, bg='#F4EEFF', html=f'''<span class="tag a">Verzorging</span>
<svg class="art" viewBox="0 0 300 260" aria-hidden="true">{sans_leaf(150,262,250,8,0)}{dust_wipe()}</svg>
<h2 class="a d2" style="font-size:15cqw">Afstoffen</h2>'''),
      dict(dur=6000, bg='#E3ECFF', html=f'''<span class="tag a">Water</span>
<svg class="art" viewBox="96 0 108 124" aria-hidden="true">{drop(150,10,4,'flash','#7FC8E8')}</svg>
<div class="col" style="color:var(--blue)">
<h2 class="a d1" style="color:var(--ink)">Zeer weinig</h2>
<div class="cal a d2" style="grid-template-columns:repeat(4,1fr)">{cal}</div>
<span class="chip a d3">1x / 4 weken</span></div>'''),
      dict(dur=6200, bg='#FFF6C2', html=light_scene('<p class="note a d5" style="font-size:8.6cqw">van weinig tot veel</p>', half=True)),
      dict(dur=7000, bg='#E6F6E3', html=f'''<span class="tag a">Vermeerderen</span>
<svg class="art" viewBox="0 0 300 290" aria-hidden="true">
<g class="a d1"><g transform="translate(-60 0) scale(.8)">{sans_leaf(110,250,180,-8,.2)}{sans_leaf(135,250,210,4,.3)}<path d="M80 245h90l-10 60h-70Z" fill="#FFE24A" stroke="{INK}" stroke-width="5"/></g>
<g transform="translate(15 0) scale(.8)">{sans_leaf(120,250,190,6,.4)}<path d="M85 245h70l-8 60h-54Z" fill="#FFE24A" stroke="{INK}" stroke-width="5"/></g>
<path class="cross" style="--cd:.8s;stroke-dasharray:6 8" d="M79 96v150" stroke="{INK}" stroke-width="4"/></g>
<g class="a d4"><g transform="translate(225 110)"><path d="M-30 0h60v110h-60Z" fill="#CFE9F7" stroke="{INK}" stroke-width="5"/><path d="M-30 40h60v70h-60Z" fill="#7FC8E8" opacity=".8"/>{sans_leaf(0,80,95,0,0)}<path d="M-6 82l-6 18M0 82v20M6 82l6 18" stroke="#fff" stroke-width="2.5"/></g></g>
<text x="72" y="284" text-anchor="middle" style="font:700 30px var(--hand)" class="a d3">scheuren</text>
<text x="225" y="284" text-anchor="middle" style="font:700 30px var(--hand)" class="a d5">bladstek</text></svg>
<h2 class="a d2" style="font-size:10cqw">Scheuren<br>of bladstek</h2>'''),
      dict(dur=8800, bg='#FFFDF6', html=f'''<span class="tag a">Luchtfilter</span>
<div class="col" style="gap:5cqw">
<div class="pair a d1"><svg viewBox="-60 -60 120 120">{ghs(0,0,1,FLAME)}</svg><div style="text-align:left"><b>Benzeen</b><svg viewBox="0 0 170 60" style="width:44cqw;height:auto">{benzene(30,30)}<text x="74" y="40" class="mol">C₆H₆</text></svg></div></div>
<div class="pair a d3"><svg viewBox="-60 -60 120 120">{ghs(0,0,1,'<rect x="-30" y="-30" width="60" height="60" fill="#d6d6d6" transform="rotate(45)"/>'+SKULL)}</svg><div style="text-align:left"><b>Formaldehyde</b><svg viewBox="-60 -64 200 110" style="width:34cqw;height:auto">{formaldehyde(0,0)}</svg></div></div>
<div class="need a d5">6 à 8 planten nodig<small>goed verspreid</small></div></div>'''),
      dict(dur=6500, bg=INK, dark=True, html=f'''{recap([('Blad','afstoffen','var(--leaf-lt)'),('Water','zeer weinig, 1x per 4 weken','#AFC7F5'),('Licht','weinig tot veel indirect','var(--sun)'),('Vermeerderen','scheuren of bladstek','#CDB4F5'),('Lucht','benzeen, formaldehyde','#F59AA5'),('Aantal','6 à 8, goed verspreid','#FFE24A')])}
<p class="note a d6" style="color:var(--desk);font-size:9cqw">Sansevieria · vrouwentong</p>'''),
    ]
    page('vrouwentong', 'Vrouwentong in een minuutje',
         'Geanimeerde explainer over de vrouwentong (Sansevieria), gemaakt op basis van een handgetekende plantenfiche.', scenes)

# ---------- CHLOROPHYTUM ----------

def blade(x, y, dx, h, delay, w=8):
    return f'<g class="grow" style="animation-delay:{delay:.2f}s"><path d="M{x} {y}Q{x+dx*.35:.0f} {y-h} {x+dx} {y-h*.45:.0f}" stroke="#1E7A3C" stroke-width="{w+4}" fill="none" stroke-linecap="round"/><path d="M{x} {y}Q{x+dx*.35:.0f} {y-h} {x+dx} {y-h*.45:.0f}" stroke="#5DBB72" stroke-width="{w}" fill="none" stroke-linecap="round"/></g>'

def rosette(x, y, s, cls='', style=''):
    bl = ''.join(f'<path d="M0 0Q{dx*.4:.0f} {-h} {dx} {-h*.4:.0f}" stroke="#1E7A3C" stroke-width="5" fill="none" stroke-linecap="round"/>' for dx,h in [(-30,26),(-16,36),(0,40),(16,36),(30,26),(-24,14),(24,14)])
    return f'<g class="{cls}" style="{style}"><g transform="translate({x} {y}) scale({s})">{bl}</g></g>'

def chloro_plant(runner=True):
    bl = [(-90,150),(-60,190),(-30,210),(0,220),(30,205),(60,185),(90,150),(-110,110),(110,115),(-15,180),(15,170)]
    blades = ''.join(blade(150+(i%3-1)*6, 220, dx, h, .1+i*.08) for i,(dx,h) in enumerate(bl))
    run = f'<g class="grow" style="animation-delay:1.2s"><path d="M160 210Q250 150 262 238" stroke="#1E7A3C" stroke-width="3" fill="none"/>{rosette(262,248,.9)}</g>' if runner else ''
    return f'''<ellipse cx="160" cy="318" rx="70" ry="9" fill="{INK}" opacity=".3"/>{blades}{run}
<path d="M98 216h104l-12 96h-80Z" fill="#FFC21A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
<path d="M92 208h116v12H92Z" fill="#FFC21A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'''

def build_chloro():
    scenes = [
      dict(dur=5600, bg='#2E9E4F', dark=True, html=f'''<span class="tag a">Plantenfiche</span>
<svg class="art" viewBox="0 0 300 330" aria-hidden="true" style="width:80cqw">{chloro_plant()}</svg>
<div class="col"><h2 class="a d3" style="font-size:11.5cqw">Chlorophytum comosum</h2><p class="note a d4" style="font-size:9.4cqw;color:var(--pot)">graslelie <span style="opacity:.8">(spinnenplant)</span></p></div>'''),
      dict(dur=6800, bg='#E3ECFF', html=f'''<span class="tag a">Water</span>
<svg class="art" viewBox="0 0 300 200" aria-hidden="true" style="width:74cqw">
{spray(190,60,.8)}
<g class="a d2">{drop(40,40,1.6,'flash','#2F6FD6')}{drop(80,30,1.6,'flash','#2F6FD6')}{drop(120,40,1.6,'flash','#2F6FD6')}</g>
<g class="a d4"><g transform="translate(80 120)"><rect x="-60" y="0" width="120" height="44" rx="8" fill="#4A3424" stroke="{INK}" stroke-width="5"></rect>
<path d="M-40 22h18M0 14h22M30 30h16" stroke="#C9A77A" stroke-width="4" stroke-linecap="round" class="a d6"/></g></g></svg>
<div class="col"><h2 class="a d1" style="font-size:14cqw;color:var(--blue)">Ruim</h2><p class="note a d5" style="font-size:9cqw">en laat uitdrogen</p></div>'''),
      dict(dur=6000, bg='#FFF6C2', html=f'''<span class="tag a">Licht</span>
<svg class="art" viewBox="0 0 300 200" aria-hidden="true" style="width:78cqw">{sun(80,100,40)}<g class="a d3">{sun(220,100,40,True,18)}</g></svg>
<div class="col"><h2><span class="in">in</span><span class="dir">direct</span><br>zonlicht</h2><p class="note a d5" style="font-size:9cqw">veel of weinig</p></div>'''),
      dict(dur=7200, bg='#E6F6E3', html=f'''<span class="tag a">Stekken</span>
<svg class="art" viewBox="0 0 300 300" aria-hidden="true">
<g transform="translate(-40 0) scale(.85)">{chloro_plant(runner=False)}</g>
<path class="tick" style="--cd:.6s;stroke-dasharray:400;stroke-dashoffset:400" d="M100 190Q200 110 222 196" stroke="#1E7A3C" stroke-width="3.5" fill="none"/>
{rosette(222,206,1.1,'a d3')}
<g class="a d5"><path d="M206 212l-4 14M222 214v16M238 212l4 14" stroke="#C9A77A" stroke-width="3" stroke-linecap="round"/></g>
<g class="a d6"><path d="M196 236h52l-6 40h-40Z" fill="#B5654A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g></svg>
<h2 class="a d2" style="font-size:13cqw">Stekken</h2>'''),
      dict(dur=7000, bg='#FFFDF6', html=f'''<span class="tag a">Luchtfilter</span>
<svg class="art" viewBox="-70 -70 140 140" aria-hidden="true" style="width:44cqw"><g class="a d1">{ghs(0,0,1.05,SKULL)}</g></svg>
<div class="col"><h2 class="a d2" style="color:var(--red);font-size:11cqw">Formaldehyde</h2>
<svg class="a d3" viewBox="-60 -64 120 110" style="width:30cqw;height:auto" aria-hidden="true">{formaldehyde(0,0)}</svg>
<div class="need a d5">4 à 6 planten nodig</div></div>'''),
      dict(dur=6200, bg=INK, dark=True, html=f'''{recap([('Water','ruim, dan laten uitdrogen','#AFC7F5'),('Verstuiver','blad besproeien','#8FD3D5'),('Licht','indirect, veel of weinig','var(--sun)'),('Stekken','via de uitlopers','var(--leaf-lt)'),('Lucht','formaldehyde','#F59AA5'),('Aantal','4 à 6 planten','#FFE24A')])}
<p class="note a d6" style="color:var(--desk);font-size:9cqw">graslelie · spinnenplant</p>'''),
    ]
    page('graslelie', 'Graslelie in een minuutje',
         'Geanimeerde explainer over de graslelie of spinnenplant (Chlorophytum comosum), gemaakt op basis van een handgetekende plantenfiche.', scenes)

build_pilea(); build_sans(); build_chloro()
# ---------- OVERZICHT ----------

FI_LEAF = f'<g id="fl"><path d="M0 0C-38-18-40-70 0-100C40-70 38-18 0 0Z" fill="#8ED19B" stroke="{INK}" stroke-width="4"/><path d="M0-4V-92" stroke="#2E9E4F" stroke-width="3.5"/></g>'

def ficus_plant():
    ls = [(250,-62,.9),(240,58,.9),(190,-55,.85),(160,52,.85),(115,-40,.75),(95,35,.7),(50,-6,.55)]
    leaves = ''.join(f'<use href="#fl" transform="translate(150 {y}) rotate({r}) scale({sc})"/>' for y,r,sc in ls)
    return (f'<ellipse cx="150" cy="318" rx="80" ry="10" fill="{INK}" opacity=".3"/><path d="M150 300V40" stroke="{INK}" stroke-width="5"/>{leaves}'
            f'<path d="M95 240h110l-14 70H109Z" fill="#FFE24A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M88 232h124v14H88Z" fill="#FFE24A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')

# Elke nieuwe plant: een blok hier. Alles komt van de fiche.
# spot: waar de plant in de huiskamer staat (x, y = midden onderaan de pot, s = schaal)
# tag: waar het naamkaartje hangt (x, y linksboven) en wat erop staat (woorden van de fiche)
PLANTS = [
  dict(slug='rubberboom', name='Rubberboom', sci='Ficus elastica', tint='#BFE6C6', art=ficus_plant, vb='30 -10 240 345',
       licht_txt='indirect', water_txt='1x / week', lucht=True, toxic=True,
       spot=(705, 640, .78), tagtxt='indirect, uit de tocht', ghosts=[]),
  dict(slug='pannenkoekenplant', name='Pannenkoeken­plant', sci='Pilea peperomioides', tint='#CFEFF0', art=lambda: pilea_plant(), vb='10 15 280 320',
       licht_txt='indirect, veel', water_txt='1x / week', lucht=False, toxic=False,
       spot=(530, 404, .42), tagtxt='indirect, maar wel veel', ghosts=[]),
  dict(slug='vrouwentong', name='Vrouwentong', sci='Sansevieria', tint='#FFF1A8', art=sans_plant, vb='40 -20 220 360',
       licht_txt='weinig tot veel', water_txt='1x / 4 weken', lucht=True, toxic=False,
       spot=(1128, 650, .62), tagtxt='weinig tot veel licht', ghosts=[(478, 652, .5, False)]),
  dict(slug='graslelie', name='Graslelie', sci='Chlorophytum comosum', tint='#DCE6FF', art=lambda: chloro_plant(), vb='20 20 280 310',
       licht_txt='veel of weinig', water_txt='ruim', lucht=True, toxic=False,
       spot=(955, 262, .5), tagtxt='veel of weinig licht', hang=True, ghosts=[(1122, 236, .4, True)]),
]

ICON = {
  'licht': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="5" fill="#F5C400" stroke="#141414" stroke-width="2"/><path d="M12 1.5v3M12 19.5v3M1.5 12h3M19.5 12h3M4.6 4.6l2.1 2.1M17.3 17.3l2.1 2.1M4.6 19.4l2.1-2.1M17.3 6.7l2.1-2.1" stroke="#141414" stroke-width="2" stroke-linecap="round"/></svg>',
  'water': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5C7 9.5 5.5 12.5 5.5 15.3a6.5 6.5 0 0 0 13 0c0-2.8-1.5-5.8-6.5-12.8Z" fill="#7FC8E8" stroke="#141414" stroke-width="2" stroke-linejoin="round"/></svg>',
  'lucht': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h11a3 3 0 1 0-3-3M3 12h16a3 3 0 1 1-3 3M3 16h8" fill="none" stroke="#141414" stroke-width="2.2" stroke-linecap="round"/></svg>',
}

def room_svg(links):
    I = INK
    planks = ''.join(f'<path d="M0 {y}H1200" stroke="#B9814F" stroke-width="3"/>' for y in (600, 645))
    planks += ''.join(f'<path d="M{x} {y1}v{45}" stroke="#B9814F" stroke-width="3"/>' for x, y1 in [(140,560),(420,560),(760,560),(1010,560),(260,600),(600,600),(900,600),(80,645),(470,645),(830,645),(1110,645)])
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="#F0DFA8"/>' for y in range(40, 540, 60) for x in range(30 + (y // 60 % 2) * 30, 1200, 60))
    base = f'''<rect width="1200" height="700" fill="#FFF8E1"/>{dots}
<path d="M1040 0H1200V560H1040Z" fill="{I}" opacity=".13"/>
<path d="M1040 0V560" stroke="{I}" stroke-width="2" stroke-dasharray="6 10" opacity=".35"/>
<rect y="560" width="1200" height="140" fill="#E2B07A"/>{planks}
<path d="M1040 560L1200 560V700H980Z" fill="{I}" opacity=".13"/>
<path d="M0 560H1200" stroke="{I}" stroke-width="6"/>
<!-- raam met vitrage -->
<path d="M300 418H600L690 700H400Z" fill="#FFE24A" opacity=".45"/>
<rect x="306" y="96" width="288" height="304" fill="#BFE3FF" stroke="{I}" stroke-width="7"/>
<circle cx="540" cy="150" r="34" fill="#F5C400" stroke="{I}" stroke-width="5"/>
<path d="M450 96V400M306 248H594" stroke="{I}" stroke-width="6"/>
<g opacity=".55">{''.join(f'<path d="M{x} 100V396" stroke="#fff" stroke-width="9"/>' for x in range(318, 594, 22))}</g>
<path d="M292 400H608V418H292Z" fill="#fff" stroke="{I}" stroke-width="5"/>
<path d="M282 82H618" stroke="{I}" stroke-width="7" stroke-linecap="round"/>
<path d="M286 86c18 120-8 230 12 330h-30c-10-110 8-220 2-330Z" fill="#F59AA5" stroke="{I}" stroke-width="5" stroke-linejoin="round"/>
<path d="M614 86c-18 120 8 230-12 330h30c10-110-8-220-2-330Z" fill="#F59AA5" stroke="{I}" stroke-width="5" stroke-linejoin="round"/>
<!-- deur met tocht -->
<rect x="52" y="172" width="150" height="388" fill="#C98B5E" stroke="{I}" stroke-width="7"/>
<rect x="76" y="200" width="102" height="140" rx="6" fill="none" stroke="{I}" stroke-width="4"/>
<rect x="76" y="370" width="102" height="160" rx="6" fill="none" stroke="{I}" stroke-width="4"/>
<circle cx="184" cy="372" r="8" fill="#F5C400" stroke="{I}" stroke-width="4"/>
<g stroke="#2F6FD6" stroke-width="6" fill="none" stroke-linecap="round">
<path class="gust" d="M210 470q40-14 80 0t70-6"/><path class="gust" d="M210 505q46-10 92 0t76 4"/><path class="gust" d="M210 540q40 8 80 0t66 8"/></g>
<text x="232" y="452" class="lbl" fill="#2F6FD6">tocht</text>
<!-- zetel -->
<path d="M760 452h300v108H760Z" fill="#7FA4E6" stroke="{I}" stroke-width="6" stroke-linejoin="round"/>
<path d="M776 400h268v60H776Z" fill="#9BB9EE" stroke="{I}" stroke-width="6" stroke-linejoin="round"/>
<path d="M742 430h44v130h-44ZM1034 430h44v130h-44Z" fill="#7FA4E6" stroke="{I}" stroke-width="6" stroke-linejoin="round"/>
<path d="M770 560v22M1050 560v22" stroke="{I}" stroke-width="8" stroke-linecap="round"/>
<!-- donkere hoek -->
<text x="1050" y="46" class="lbl" fill="{I}" opacity=".7" style="font-size:28px">donkere hoek</text>
<text x="548" y="606" class="lbl" fill="#9A7400">licht</text>
<!-- vrij plekje op de vensterbank -->
<g class="free"><path d="M352 404h44l-6 -30h-32Z" fill="none" stroke="{I}" stroke-width="4" stroke-dasharray="6 6" stroke-linejoin="round"/>
<text x="374" y="368" text-anchor="middle" class="lbl" style="font-size:30px">?</text></g>'''
    def one(pl, x, y, s, hang, ghost, href, plain):
        h = ''
        if hang:
            top = y - 330 * s
            h = f'<path d="M{x} 0V{top:.0f}M{x} {top:.0f}L{x-48*s:.0f} {y-150*s:.0f}M{x} {top:.0f}L{x+48*s:.0f} {y-150*s:.0f}" stroke="{I}" stroke-width="3" fill="none"/>'
        cls = 'pl ghost' if ghost else 'pl'
        label = f'{plain}: {pl["tagtxt"]}' + ('. Kan ook hier staan' if ghost else '') + '. Bekijk de reel.'
        tip = f'{plain}' + (' (kan ook hier)' if ghost else '')
        return (f'<a class="{cls}" href="{href}" aria-label="{label}"><title>{tip}</title>{h}'
                f'<rect class="hit" x="{x-125*s:.0f}" y="{y-335*s:.0f}" width="{250*s:.0f}" height="{335*s:.0f}"/>'
                f'<g class="lift"><g transform="translate({x-150*s:.1f} {y-325*s:.1f}) scale({s})">{pl["art"]()}</g></g></a>')
    ghosts, plants = '', ''
    for pl in PLANTS:
        href = links.get(pl['slug'], pl['slug'] + '/')
        plain = pl['name'].replace('\u00ad', '')
        x, y, s = pl['spot']
        plants += one(pl, x, y, s, pl.get('hang'), False, href, plain)
        for gx, gy, gs, gh in pl.get('ghosts', []):
            ghosts += one(pl, gx, gy, gs, gh, True, href, plain)
    plants = ghosts + plants
    return f'<svg class="room" viewBox="0 0 1200 700" role="group" aria-label="Huiskamer met de planten op hun plek">{base}{plants}</svg>'

OV_CSS = r"""
:root{--desk:#FFD60A;--ink:#141414;--paper:#FFFDF6;--leaf:#2E9E4F;--red:#D8263A;--purple:#5B2A9E;
--display:"Bricolage Grotesque",system-ui,sans-serif;--hand:"Caveat","Comic Sans MS",cursive;color-scheme:light}
body{margin:0;background:var(--desk);color:var(--ink);font-family:var(--display)}
[hidden]{display:none!important}
.wrap{max-width:1120px;margin:0 auto;padding-inline:16px;padding-block:32px 56px}
h1{font:800 clamp(48px,11vw,104px)/.88 var(--display);letter-spacing:-.04em;margin:0;text-wrap:balance}
.hand{font:700 clamp(26px,5.4vw,36px)/1 var(--hand);margin:8px 0 20px}
.roomwrap{border:3px solid var(--ink);border-radius:22px;box-shadow:8px 8px 0 var(--ink);overflow-x:auto;overflow-y:hidden;background:#FFF8E1;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
svg.room{display:block;height:clamp(380px,68vh,600px);width:auto;max-width:none}
@media (min-width:900px){svg.room{width:100%;height:auto}}
.mini{position:relative;width:max-content;margin:14px auto 4px;border:3px solid var(--ink);border-radius:10px;overflow:hidden;background:#FFF8E1;cursor:pointer;touch-action:none}
.mini .minisvg{display:block;height:72px;width:auto}
.mini .minisvg .gust{animation:none;stroke-dashoffset:0}
.mini .vp{position:absolute;top:0;bottom:0;left:0;border:3px solid var(--ink);border-radius:6px;background:rgba(255,214,10,.28);box-sizing:border-box}
.mini .hand{position:absolute;width:30px;height:33px;left:50%;bottom:-6px;margin-left:-15px;animation:nudge 1.4s ease-in-out infinite}
.mini.moved .hand{opacity:0;transition:opacity .4s;animation:none}
@keyframes nudge{0%,100%{transform:translateX(-12px) rotate(-8deg)}50%{transform:translateX(12px) rotate(8deg)}}
.mini.off{display:none}
svg.room .lbl{font:700 34px var(--hand)}
svg.room .gust{stroke-dasharray:120;stroke-dashoffset:120;animation:gust 1.6s ease-out infinite}
svg.room .gust:nth-of-type(2){animation-delay:.5s}svg.room .gust:nth-of-type(3){animation-delay:1s}
@keyframes gust{0%{stroke-dashoffset:120;opacity:1}100%{stroke-dashoffset:-120;opacity:0}}
.pl{cursor:pointer;outline:none}
.pl .lift{transition:transform .25s}
.pl:hover .lift,.pl:focus-visible .lift{transform:translateY(-8px)}
.pl .hit{fill:transparent}
.pl.ghost .lift{opacity:.38;filter:grayscale(1)}
.pl.ghost path[stroke]{opacity:.5}
.pl.ghost:hover .lift,.pl.ghost:focus-visible .lift{opacity:.85;filter:none}
.pl:focus-visible .lift{filter:drop-shadow(0 0 0 transparent) drop-shadow(0 0 6px #5B2A9E)}
.legend{display:flex;flex-wrap:wrap;gap:6px 22px;font:700 24px/1.1 var(--hand);margin:12px 0 0}
.legend span{display:flex;align-items:center;gap:8px}
.legend i{display:inline-block;width:26px;height:26px;border-radius:50%;background:#5DBB72;border:3px solid var(--ink)}
.legend i.g{opacity:.38;filter:grayscale(1)}
h2.all{font:800 clamp(28px,6vw,44px)/1 var(--display);letter-spacing:-.03em;margin:44px 0 16px}
.mosaic{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));grid-auto-rows:200px;grid-auto-flow:dense;gap:16px}
.tile{container-type:inline-size;position:relative;display:flex;flex-direction:column;text-decoration:none;color:var(--ink);border:3px solid var(--ink);border-radius:18px;box-shadow:5px 5px 0 var(--ink);overflow:hidden;transition:transform .2s,box-shadow .2s;min-width:0}
.tile:hover{transform:translate(-2px,-3px);box-shadow:8px 9px 0 var(--ink)}
.tile:focus-visible{outline:3px solid var(--purple);outline-offset:3px}
.tile.big{grid-column:span 2;grid-row:span 2}.tile.tall{grid-row:span 2}.tile.wide{grid-column:span 2}
.tile svg.plant{flex:1;min-height:0;width:100%;padding:8px;box-sizing:border-box}
.label{background:var(--paper);border-top:3px solid var(--ink);padding:8px 12px 10px;display:flex;flex-direction:column;gap:3px}
.sci{font:700 19px/1 var(--hand);color:var(--leaf);overflow-wrap:break-word}
.name{font:800 clamp(14px,10.5cqi,20px)/1.05 var(--display);letter-spacing:-.02em;margin:0;overflow-wrap:normal;hyphens:manual}
.big .name{font-size:clamp(22px,9cqi,30px)}.big .sci{font-size:25px}
.needs{list-style:none;margin:4px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:4px 10px}
.needs li{display:flex;align-items:center;gap:4px;font:700 19px/1 var(--hand)}
.needs svg{width:17px;height:17px;flex:none}
.big .needs li{font-size:23px}.big .needs svg{width:20px;height:20px}
.badge{position:absolute;top:10px;right:10px;font:800 10px var(--display);letter-spacing:.1em;text-transform:uppercase;background:var(--red);color:var(--paper);border-radius:99px;padding:4px 8px;z-index:1}
.play{position:absolute;top:10px;left:10px;width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--desk);display:grid;place-items:center;font-size:11px;z-index:1}
.soon{border:3px dashed var(--ink);border-radius:18px;display:grid;place-items:center;text-align:center;padding:14px;font:700 28px/1 var(--hand)}
.info{margin-top:48px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:24px 32px;align-items:center;background:var(--paper);border:3px solid var(--ink);border-radius:22px;box-shadow:8px 8px 0 var(--ink);padding:24px}
.info .nb{width:100%;height:auto}
.info h2{font:800 clamp(28px,5.5vw,40px)/1 var(--display);letter-spacing:-.03em;margin:0 0 14px}
.info ol{margin:0;padding:0;list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:12px}
.info li{counter-increment:s;display:grid;grid-template-columns:38px 1fr;gap:12px;font:500 16px/1.45 var(--display);max-width:60ch}
.info li::before{content:counter(s);width:34px;height:34px;border-radius:50%;background:var(--ink);color:var(--desk);display:grid;place-items:center;font:800 16px var(--display)}
.info li b{font-weight:800}
.info-note{font:700 23px/1.15 var(--hand);color:var(--leaf);margin:16px 0 0}
@media (max-width:720px){.info{grid-template-columns:1fr;padding:18px}.info .nb{max-width:360px;margin:0 auto}}
.foot{margin-top:40px;font:700 22px/1.2 var(--hand);max-width:52ch}
@media (max-width:520px){.mosaic{grid-auto-rows:215px}}
@media (max-width:360px){.mosaic{grid-template-columns:1fr}.tile.big,.tile.wide{grid-column:span 1}}
@media (prefers-reduced-motion:reduce){.tile,.pl .lift{transition:none}svg.room .gust{animation:none;stroke-dashoffset:0}.mini .hand{animation:none}}
"""

OV_JS = r"""
(function(){
 // start de kamer op gsm bij het raam, zodat je meteen planten ziet
 const w=document.querySelector('.roomwrap'),mini=document.getElementById('mini'),vp=document.getElementById('vp');
 let start=0;
 function sync(){
  const over=w.scrollWidth>w.clientWidth+2;mini.classList.toggle('off',!over);if(!over)return;
  const mw=mini.clientWidth;vp.style.width=(w.clientWidth/w.scrollWidth*mw)+'px';vp.style.left=(w.scrollLeft/w.scrollWidth*mw)+'px';
 }
 try{ if(w.scrollWidth>w.clientWidth) w.scrollLeft=(w.scrollWidth-w.clientWidth)*0.28; }catch(e){}
 start=w.scrollLeft;sync();
 w.addEventListener('scroll',()=>{sync();if(Math.abs(w.scrollLeft-start)>20)mini.classList.add('moved')},{passive:true});
 window.addEventListener('resize',sync);
 function jump(e){const r=mini.getBoundingClientRect();const f=(e.clientX-r.left)/r.width;w.scrollLeft=f*w.scrollWidth-w.clientWidth/2;mini.classList.add('moved')}
 let drag=false;
 mini.addEventListener('pointerdown',e=>{drag=true;mini.setPointerCapture(e.pointerId);jump(e)});
 mini.addEventListener('pointermove',e=>{if(drag)jump(e)});
 mini.addEventListener('pointerup',()=>{drag=false});
})();
"""

ARTIFACT_LINKS = {'rubberboom':'https://claude.ai/artifact/Pe65DNa14PMjNJazRRsmVY','pannenkoekenplant':'https://claude.ai/artifact/Q1NQFtvBS527ePdVp2beuH','vrouwentong':'https://claude.ai/artifact/G4852WAcyFnP8FvMYAvd7M','graslelie':'https://claude.ai/artifact/5iLZijme21bXEyhVhve6cn'}

SIZES = ['big', 'tall', '', 'wide', '']

def build_overview():
    links = ARTIFACT_LINKS if ARTIFACT else {}
    tiles = ''
    for i, pl in enumerate(PLANTS):
        size = SIZES[i % len(SIZES)]
        href = links.get(pl['slug'], pl['slug'] + '/')
        plain = pl['name'].replace('­', '')
        needs = (f'<li>{ICON["licht"]}<span>{pl["licht_txt"]}</span></li>'
                 f'<li>{ICON["water"]}<span>{pl["water_txt"]}</span></li>'
                 + (f'<li>{ICON["lucht"]}<span>luchtfilter</span></li>' if pl['lucht'] else ''))
        badge = '<span class="badge">giftig sap</span>' if pl['toxic'] else ''
        tiles += (f'<a class="tile {size}" href="{href}" style="background:{pl["tint"]}" aria-label="{plain} ({pl["sci"]}). Bekijk de reel.">\n'
                  f'<span class="play" aria-hidden="true">&#9654;</span>{badge}'
                  f'<svg class="plant" viewBox="{pl["vb"]}" aria-hidden="true">{pl["art"]()}</svg>\n'
                  f'<span class="label"><span class="sci">{pl["sci"]}</span><span class="name">{pl["name"]}</span><ul class="needs">{needs}</ul></span></a>\n')
    tiles += '<div class="soon">nog meer planten<br>in het schriftje…</div>\n'
    import re as _re
    mini_svg = room_svg(links)
    mini_svg = _re.sub(r'<title>.*?</title>', '', mini_svg)
    mini_svg = _re.sub(r'<rect class="hit"[^>]*/>', '', mini_svg)
    mini_svg = _re.sub(r'<a class="([^"]*)"[^>]*>', r'<g class="\1">', mini_svg).replace('</a>', '</g>').replace('class="room"', 'class="minisvg"').replace(' role="group" aria-label="Huiskamer met de planten op hun plek"', ' focusable="false"')
    defs = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{PL_LEAF}{FI_LEAF}</defs></svg>'
    core = f'<title>Waar zet ik mijn plant?</title>\n{FONTS}\n<style>{OV_CSS}</style>\n'
    main = (f'{defs}<div class="wrap">\n'
            f'<h1>Waar zet ik mijn plant?</h1><p class="hand">klik op een plant voor haar fiche</p>\n'
            f'<div class="roomwrap">{room_svg(links)}</div>\n'
            f'<div class="mini" id="mini" aria-hidden="true">{mini_svg}<div class="vp" id="vp"><svg class="hand" viewBox="0 0 40 44" aria-hidden="true"><path d="M17 41c-5-3-9-9-10-13-1-3 2-5 4-3l4 4V8c0-3 5-3 5 0v11c0-3 5-3 5 0v2c0-3 5-3 5 0v2c0-3 5-3 5 0v7c0 5-2 8-5 11Z" fill="#FFFDF6" stroke="#141414" stroke-width="3" stroke-linejoin="round"/></svg></div></div>\n'
            f'<p class="legend"><span><i></i>een plant op haar plek</span><span><i class="g"></i>doorschijnend: kan hier ook staan</span></p>\n'
            f'<section class="info" aria-labelledby="info-t"><svg class="nb" viewBox="0 0 480 300" aria-hidden="true"><ellipse cx="210" cy="282" rx="190" ry="12" fill="#141414" opacity=".18"/><path d="M30 40l170 10v220L30 262Z" fill="#FFFDF6" stroke="#141414" stroke-width="5" stroke-linejoin="round"/><path d="M390 40l-170 10v220l170-8Z" fill="#FFFDF6" stroke="#141414" stroke-width="5" stroke-linejoin="round"/><path d="M200 50h20v220h-20Z" fill="#E8E2D0" stroke="#141414" stroke-width="4"/><path d="M372 40v226" stroke="#141414" stroke-width="7"/><text x="62" y="82" style="font:700 22px var(--hand)" fill="#141414">Pilea</text><g transform="translate(112 196)"><path d="M0 0V-46M0-20l-22-24M0-26l20-26" stroke="#1E7A3C" stroke-width="3" fill="none"/><circle cx="-24" cy="-48" r="13" fill="#5DBB72" stroke="#1E7A3C" stroke-width="3"/><circle cx="21" cy="-56" r="14" fill="#5DBB72" stroke="#1E7A3C" stroke-width="3"/><circle cx="0" cy="-56" r="11" fill="#5DBB72" stroke="#1E7A3C" stroke-width="3"/><path d="M-16 0h32l-4 22h-24Z" fill="#FFE24A" stroke="#141414" stroke-width="3"/></g><rect x="238" y="92" width="80" height="30" rx="6" fill="#CFE9F7" stroke="#2F6FD6" stroke-width="3"/><text x="248" y="114" style="font:700 19px var(--hand)" fill="#2F6FD6">1x/week</text><circle cx="250" cy="152" r="10" fill="#F5C400" stroke="#141414" stroke-width="2.5"/><path d="M268 154h70M240 186h96M240 212h80M240 238h60" stroke="#9AA" stroke-width="3" stroke-linecap="round"/><g transform="translate(270 196) rotate(-28)"><rect x="0" y="-9" width="150" height="18" fill="#2E9E4F" stroke="#141414" stroke-width="4"/><path d="M0 -9L-26 0 0 9Z" fill="#F2D3A8" stroke="#141414" stroke-width="4" stroke-linejoin="round"/><path d="M-26 0l9-3v6Z" fill="#2E9E4F"/></g><g transform="translate(300 232) rotate(-14)"><rect x="0" y="-9" width="140" height="18" fill="#F5C400" stroke="#141414" stroke-width="4"/><path d="M0 -9L-26 0 0 9Z" fill="#F2D3A8" stroke="#141414" stroke-width="4" stroke-linejoin="round"/><path d="M-26 0l9-3v6Z" fill="#F5C400"/></g><g transform="translate(300 266) rotate(-4)"><rect x="0" y="-9" width="120" height="18" fill="#D8263A" stroke="#141414" stroke-width="4"/><path d="M0 -9L-26 0 0 9Z" fill="#F2D3A8" stroke="#141414" stroke-width="4" stroke-linejoin="round"/><path d="M-26 0l9-3v6Z" fill="#D8263A"/></g></svg><div class="info-txt"><h2 id="info-t">Hoe dit gemaakt is</h2><ol><li><span><b>Getekend.</b> Elke plant krijgt een fiche in een schriftje, met kleurpotloden en stiften: verzorging, licht, water, stekken.</span></li><li><span><b>Gefotografeerd.</b> Een foto van die bladzijde is de enige bron.</span></li><li><span><b>Tot leven gebracht.</b> Met hulp van AI (Claude) wordt de foto een korte reel. De tekeningen mogen opgepimpt worden, de informatie niet: wat niet op de fiche staat, komt er niet in.</span></li></ol><p class="info-note">Ook de plek in de huiskamer volgt de fiche. Zegt die niets over licht, dan krijgt de plant geen plek die het wel suggereert.</p></div></section>\n'
            f'</div>\n<script>{OV_JS}</script>\n')
    if ARTIFACT:
        path = os.path.join(OUT, 'overzicht.html'); open(path, 'w').write(core + main)
    else:
        path = os.path.join(OUT, 'index.html')
        open(path, 'w').write('<!DOCTYPE html>\n<html lang="nl">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
            '<meta name="description" content="Welke plant past waar in je huiskamer? Geanimeerde plantenfiches, getekend in een schriftje.">\n'
            '<meta name="theme-color" content="#FFD60A">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
            '<meta name="apple-mobile-web-app-title" content="Plantplek">\n<link rel="manifest" href="manifest.webmanifest">\n'
            '<link rel="icon" href="icons/icon.svg" type="image/svg+xml">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
            + core + '</head>\n<body>\n' + main + '</body>\n</html>\n')
    print('geschreven', path)

build_overview()
