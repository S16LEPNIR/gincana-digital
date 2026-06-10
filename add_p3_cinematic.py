"""
Añade cinemática de la Pintora a Prueba 3.
- Imagen 1 ('Pintora mirandote.jpg')      → 2 diálogos
- Crossfade suave a imagen 2 ('Pintora mirando el cuadro.jpg') → 2 diálogos
- Tras el último diálogo + tap → va directamente a initP3Game()
Misma composición que cinemáticas de Bruja y Reina del Jardín.
"""

import base64

HTML_PATH = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'
IMG1_PATH = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\Pintora mirandote.jpg'
IMG2_PATH = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\Pintora mirando el cuadro.jpg'

# ── 0. Codificar imágenes ────────────────────────────────────
with open(IMG1_PATH, 'rb') as f:
    img1_b64 = base64.b64encode(f.read()).decode('ascii')
with open(IMG2_PATH, 'rb') as f:
    img2_b64 = base64.b64encode(f.read()).decode('ascii')

img1_uri = f'data:image/jpeg;base64,{img1_b64}'
img2_uri = f'data:image/jpeg;base64,{img2_b64}'
print(f'[0] Imágenes codificadas: img1={len(img1_b64)//1024} KB, img2={len(img2_b64)//1024} KB')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    c = f.read()

errors = []

# ────────────────────────────────────────────────────────────
# 1. CSS — inyectar antes del bloque de la Reina del Jardín
# ────────────────────────────────────────────────────────────
P3_CIN_CSS = """\
/* ── PRUEBA 3 — CINEMÁTICA PINTORA ────────────────────────── */
#p3-cin-overlay{position:fixed;inset:0;background:#0d0a07;display:none;z-index:9999;flex-direction:column;align-items:center;justify-content:flex-end;overflow:hidden}
#p3-cin-overlay.active{display:flex}
#p3-cin-bg{position:absolute;inset:0}
#p3-cin-img1,#p3-cin-img2{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top}
#p3-cin-img1{opacity:.84}
#p3-cin-img2{opacity:0;transition:opacity 1.4s ease}
#p3-cin-img2.visible{opacity:.84}
#p3-cin-flies{position:absolute;inset:0;pointer-events:none;z-index:1}
#p3-cin-panel{position:relative;z-index:2;width:100%;max-width:480px;padding:18px 22px 34px;background:linear-gradient(0deg,rgba(13,10,7,.97) 70%,transparent)}
#p3-cin-speaker{font-family:var(--fnb);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#e8c87a;background:rgba(232,180,80,.13);border:1px solid rgba(232,180,80,.32);border-radius:20px;padding:4px 14px;display:inline-block;margin-bottom:10px}
#p3-cin-speech-wrap{width:100%;min-height:72px}
#p3-cin-text{font-family:var(--fnt);font-size:17px;color:#f2ede6;line-height:1.55;font-style:italic}
#p3-cin-tap{font-family:var(--fnb);font-size:11px;color:rgba(232,200,150,.4);text-align:right;margin-top:8px;letter-spacing:.05em}

"""

CSS_ANCHOR = '/* ── PRUEBA 5 — CINEMÁTICA REINA'
if CSS_ANCHOR in c:
    c = c.replace(CSS_ANCHOR, P3_CIN_CSS + CSS_ANCHOR, 1)
    print('[1] CSS inyectado')
else:
    errors.append('[1] Ancla CSS no encontrada')

# ────────────────────────────────────────────────────────────
# 2. HTML — inyectar antes del overlay de la Reina del Jardín
# ────────────────────────────────────────────────────────────
P3_CIN_HTML = f"""\
<!-- PRUEBA 3 — CINEMÁTICA LA PINTORA -->
<div id="p3-cin-overlay" onclick="p3CinTap()">
  <div id="p3-cin-bg">
    <img id="p3-cin-img1" src="{img1_uri}" alt="">
    <img id="p3-cin-img2" src="{img2_uri}" alt="">
  </div>
  <div id="p3-cin-flies"></div>
  <div id="p3-cin-panel">
    <div id="p3-cin-speaker">🎨 La Pintora</div>
    <div id="p3-cin-speech-wrap">
      <span id="p3-cin-text" class="sv-speech-text"></span><span class="cin-cursor">▌</span>
    </div>
    <div id="p3-cin-tap">Toca para continuar</div>
  </div>
</div>

"""

HTML_ANCHOR = '<!-- PRUEBA 5 — CINEMÁTICA REINA DEL JARDÍN -->'
if HTML_ANCHOR in c:
    c = c.replace(HTML_ANCHOR, P3_CIN_HTML + HTML_ANCHOR, 1)
    print('[2] HTML inyectado')
else:
    errors.append('[2] Ancla HTML no encontrada')

# ────────────────────────────────────────────────────────────
# 3. JS — inyectar antes del bloque de la Reina del Jardín
# ────────────────────────────────────────────────────────────
P3_DIALOGS = [
    # imagen 1
    "¿Sabías que el Umbráculo del Jardín Botánico de Valencia tiene como destino dar cabida a aquellas plantas que no pueden soportar la luz solar directa?",
    "Resguarda ejemplares que, por ejemplo, originalmente vivirían en bosques densos.",
    # imagen 2
    "Con el tiempo también se ha convertido en un refugio para los pintores.",
    "No te quedes ahí sembrado. Ayúdame a terminar mi cuadro.",
]
dialogs_js = ',\n  '.join(f'"{d}"' for d in P3_DIALOGS)

