"""Bouwt de plantenreels (Pilea, Sansevieria, Chlorophytum) als losse HTML-pagina's.
Gebruik: python3 build.py <uitvoermap> [--artifact]
--artifact: zonder doctype/head-skelet en zonder terugknop (voor claude.ai-preview)."""
import sys, os, math

OUT = sys.argv[1]
ARTIFACT = '--artifact' in sys.argv
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
.sub{font:500 5.4cqw/1.25 var(--display);text-align:center;margin:0;text-wrap:balance}
.note{font:700 7.4cqw/1.05 var(--hand);text-align:center;margin:0}
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
.pair span{font:700 6.2cqw/1 var(--hand)}
/* recap */
.recap{display:grid;grid-template-columns:1fr 1fr;gap:2.5cqw;width:100%}
.recap div{border-radius:14px;padding:3cqw;font:700 6cqw/1.02 var(--hand);color:var(--ink);text-align:left}
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
.home{position:fixed;top:calc(10px + env(safe-area-inset-top,0px));left:12px;font:700 14px var(--display);color:var(--ink);text-decoration:none;background:var(--paper);border:2px solid var(--ink);border-radius:99px;padding:4px 12px;z-index:10}
.home:focus-visible{outline:3px solid var(--purple)}
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
  }
  function setPlay(p){playing=p;playBtn.textContent=p?'Pauze':'Speel';stage.querySelectorAll('.scene.on *').forEach(el=>el.style.animationPlayState=p?'running':'paused')}
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
  stage.addEventListener('click',()=>playBtn.click());
  document.getElementById('prev').addEventListener('click',()=>{show(idx-1);setPlay(true)});
  document.getElementById('next').addEventListener('click',()=>{show(idx+1);setPlay(true)});
  document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')document.getElementById('next').click();if(e.key==='ArrowLeft')document.getElementById('prev').click();if(e.key===' '){e.preventDefault();playBtn.click()}});
  show(0);requestAnimationFrame(tick);
})();
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Caveat:wght@600;700&display=swap">'


