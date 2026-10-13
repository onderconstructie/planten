"""Voegt de gedeelde compositielaag (layout.css + layout.js) en de motorkoppeling toe
aan een handgemaakte reel (zoals rubberboom). Veilig om opnieuw te draaien."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'layout.css')).read()
JS = open(os.path.join(HERE, 'layout.js')).read()
SMOOTH = open(os.path.join(HERE, 'smooth.css')).read()
HOOK_A = "fills.forEach((f,i)=>f.style.width=i<idx?'100%':'0%');"
HOOK_A2 = HOOK_A + "\n    document.dispatchEvent(new CustomEvent('reel:scene',{detail:idx}));"
SETPLAY = re.compile(r"(  function setPlay\(p\)\{[^\n]*\})")

def patch(s):
    if 'reel:scene' not in s:
        assert HOOK_A in s
        s = s.replace(HOOK_A, HOOK_A2, 1)
        s = SETPLAY.sub(lambda m: m.group(1) + "\n  window.__reel={go:i=>{show(i);setPlay(true)}};", s, count=1)
        assert 'window.__reel' in s
    s = re.sub(r'<style id="layout">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="layout-js">.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<style id="smooth">.*?</style>', '', s, flags=re.S)
    s = s.replace('</style>', '</style>\n<style id="layout">' + CSS + '</style>\n<style id="smooth">' + SMOOTH + '</style>', 1)
    i = s.rfind('</script>') + len('</script>')
    s = s[:i] + '\n<script id="layout-js">' + JS + '</script>' + s[i:]
    return s

if __name__ == '__main__':
    for p in sys.argv[1:]:
        src = open(p).read()
        out = patch(src)
        open(p, 'w').write(out)
        print('compositielaag toegepast:', p)