P3_CIN_JS = f"""\

// ── PRUEBA 3 — CINEMÁTICA PINTORA ───────────────────────────
var P3_CIN_DIALOGS = [
  {dialogs_js}
];
var _p3CinStep      = 0;
var _p3CinTyping    = false;
var _p3CinTimer     = null;
var _p3CinCrossfade = false;  // true durante el crossfade, bloquea taps

function openP3Cinematic() {{
  _p3CinStep = 0; _p3CinTyping = false; _p3CinCrossfade = false;
  document.getElementById('p3-cin-img2').classList.remove('visible');
  document.getElementById('p3-cin-overlay').classList.add('active');
  p3CinAddFireflies();
  p3CinTypeDialog(0);
}}

function p3CinAddFireflies() {{
  var fl = document.getElementById('p3-cin-flies');
  fl.innerHTML = '';
  for (var i = 0; i < 13; i++) {{
    var d = document.createElement('div');
    d.className = 'cin-fly';
    var r = Math.floor(220 + Math.random() * 35);
    var g = Math.floor(150 + Math.random() * 70);
    var b = Math.floor(40  + Math.random() * 40);
    d.style.cssText = 'left:'+(5+Math.random()*90)+'%;top:'+(5+Math.random()*65)+'%;'
      +'--dx:'+(Math.random()*60-30)+'px;--dy:'+(Math.random()*50-40)+'px;'
      +'--dur:'+(2+Math.random()*3)+'s;--del:-'+(Math.random()*3)+'s;'
      +'opacity:'+(0.4+Math.random()*0.5)+';'
      +'background:rgba('+r+','+g+','+b+',.9);'
      +'box-shadow:0 0 10px 4px rgba('+r+','+g+','+b+',.5);';
    fl.appendChild(d);
  }}
}}

function p3CinTypeDialog(idx) {{
  _p3CinTyping = true; _p3CinStep = idx;
  var el = document.getElementById('p3-cin-text');
  el.textContent = '';
  var txt = P3_CIN_DIALOGS[idx], i = 0;
  clearInterval(_p3CinTimer);
  _p3CinTimer = setInterval(function() {{
    if (i < txt.length) {{ el.textContent += txt[i++]; }}
    else {{ clearInterval(_p3CinTimer); _p3CinTyping = false; }}
  }}, 40);
}}

function p3CinTap() {{
  if (_p3CinCrossfade) return;   // bloquear taps durante crossfade

  if (_p3CinTyping) {{
    // completar texto al instante
    clearInterval(_p3CinTimer);
    document.getElementById('p3-cin-text').textContent = P3_CIN_DIALOGS[_p3CinStep];
    _p3CinTyping = false;
    return;
  }}

  if (_p3CinStep === 0) {{
    // diálogo 0 terminado → siguiente diálogo (misma imagen)
    p3CinTypeDialog(1);
  }} else if (_p3CinStep === 1) {{
    // diálogo 1 terminado → crossfade a imagen 2, luego diálogo 2
    _p3CinCrossfade = true;
    document.getElementById('p3-cin-text').textContent = '';
    document.getElementById('p3-cin-img2').classList.add('visible');
    setTimeout(function() {{
      _p3CinCrossfade = false;
      p3CinTypeDialog(2);
    }}, 1500);
  }} else if (_p3CinStep === 2) {{
    // diálogo 2 terminado → siguiente diálogo (misma imagen)
    p3CinTypeDialog(3);
  }} else {{
    // diálogo 3 (último) terminado → iniciar prueba
    document.getElementById('p3-cin-overlay').classList.remove('active');
    go('screen-p3-game');
    initP3Game();
  }}
}}
// ─────────────────────────────────────────────────────────────

"""

JS_ANCHOR = '// ── PRUEBA 5 — CINEMÁTICA REINA ──────────────────────────────'
if JS_ANCHOR in c:
    c = c.replace(JS_ANCHOR, P3_CIN_JS + JS_ANCHOR, 1)
    print('[3] JS inyectado')
else:
    errors.append('[3] Ancla JS no encontrada')

# ────────────────────────────────────────────────────────────
# 4. Redirigir el flujo de P3 para mostrar la cinemática
# ────────────────────────────────────────────────────────────
OLD_P3_FLOW = (
    '  // Prueba 3: Pieza a Pieza (Puzzle)\n'
    '  if (S.activeTestIndex === 2) {\n'
    "    go('screen-p3-game');\n"
    '    initP3Game();\n'
    '    return;\n'
    '  }'
)
NEW_P3_FLOW = (
    '  // Prueba 3: Pieza a Pieza (Puzzle)\n'
    '  if (S.activeTestIndex === 2) {\n'
    '    openP3Cinematic();\n'
    '    return;\n'
    '  }'
)
if OLD_P3_FLOW in c:
    c = c.replace(OLD_P3_FLOW, NEW_P3_FLOW, 1)
    print('[4] Flujo de P3 redirigido a cinemática')
else:
    errors.append('[4] Bloque de flujo P3 no encontrado')

# ────────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:', errors)
else:
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'\nAll OK — guardado. {len(c)//1024} KB')