def page(slug, title, desc, scenes, extra_css=''):
    css = BASE_CSS.replace('__OFF__', '110' if ARTIFACT else '150')
    if not ARTIFACT:
        css += 'body{padding-top:52px}'
    body = ''.join(
        f'<section class="scene{" dk" if s.get("dark") else ""}" data-dur="{s["dur"]}" style="background:{s["bg"]}">{s["html"]}</section>\n'
        for s in scenes)
    core = f"""<title>{title}</title>
{FONTS}
<style>{css}{extra_css}</style>
"""
    main = f"""<div class="stage" id="stage" aria-live="polite">
<div class="bars" id="bars"></div>
{body}</div>
<div class="ctrl">
<button id="prev" type="button" aria-label="Vorige scène">◀</button>
<button id="play" type="button">Pauze</button>
<button id="next" type="button" aria-label="Volgende scène">▶</button>
</div>
<script>{JS}</script>
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
{core}</head>
<body>
<a class="home" href="../" aria-label="Terug naar Planten">&larr; Planten</a>
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
      dict(dur=5200, bg='#1E7A3C', dark=True, html=f'''{defs}<span class="tag a">Plantenfiche</span>
<svg class="art" viewBox="0 0 300 335" aria-hidden="true" style="width:80cqw">{pilea_plant()}</svg>
<div class="col"><h2 class="a d3" style="font-size:12cqw">Pilea peperomioides</h2><p class="note a d4" style="font-size:10cqw;color:var(--pot)">de pannenkoekenplant</p></div>'''),
      dict(dur=4800, bg='#F4EEFF', html=f'''<span class="tag a">Verzorging</span>
<svg class="art" viewBox="0 0 300 260" aria-hidden="true"><use href="#pl" transform="translate(150 130) scale(4.2)"/>{dust_wipe()}</svg>
<div class="col"><h2 class="a d2" style="font-size:15cqw">Afstoffen</h2></div>'''),
      dict(dur=6200, bg='#DDF4F3', html=f'''<span class="tag a">Water</span>
<svg class="art" viewBox="0 0 300 150" aria-hidden="true" style="width:70cqw">
{drop(150,10,3.2,'flash','#7FC8E8')}
{drop(70,40,1,'drop','#0F8A8F')}{drop(230,30,1,'drop','#0F8A8F','animation-delay:.6s')}</svg>
<div class="col" style="color:var(--teal)">
<span class="chip a d1">1x / week</span>
<div class="cal a d2" style="grid-template-columns:repeat(7,1fr)"><span><b>ma</b></span><span><b>di</b></span><span class="w"><b>wo</b></span><span><b>do</b></span><span><b>vr</b></span><span><b>za</b></span><span><b>zo</b></span></div>
<h2 class="a d3" style="color:var(--ink);font-size:10cqw">≋ licht vochtig</h2>
<p class="note a d4" style="color:var(--blue)">in kleine hoeveelheden</p></div>'''),
      dict(dur=5600, bg='#FFE7E9', html=f'''<span class="tag a">Let op</span>
<svg class="art" viewBox="0 0 300 200" aria-hidden="true">
<g class="flash"><path d="M150 14L196 96H104Z" fill="#FFD60A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M150 42v28" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="83" r="4.5" fill="{INK}"/></g>
<g transform="translate(70 120)"><rect x="-38" y="0" width="76" height="60" rx="6" fill="#E8C9A0" stroke="{INK}" stroke-width="5"/><path d="M-26 20l10 6M-6 14l8 8M14 24l12-4M-20 42l14-2M10 44l12 4" stroke="#9B7A4E" stroke-width="3" stroke-linecap="round"/>
<path class="tick" style="--cd:1.6s" d="M-22 30l14 14 30-34" stroke="#1E7A3C" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(230 120)"><rect x="-38" y="0" width="76" height="60" rx="6" fill="#4A3424" stroke="{INK}" stroke-width="5"/><path d="M-30 10h60" stroke="#2F6FD6" stroke-width="7"/>
<path class="cross" style="--cd:2.2s" d="M-24 8l48 46M24 8l-48 46" stroke="#D8263A" stroke-width="9" stroke-linecap="round"/></g>
<text x="70" y="114" text-anchor="middle" style="font:700 22px var(--hand)">te droog</text><text x="230" y="114" text-anchor="middle" style="font:700 22px var(--hand)">te nat</text></svg>
<div class="col"><h2 class="a d2" style="font-size:13cqw">Beter te droog</h2><p class="sub a d4">dan te nat.</p></div>'''),
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
    page('pannenkoekenplant', 'Pannenkoekenplant in een minuut',
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
      dict(dur=5200, bg='#1E7A3C', dark=True, html=f'''<span class="tag a">Plantenfiche</span>
<svg class="art" viewBox="0 0 300 340" aria-hidden="true" style="width:74cqw">{sans_plant()}</svg>
<div class="col"><h2 class="a d3" style="font-size:14cqw">Sansevieria</h2><p class="note a d4" style="font-size:10cqw;color:var(--pot)">de vrouwentong</p></div>'''),
      dict(dur=4800, bg='#F4EEFF', html=f'''<span class="tag a">Verzorging</span>
<svg class="art" viewBox="0 0 300 260" aria-hidden="true">{sans_leaf(150,262,250,8,0)}{dust_wipe()}</svg>
<h2 class="a d2" style="font-size:15cqw">Afstoffen</h2>'''),
      dict(dur=6000, bg='#E3ECFF', html=f'''<span class="tag a">Water</span>
<svg class="art" viewBox="0 0 300 140" aria-hidden="true" style="width:60cqw">{drop(150,10,4,'flash','#7FC8E8')}</svg>
<div class="col" style="color:var(--blue)">
<h2 class="a d1" style="color:var(--ink)">Zeer weinig</h2>
<div class="cal a d2" style="grid-template-columns:repeat(4,1fr)">{cal}</div>
<span class="chip a d3">1x / 4 weken</span></div>'''),
      dict(dur=6200, bg='#FFF6C2', html=light_scene('<p class="note a d5" style="font-size:8.6cqw">van weinig tot veel</p>', half=True)),
      dict(dur=7000, bg='#E6F6E3', html=f'''<span class="tag a">Vermeerderen</span>
<svg class="art" viewBox="0 0 300 250" aria-hidden="true">
<g class="a d1"><g transform="translate(-60 0) scale(.8)">{sans_leaf(110,250,180,-8,.2)}{sans_leaf(135,250,210,4,.3)}<path d="M80 245h90l-10 60h-70Z" fill="#FFE24A" stroke="{INK}" stroke-width="5"/></g>
<g transform="translate(15 0) scale(.8)">{sans_leaf(120,250,190,6,.4)}<path d="M85 245h70l-8 60h-54Z" fill="#FFE24A" stroke="{INK}" stroke-width="5"/></g>
<path class="cross" style="--cd:.8s;stroke-dasharray:6 8" d="M90 110v140" stroke="{INK}" stroke-width="4"/></g>
<g class="a d4"><g transform="translate(225 110)"><path d="M-30 0h60v110h-60Z" fill="#CFE9F7" stroke="{INK}" stroke-width="5"/><path d="M-30 40h60v70h-60Z" fill="#7FC8E8" opacity=".8"/>{sans_leaf(0,80,95,0,0)}<path d="M-6 82l-6 18M0 82v20M6 82l6 18" stroke="#fff" stroke-width="2.5"/></g></g>
<text x="80" y="245" text-anchor="middle" style="font:700 24px var(--hand)" class="a d3">scheuren</text>
<text x="225" y="245" text-anchor="middle" style="font:700 24px var(--hand)" class="a d5">bladstek</text></svg>
<h2 class="a d2" style="font-size:10cqw">Scheuren<br>of bladstek</h2>'''),
      dict(dur=8800, bg='#FFFDF6', html=f'''<span class="tag a">Luchtfilter</span>
<div class="col" style="gap:5cqw">
<div class="pair a d1"><svg viewBox="-60 -60 120 120">{ghs(0,0,1,FLAME)}</svg><div style="text-align:left"><b>Benzeen</b><svg viewBox="0 0 170 60" style="width:44cqw;height:auto">{benzene(30,30)}<text x="74" y="40" class="mol">C₆H₆</text></svg></div></div>
<div class="pair a d3"><svg viewBox="-60 -60 120 120">{ghs(0,0,1,'<rect x="-30" y="-30" width="60" height="60" fill="#d6d6d6" transform="rotate(45)"/>'+SKULL)}</svg><div style="text-align:left"><b>Formaldehyde</b><svg viewBox="-60 -64 200 110" style="width:34cqw;height:auto">{formaldehyde(0,0)}</svg></div></div>
<div class="need a d5">6 à 8 planten nodig<small>goed verspreid</small></div></div>'''),
      dict(dur=6500, bg=INK, dark=True, html=f'''{recap([('Blad','afstoffen','var(--leaf-lt)'),('Water','zeer weinig, 1x per 4 weken','#AFC7F5'),('Licht','weinig tot veel indirect','var(--sun)'),('Vermeerderen','scheuren of bladstek','#CDB4F5'),('Lucht','benzeen, formaldehyde','#F59AA5'),('Aantal','6 à 8, goed verspreid','#FFE24A')])}
<p class="note a d6" style="color:var(--desk);font-size:9cqw">Sansevieria · vrouwentong</p>'''),
    ]
    page('vrouwentong', 'Vrouwentong in een minuut',
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
      dict(dur=5600, bg='#1E7A3C', dark=True, html=f'''<span class="tag a">Plantenfiche</span>
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
    page('graslelie', 'Graslelie in een minuut',
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

# Elke nieuwe plant: een regel hier. Feiten alleen van de fiche.
PLANTS = [
  dict(slug='rubberboom', name='Rubberboom', sci='Ficus elastica', tint='#BFE6C6', art=ficus_plant, vb='30 -10 240 345',
       facts=['1x / week water', 'indirect licht', 'luchtfilter: 1 à 3'], lucht=True, toxic=True),
  dict(slug='pannenkoekenplant', name='Pannenkoekenplant', sci='Pilea peperomioides', tint='#CFEFF0', art=lambda: pilea_plant(), vb='10 15 280 320',
       facts=['1x / week water', 'veel indirect licht', "stekken via baby'tjes"], lucht=False, toxic=False),
  dict(slug='vrouwentong', name='Vrouwentong', sci='Sansevieria', tint='#FFF1A8', art=sans_plant, vb='40 -20 220 360',
       facts=['1x / 4 weken water', 'weinig tot veel licht', 'luchtfilter: 6 à 8'], lucht=True, toxic=False),
  dict(slug='graslelie', name='Graslelie', sci='Chlorophytum comosum', tint='#DCE6FF', art=lambda: chloro_plant(), vb='20 20 280 310',
       facts=['ruim water, laat uitdrogen', 'indirect licht', 'luchtfilter: 4 à 6'], lucht=True, toxic=False),
]

OV_CSS = r"""
:root{--desk:#FFD60A;--ink:#141414;--paper:#FFFDF6;--leaf:#2E9E4F;--red:#D8263A;--purple:#5B2A9E;
--display:"Bricolage Grotesque",system-ui,sans-serif;--hand:"Caveat","Comic Sans MS",cursive;color-scheme:light}
body{margin:0;background:var(--desk);color:var(--ink);font-family:var(--display)}
.wrap{max-width:1040px;margin:0 auto;padding-inline:16px;padding-block:24px 56px}
.back{display:inline-block;font:700 14px var(--display);color:var(--ink);text-decoration:none;border:2px solid var(--ink);background:var(--paper);border-radius:99px;padding:4px 12px;margin-bottom:18px}
.top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px 24px;margin-bottom:22px}
h1{font:800 clamp(48px,11vw,104px)/.88 var(--display);letter-spacing:-.04em;margin:0;text-wrap:balance}
.hand{font:700 clamp(24px,5vw,34px)/1 var(--hand);margin:8px 0 0}
.tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.tools input{font:600 16px var(--display);color:var(--ink);border:3px solid var(--ink);border-radius:99px;padding:9px 16px;background:var(--paper);box-shadow:3px 3px 0 var(--ink);min-width:0;width:220px;max-width:100%}
.tools input::placeholder{color:#6b6b5e}
.chipbtn{font:800 14px var(--display);border:3px solid var(--ink);border-radius:99px;padding:9px 14px;background:var(--paper);color:var(--ink);box-shadow:3px 3px 0 var(--ink);cursor:pointer}
.chipbtn[aria-pressed="true"]{background:var(--ink);color:var(--desk)}
input:focus-visible,.chipbtn:focus-visible,.card:focus-visible,.back:focus-visible{outline:3px solid var(--purple);outline-offset:3px}
.sr{position:absolute;left:-9999px}
.count{font:700 24px var(--hand);margin:0 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:28px 22px}
.card{display:flex;flex-direction:column;text-decoration:none;color:var(--ink);background:var(--paper);border:3px solid var(--ink);border-radius:18px;box-shadow:6px 6px 0 var(--ink);overflow:hidden;transform:rotate(var(--r,0deg));transition:transform .2s,box-shadow .2s}
.card:hover{transform:rotate(0) translate(-2px,-4px);box-shadow:9px 10px 0 var(--ink)}
.card:nth-child(4n+1){--r:-1.2deg}.card:nth-child(4n+2){--r:.8deg}.card:nth-child(4n+3){--r:-.6deg}.card:nth-child(4n){--r:1.1deg}
.pic{aspect-ratio:4/3.4;display:grid;place-items:center;border-bottom:3px solid var(--ink);padding:12px;position:relative;box-sizing:border-box;max-width:100%}
.pic{overflow:hidden}.pic svg{position:absolute;top:12px;left:12px;width:calc(100% - 24px);height:calc(100% - 24px)}
.badge{position:absolute;top:10px;right:10px;font:800 11px var(--display);letter-spacing:.1em;text-transform:uppercase;background:var(--red);color:var(--paper);border-radius:99px;padding:4px 9px}
.body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.sci{font:700 22px/1 var(--hand);color:var(--leaf)}
.name{font:800 26px/1 var(--display);letter-spacing:-.02em;margin:0}
.facts{list-style:none;margin:2px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.facts li{font:600 13px/1.2 var(--display);border:2px solid var(--ink);border-radius:9px;padding:3px 8px}
.play{margin-top:auto;padding-top:8px;font:800 15px var(--display);display:flex;align-items:center;gap:8px}
.play i{width:30px;height:30px;border-radius:50%;background:var(--ink);display:grid;place-items:center;font-style:normal;color:var(--desk);font-size:12px}
.empty{font:700 28px var(--hand);text-align:center;padding:40px 0}
.foot{margin-top:44px;font:600 14px/1.5 var(--display);max-width:62ch}
@media (prefers-reduced-motion:reduce){.card{transition:none}}
"""

OV_JS = r"""
(function(){
 const q=document.getElementById('q'),f=document.getElementById('lucht'),cards=[...document.querySelectorAll('.card')],cnt=document.getElementById('count'),empty=document.getElementById('empty');
 function run(){const t=q.value.trim().toLowerCase(),only=f.getAttribute('aria-pressed')==='true';let n=0;
  cards.forEach(c=>{const ok=(!t||c.dataset.s.includes(t))&&(!only||c.dataset.lucht==='1');c.hidden=!ok;if(ok)n++});
  cnt.textContent=n===1?'1 plant':n+' planten';empty.hidden=n>0;}
 q.addEventListener('input',run);
 f.addEventListener('click',()=>{f.setAttribute('aria-pressed',f.getAttribute('aria-pressed')==='true'?'false':'true');run()});
 run();
})();
"""

ARTIFACT_LINKS = {'rubberboom':'https://claude.ai/artifact/Pe65DNa14PMjNJazRRsmVY','pannenkoekenplant':'https://claude.ai/artifact/Q1NQFtvBS527ePdVp2beuH','vrouwentong':'https://claude.ai/artifact/G4852WAcyFnP8FvMYAvd7M','graslelie':'https://claude.ai/artifact/5iLZijme21bXEyhVhve6cn'}

def build_overview():
    links = ARTIFACT_LINKS if ARTIFACT else {}
    cards = ''
    for pl in PLANTS:
        href = links.get(pl['slug'], pl['slug'] + '/')
        facts = ''.join(f'<li>{x}</li>' for x in pl['facts'])
        badge = '<span class="badge">giftig sap</span>' if pl['toxic'] else ''
        search = (pl['name'] + ' ' + pl['sci'] + ' ' + ' '.join(pl['facts'])).lower()
        cards += (f'<a class="card" href="{href}" data-s="{search}" data-lucht="{1 if pl["lucht"] else 0}">\n'
                  f'<div class="pic" style="background:{pl["tint"]}">{badge}<svg viewBox="{pl["vb"]}" aria-hidden="true">{pl["art"]()}</svg></div>\n'
                  f'<div class="body"><span class="sci">{pl["sci"]}</span><h2 class="name">{pl["name"]}</h2><ul class="facts">{facts}</ul>'
                  f'<span class="play"><i>&#9654;</i> Bekijk de reel</span></div></a>\n')
    defs = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{PL_LEAF}{FI_LEAF}</defs></svg>'
    core = f'<title>Plantenfiches</title>\n{FONTS}\n<style>{OV_CSS}</style>\n'
    main = (f'{defs}<div class="wrap">\n'
            f'<a class="back" href="https://onderconstructie.github.io/">&larr; Onder Constructie</a>\n'
            f'<header class="top"><div><h1>Plantenfiches</h1><p class="hand">getekend in een schriftje, tot leven gebracht</p></div>\n'
            f'<div class="tools"><label for="q" class="sr">Zoek een plant</label><input id="q" type="search" placeholder="Zoek een plant" autocomplete="off">\n'
            f'<button class="chipbtn" id="lucht" type="button" aria-pressed="false">Luchtfilter</button></div></header>\n'
            f'<p class="count" id="count" aria-live="polite"></p>\n'
            f'<div class="grid">{cards}</div>\n'
            f'<p class="empty" id="empty" hidden>Geen plant gevonden.</p>\n'
            f'<p class="foot">Elke reel volgt alleen wat op de handgetekende fiche staat.</p>\n'
            f'</div>\n<script>{OV_JS}</script>\n')
    if ARTIFACT:
        path = os.path.join(OUT, 'overzicht.html'); open(path, 'w').write(core + main)
    else:
        path = os.path.join(OUT, 'index.html')
        open(path, 'w').write('<!DOCTYPE html>\n<html lang="nl">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
            '<meta name="description" content="Geanimeerde plantenfiches van Onder Constructie.">\n'
            + core + '</head>\n<body>\n' + main + '</body>\n</html>\n')
    print('geschreven', path)

build_overview()
