"""
Añade cinemática de la Reina del Jardín a Prueba 5.
- Embedding de 'Reyna Jardín.jpg' como base64
- CSS/HTML/JS para el overlay (igual composición que bruja)
- Al terminar el último diálogo, toca → fundido a negro → inicia meditación
"""

import base64, re, os

html_path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'
img_path  = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\Reyna Jardín.jpg'

# ── 0. Encode image ──────────────────────────────────────────
with open(img_path, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('ascii')

img_data_uri = f'data:image/jpeg;base64,{img_b64}'
print(f'[0] Image encoded: {len(img_b64)//1024} KB')

# ── Read HTML ────────────────────────────────────────────────
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

errors = []

# ────────────────────────────────────────────────────────────
# 1. CSS — inject before the bruja overlay styles block
# ────────────────────────────────────────────────────────────
P5_CIN_CSS = """\
/* ── PRUEBA 5 — CINEMÁTICA REINA ──────────────────────────── */
#p5-cin-overlay{position:fixed;inset:0;background:#060e06;display:none;z-index:9999;flex-direction:column;align-items:center;justify-content:flex-end;overflow:hidden}
#p5-cin-overlay.active{display:flex}
#p5-cin-bg{position:absolute;inset:0}
#p5-cin-img{width:100%;height:100%;object-fit:cover;object-position:center top;opacity:.82}
#p5-cin-black{position:absolute;inset:0;background:#000;opacity:0;transition:opacity 1.8s ease;pointer-events:none;z-index:3}
#p5-cin-black.fade{opacity:1}
#p5-cin-flies{position:absolute;inset:0;pointer-events:none;z-index:1}
#p5-cin-panel{position:relative;z-index:2;width:100%;max-width:480px;padding:18px 22px 34px;background:linear-gradient(0deg,rgba(6,14,6,.97) 70%,transparent)}
#p5-cin-speaker{font-family:var(--fnb);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#8fd88f;background:rgba(100,200,100,.13);border:1px solid rgba(100,200,100,.32);border-radius:20px;padding:4px 14px;display:inline-block;margin-bottom:10px}
#p5-cin-speech-wrap{width:100%;min-height:72px}
#p5-cin-text{font-family:var(--fnt);font-size:17px;color:#e8f2e8;line-height:1.55;font-style:italic}
#p5-cin-tap{font-family:var(--fnb);font-size:11px;color:rgba(200,230,200,.45);text-align:right;margin-top:8px;letter-spacing:.05em}

"""

CSS_ANCHOR = '#bru-cin-overlay{position:fixed'
if CSS_ANCHOR in c:
    c = c.replace(CSS_ANCHOR, P5_CIN_CSS + CSS_ANCHOR, 1)
    print('[1] CSS injected')
else:
    errors.append('[1] CSS anchor not found')

# ────────────────────────────────────────────────────────────
# 2. HTML — inject overlay before the bruja overlay
# ────────────────────────────────────────────────────────────
P5_CIN_HTML = f"""\
<!-- PRUEBA 5 — CINEMÁTICA REINA DEL JARDÍN -->
<div id="p5-cin-overlay" onclick="p5CinTap()">
  <div id="p5-cin-bg">
    <img id="p5-cin-img" src="{img_data_uri}" alt="">
    <div id="p5-cin-black"></div>
  </div>
  <div id="p5-cin-flies"></div>
  <div id="p5-cin-panel">
    <div id="p5-cin-speaker">👑 La Reina del Jardín</div>
    <div id="p5-cin-speech-wrap">
      <span id="p5-cin-text" class="sv-speech-text"></span><span class="cin-cursor">▌</span>
    </div>
    <div id="p5-cin-tap">Toca para continuar</div>
  </div>
</div>

"""

HTML_ANCHOR = '<div id="bru-cin-overlay" onclick="bruCinTap()">'
if HTML_ANCHOR in c:
    c = c.replace(HTML_ANCHOR, P5_CIN_HTML + HTML_ANCHOR, 1)
    print('[2] HTML injected')
else:
    errors.append('[2] HTML anchor not found')

# ────────────────────────────────────────────────────────────
# 3. JS — inject before the P5 music section marker
# ────────────────────────────────────────────────────────────
P5_CIN_DIALOGS = [
    "No me gustas. Tienes algo diferente a todas las plantas que han venido antes buscando refugio.",
    "Es como si vivieras a otro ritmo. Un ritmo acelerado, ignorando la belleza de la vida que nos rodea.",
    "Quizás tendría que quitarte la vista para que aprendieras a ver a tu alrededor."
]
dialogs_js = ',\n  '.join(f'"{d}"' for d in P5_CIN_DIALOGS)

P5_CIN_JS = f"""\

// ── PRUEBA 5 — CINEMÁTICA REINA ──────────────────────────────
var P5_CIN_DIALOGS = [
  {dialogs_js}
];
var _p5CinStep   = 0;
var _p5CinTyping = false;
var _p5CinTimer  = null;

function openP5Cinematic() {{
  _p5CinStep = 0; _p5CinTyping = false;
  document.getElementById('p5-cin-black').classList.remove('fade');
  document.getElementById('p5-cin-overlay').classList.add('active');
  p5CinAddFireflies();
  p5CinTypeDialog(0);
}}

function p5CinAddFireflies() {{
  var fl = document.getElementById('p5-cin-flies');
  fl.innerHTML = '';
  for (var i = 0; i < 14; i++) {{
    var d = document.createElement('div');
    d.className = 'cin-fly';
    // tonos verdosos para la Reina del Jardín
    var green = Math.floor(180 + Math.random() * 75);
    var red   = Math.floor(80  + Math.random() * 60);
    d.style.cssText = 'left:'+(5+Math.random()*90)+'%;top:'+(5+Math.random()*65)+'%;'
      +'--dx:'+(Math.random()*60-30)+'px;--dy:'+(Math.random()*50-40)+'px;'
      +'--dur:'+(2+Math.random()*3)+'s;--del:-'+(Math.random()*3)+'s;'
      +'opacity:'+(0.4+Math.random()*0.55)+';'
      +'background:rgba('+red+','+green+',80,.92);'
      +'box-shadow:0 0 10px 4px rgba('+red+','+green+',60,.55);';
    fl.appendChild(d);
  }}
}}

function p5CinTypeDialog(idx) {{
  if (idx >= P5_CIN_DIALOGS.length) {{
    // último diálogo terminó — siguiente tap cierra con fundido a negro
    _p5CinStep = P5_CIN_DIALOGS.length;
    return;
  }}
  _p5CinTyping = true; _p5CinStep = idx;
  var el = document.getElementById('p5-cin-text');
  el.textContent = '';
  var txt = P5_CIN_DIALOGS[idx], i = 0;
  clearInterval(_p5CinTimer);
  _p5CinTimer = setInterval(function() {{
    if (i < txt.length) {{ el.textContent += txt[i++]; }}
    else {{ clearInterval(_p5CinTimer); _p5CinTyping = false; }}
  }}, 40);
}}

function p5CinTap() {{
  if (_p5CinTyping) {{
    // completar texto al instante
    clearInterval(_p5CinTimer);
    document.getElementById('p5-cin-text').textContent = P5_CIN_DIALOGS[_p5CinStep];
    _p5CinTyping = false;
  }} else if (_p5CinStep < P5_CIN_DIALOGS.length) {{
    p5CinTypeDialog(_p5CinStep + 1);
  }} else {{
    // fundido a negro y luego iniciar meditación
    document.getElementById('p5-cin-black').classList.add('fade');
    setTimeout(function() {{
      document.getElementById('p5-cin-overlay').classList.remove('active');
      go('screen-p5-meditation');
      initP5Meditation();
    }}, 1900);
  }}
}}
// ─────────────────────────────────────────────────────────────

"""

JS_ANCHOR = '// ── PRUEBA 5 — MÚSICA MEDITACIÓN'
if JS_ANCHOR in c:
    c = c.replace(JS_ANCHOR, P5_CIN_JS + JS_ANCHOR, 1)
    print('[3] JS injected')
else:
    errors.append('[3] JS anchor not found')

# ────────────────────────────────────────────────────────────
# 4. Redirect the P5 code-verification block to the cinematic
# ────────────────────────────────────────────────────────────
OLD_P5_FLOW = (
    '  // Prueba 5: Un Momento de Silencio\n'
    '  if (S.activeTestIndex === 4) {\n'
    "    go('screen-p5-meditation');\n"
    '    initP5Meditation();\n'
    '    return;\n'
    '  }'
)
NEW_P5_FLOW = (
    '  // Prueba 5: Un Momento de Silencio\n'
    '  if (S.activeTestIndex === 4) {\n'
    '    openP5Cinematic();\n'
    '    return;\n'
    '  }'
)
if OLD_P5_FLOW in c:
    c = c.replace(OLD_P5_FLOW, NEW_P5_FLOW, 1)
    print('[4] P5 flow redirected to cinematic')
else:
    errors.append('[4] P5 flow block not found')

# ────────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:', errors)
else:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'\nAll OK — saved. {len(c)//1024} KB')
