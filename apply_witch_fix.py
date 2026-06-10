#!/usr/bin/env python3
import sys, os, base64, re
sys.stdout.reconfigure(encoding='utf-8')

ASSETS = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
BACKUP = os.path.join(ASSETS, 'ginkana_standalone_backup.html')
OUTPUT = os.path.join(ASSETS, 'ginkana_standalone.html')

# Load images
with open(os.path.join(ASSETS, 'tarjeta planta.png'), 'rb') as f:
    PLANTA_B64 = base64.b64encode(f.read()).decode('ascii')

bruja_path = None
for fname in os.listdir(ASSETS):
    if 'Bruja' in fname and fname.endswith('.jpg'):
        bruja_path = os.path.join(ASSETS, fname)
        break
assert bruja_path, 'Bruja image not found!'
with open(bruja_path, 'rb') as f:
    BRUJA_B64 = base64.b64encode(f.read()).decode('ascii')
print(f'Images OK. Planta:{len(PLANTA_B64)} Bruja:{len(BRUJA_B64)}')

with open(BACKUP, 'r', encoding='utf-8') as f:
    content = f.read()
assert len(content.splitlines()) == 8155, f'Expected 8155, got {len(content.splitlines())}'
print('Backup loaded: 8155 lines OK')

# ── 1. Remove #tc2 CSS overrides ────────────────────────────────────────────
OLD_TC2_CSS = ('#tc2 > p {\n  font-size: 10px;\n  line-height: 1.35;\n'
               '  color: #555;\n  margin-bottom: 0;\n}\n'
               '#tc2 .tcard-split {\n  margin-top: 4px;\n}\n')
assert OLD_TC2_CSS in content, 'FAIL: tc2 CSS anchor not found'
content = content.replace(OLD_TC2_CSS, '', 1)
print('1. TC2 CSS removed')

# ── 2. Replace tc2 paragraph + SVG with image ───────────────────────────────
TC2_NEW = (
    '<h2>Encuentra la planta para empezar</h2>\n'
    '    <p>Busca la placa de la planta indicada e introduce los 4 primeros dígitos'
    ' de su número de referencia para comenzar la prueba.</p>\n'
    '    <div class="tcard-img"><img src="data:image/png;base64,' + PLANTA_B64 + '" alt="Tarjeta planta"></div>\n'
    '    <div class="tcard-footer">'
)
m = re.search(r'<h2>Encuentra la planta para empezar</h2>.*?    <div class="tcard-footer">', content, re.DOTALL)
assert m, 'FAIL: tc2 content anchor not found'
content = re.sub(
    r'<h2>Encuentra la planta para empezar</h2>.*?    <div class="tcard-footer">',
    TC2_NEW, content, count=1, flags=re.DOTALL
)
print('2. TC2 content replaced')

# ── 3. Witch CSS before </style> ─────────────────────────────────────────────
WITCH_CSS = """
/* == BRUJA POI == */
.poi.bruja .poi-pulse{background:rgba(255,220,100,.18);box-shadow:0 0 22px rgba(255,220,100,.65);animation:poiPulseAnim 1.8s infinite ease-in-out}
.poi.bruja .poi-core{background:radial-gradient(circle at 35% 35%,#fff,#f0e6c0);color:#7a4e00;font-size:18px;border-color:var(--dorado)}
/* == BRUJA CINEMATICA == */
#bru-cin-overlay{position:fixed;inset:0;background:#0a0a14;display:none;z-index:9999;flex-direction:column;align-items:center;justify-content:flex-end;overflow:hidden}
#bru-cin-overlay.active{display:flex}
#bru-cin-bg{position:absolute;inset:0}
#bru-cin-img{width:100%;height:100%;object-fit:cover;object-position:center top;opacity:.82}
#bru-cin-panel{position:relative;z-index:2;width:100%;max-width:480px;padding:18px 22px 28px;background:linear-gradient(0deg,rgba(10,8,24,.97) 70%,transparent)}
#bru-cin-speaker{font-family:var(--fnb);font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#f0d060;background:rgba(240,208,96,.14);border:1px solid rgba(240,208,96,.35);border-radius:20px;padding:4px 14px;display:inline-block;margin-bottom:10px}
#bru-cin-speech-wrap{width:100%;min-height:72px}
#bru-cin-text{font-family:var(--fnt);font-size:17px;color:#f2e8d0;line-height:1.55;font-style:italic}
.bru-choice-row{display:flex;gap:10px;margin-top:14px}
.bru-choice-btn{flex:1;padding:12px 8px;border:none;border-radius:14px;font-family:var(--fnb);font-size:14px;font-weight:700;cursor:pointer;transition:transform .15s}
.bru-choice-btn.gold{background:linear-gradient(135deg,#c9a84c,#f5d442);color:#3a2000;box-shadow:0 4px 18px rgba(197,164,60,.45)}
.bru-choice-btn.purple{background:linear-gradient(135deg,#6a2a9a,#9b4fd4);color:#fff;box-shadow:0 4px 18px rgba(130,50,200,.45)}
.cin-fly{position:absolute;width:7px;height:7px;border-radius:50%;background:rgba(255,230,80,.9);box-shadow:0 0 10px 4px rgba(255,220,60,.6);animation:flyDrift var(--dur,3s) var(--del,0s) infinite ease-in-out;pointer-events:none}
@keyframes flyDrift{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(var(--dx,20px),var(--dy,-30px)) scale(1.25)}}
/* == BRUJA ORACLE == */
#bru-oracle-overlay{position:fixed;inset:0;background:radial-gradient(ellipse at 50% 60%,#12073a,#050314);display:none;z-index:10000;align-items:center;justify-content:center}
#bru-oracle-overlay.active{display:flex}
.bru-oracle-inner{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 28px;max-width:360px;width:100%}
#bru-oracle-pre{font-family:var(--fnt);font-size:17px;color:rgba(240,208,96,.85);font-style:italic;line-height:1.55;min-height:56px;transition:opacity .4s;text-align:center}
.bru-prophecy-text{font-family:var(--fnt);font-size:20px;color:#e8d8ff;text-align:center;max-width:320px;line-height:1.6;font-style:italic;opacity:0;transition:opacity .6s}
.bru-prophecy-text.visible{opacity:1}
.bru-oracle-stars{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.bru-oracle-back-btn{margin-top:32px;background:rgba(255,255,255,.1);border:1.5px solid rgba(255,255,255,.2);color:rgba(255,255,255,.85);border-radius:22px;padding:11px 28px;font-family:var(--fnb);font-size:14px;cursor:pointer;opacity:0;transition:opacity .5s;pointer-events:none}
.bru-oracle-back-btn.visible{opacity:1;pointer-events:auto}
/* == BRUJA COMPAT == */
#bru-compat-overlay{position:fixed;inset:0;background:radial-gradient(ellipse at 50% 60%,#2a0a3a,#110020);display:none;z-index:10000;flex-direction:column;align-items:center;justify-content:center;padding:24px}
#bru-compat-overlay.active{display:flex}
.bru-compat-title{font-family:var(--fnt);font-size:22px;color:#e070ff;text-align:center;margin-bottom:20px;font-style:italic}
#bru-compat-type-sel{display:flex;flex-direction:column;align-items:center;gap:14px;width:100%;max-width:300px}
.bru-compat-type-label{font-family:var(--fnt);font-size:15px;color:rgba(232,192,255,.8);text-align:center;font-style:italic;margin:0 0 4px}
.bru-compat-type-btn{width:100%;padding:16px;border:2px solid rgba(224,112,255,.35);border-radius:14px;font-family:var(--fnb);font-size:16px;font-weight:700;background:rgba(255,255,255,.06);color:white;cursor:pointer;transition:background .2s,border-color .2s,transform .1s}
.bru-compat-type-btn:active{transform:scale(.97)}
.bru-compat-type-btn.friendship{border-color:rgba(255,220,80,.4);color:#ffe87a}
.bru-compat-type-btn.romance{border-color:rgba(255,100,160,.4);color:#ff88bb}
.bru-compat-inputs{display:flex;flex-direction:column;gap:12px;width:100%;max-width:300px;margin-bottom:20px}
.bru-compat-input{border:2px solid rgba(224,112,255,.4);border-radius:14px;padding:12px 16px;font-family:var(--fnb);font-size:16px;background:rgba(255,255,255,.08);color:white;outline:none;text-align:center}
.bru-compat-input::placeholder{color:rgba(255,255,255,.35)}
.bru-compat-btn{background:linear-gradient(135deg,#8a1aaa,#c040e0);border:none;border-radius:14px;padding:14px 32px;font-family:var(--fnb);font-size:16px;font-weight:700;color:white;cursor:pointer}
.bru-heart{font-size:88px;display:block;text-align:center;filter:drop-shadow(0 0 18px rgba(255,80,160,.7));animation:heartBeat 1s infinite;margin:12px 0}
@keyframes heartBeat{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
.bru-compat-pct{font-family:var(--fnt);font-size:52px;font-weight:700;color:#ff70c8;text-shadow:0 0 20px rgba(255,80,160,.6);text-align:center}
.bru-compat-phrase{font-family:var(--fnt);font-size:16px;color:#e8c0ff;text-align:center;max-width:300px;line-height:1.5;font-style:italic;margin-top:8px}
.bru-compat-close{position:absolute;top:18px;right:18px;background:rgba(255,255,255,.1);border:none;color:white;width:36px;height:36px;border-radius:50%;font-size:18px;cursor:pointer}
.bru-star{position:absolute;background:white;border-radius:50%;animation:starTwinkle var(--dur,2s) var(--del,0s) infinite ease-in-out;pointer-events:none}
@keyframes starTwinkle{0%,100%{opacity:.15}50%{opacity:.8}}
"""
assert '</style>' in content, 'FAIL: </style> not found'
content = content.replace('</style>', WITCH_CSS + '</style>', 1)
print('3. Witch CSS added')

# ── 4. Witch HTML after palmera cinematic ────────────────────────────────────
PALM_ANCHOR = '</div>\n\n<!-- PRUEBA 6'
assert PALM_ANCHOR in content, 'FAIL: palm anchor not found'

WITCH_HTML = (
    '</div>\n\n'
    '<!-- BRUJA — CINEMÁTICA -->\n'
    '<div id="bru-cin-overlay" onclick="bruCinTap()">\n'
    '  <div id="bru-cin-bg">\n'
    '    <img src="data:image/jpeg;base64,' + BRUJA_B64 + '" alt="" id="bru-cin-img">\n'
    '    <div id="bru-cin-black"></div>\n'
    '  </div>\n'
    '  <div id="bru-cin-flies"></div>\n'
    '  <div id="bru-cin-panel">\n'
    '    <div id="bru-cin-speaker">✨ El Jardín te Habla</div>\n'
    '    <div id="bru-cin-speech-wrap">\n'
    '      <span id="bru-cin-text" class="sv-speech-text"></span><span class="cin-cursor">▌</span>\n'
    '    </div>\n'
    '    <div class="bru-choice-row" id="bru-choice-row" style="display:none">\n'
    '      <button class="bru-choice-btn gold" onclick="bruChoiceOracle();event.stopPropagation()">\U0001f52e Adivinar el futuro</button>\n'
    '      <button class="bru-choice-btn purple" onclick="bruChoiceCompat();event.stopPropagation()">\U0001f49c Saber la compatibilidad</button>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>\n\n'
    '<!-- BRUJA — ORACLE -->\n'
    '<div id="bru-oracle-overlay" onclick="bruOracleTap()">\n'
    '  <div class="bru-oracle-stars" id="bru-oracle-stars"></div>\n'
    '  <div class="bru-oracle-inner">\n'
    '    <div id="bru-oracle-pre"></div>\n'
    '    <div class="bru-prophecy-text" id="bru-prophecy-text"></div>\n'
    '    <button class="bru-oracle-back-btn" id="bru-oracle-back" onclick="closeBruOracle();event.stopPropagation()">← Volver al mapa</button>\n'
    '  </div>\n'
    '</div>\n\n'
    '<!-- BRUJA — COMPATIBILIDAD -->\n'
    '<div id="bru-compat-overlay">\n'
    '  <button class="bru-compat-close" onclick="closeBruCompat()">✕</button>\n'
    '  <div class="bru-compat-title">\U0001f49c Test de Compatibilidad</div>\n'
    '  <div id="bru-compat-type-sel">\n'
    '    <p class="bru-compat-type-label">¿Qué tipo de vínculo deseas explorar?</p>\n'
    '    <button class="bru-compat-type-btn friendship" onclick="bruSetCompatType(\'amistad\')">\U0001f49b Amistad</button>\n'
    '    <button class="bru-compat-type-btn romance" onclick="bruSetCompatType(\'romance\')">❤️ Romance</button>\n'
    '  </div>\n'
    '  <div id="bru-compat-form" class="bru-compat-inputs" style="display:none">\n'
    '    <input class="bru-compat-input" id="bru-name1" type="text" placeholder="Tu nombre" maxlength="30">\n'
    '    <input class="bru-compat-input" id="bru-name2" type="text" placeholder="Nombre de la otra persona" maxlength="30">\n'
    '    <button class="bru-compat-btn" onclick="bruCalcCompat()">Calcular \U0001f49c</button>\n'
    '  </div>\n'
    '  <div id="bru-compat-result" style="display:none;flex-direction:column;align-items:center">\n'
    '    <div class="bru-heart" id="bru-heart-emoji">❤️</div>\n'
    '    <div class="bru-compat-pct" id="bru-compat-pct">0%</div>\n'
    '    <div class="bru-compat-phrase" id="bru-compat-phrase"></div>\n'
    '    <button class="bru-compat-btn" style="margin-top:18px" onclick="bruCompatReset()">Probar de nuevo</button>\n'
    '  </div>\n'
    '</div>\n\n'
    '<!-- PRUEBA 6'
)
content = content.replace(PALM_ANCHOR, WITCH_HTML, 1)
print('4. Witch HTML added')

# ── 5. Witch position functions after saveSupervisorPosition ─────────────────
AFTER_SV = ("function saveSupervisorPosition(x, y) {\n"
            "  try { localStorage.setItem('supervisorPos', JSON.stringify({ x, y })); } catch(e) {}\n"
            "}\n")
assert AFTER_SV in content, 'FAIL: saveSupervisorPosition anchor not found'
WITCH_POS = (
    "function loadWitchPosition() {\n"
    "  try { var p = JSON.parse(localStorage.getItem('witchPos')||'null'); if(p&&p.x!==undefined) return p; } catch(e){}\n"
    "  return { x: 62, y: 38 };\n"
    "}\n"
    "function saveWitchPosition(x, y) {\n"
    "  try { localStorage.setItem('witchPos', JSON.stringify({x:x,y:y})); } catch(e){}\n"
    "}\n"
)
content = content.replace(AFTER_SV, AFTER_SV + WITCH_POS, 1)
print('5. Witch position functions added')

# ── 6. Witch POI inside renderPOIs ───────────────────────────────────────────
RENDER_ANCHOR = ("    container.appendChild(supervisorPoi);\n"
                 "  }\n"
                 "}\n\n"
                 "// Abrir/cerrar menú contextual de POI")
assert RENDER_ANCHOR in content, 'FAIL: renderPOIs end anchor not found'
WITCH_POI_RENDER = (
    "  if (!hidden['witch-witch']) {\n"
    "    var witchPoi = document.createElement('div');\n"
    "    witchPoi.className = 'poi bruja';\n"
    "    witchPoi.id = 'poi-witch';\n"
    "    var wPos = loadWitchPosition();\n"
    "    witchPoi.style.left = wPos.x + '%';\n"
    "    witchPoi.style.top  = wPos.y + '%';\n"
    "    witchPoi.addEventListener('click', function(e) {\n"
    "      if (S.isCalibrating) return;\n"
    "      if (e.target.closest('.poi-menu-btn') || e.target.closest('.poi-ctx-menu')) return;\n"
    "      e.stopPropagation();\n"
    "      openWitchCinematic();\n"
    "    });\n"
    "    witchPoi.innerHTML = '<div class=\"poi-ctx-menu\"><button class=\"poi-ctx-item\" onclick=\"startRelocatePoi(\\'witch\\',\\'witch\\',event)\">✏️ Reubicar</button></div><div class=\"poi-pulse\"></div><div class=\"poi-core\">★</div>';\n"
    "    container.appendChild(witchPoi);\n"
    "  }\n"
)
content = content.replace(
    RENDER_ANCHOR,
    "    container.appendChild(supervisorPoi);\n  }\n" + WITCH_POI_RENDER + "}\n\n// Abrir/cerrar menú contextual de POI",
    1
)
print('6. Witch POI render added')

# ── 7. startRelocatePoi witch case ───────────────────────────────────────────
START_ANCHOR = "  else if (type === 'supervisor') poiEl = document.getElementById('poi-supervisor');\n"
assert START_ANCHOR in content, 'FAIL: startRelocatePoi supervisor case not found'
content = content.replace(
    START_ANCHOR,
    START_ANCHOR + "  else if (type === 'witch') poiEl = document.getElementById('poi-witch');\n",
    1
)
print('7. startRelocatePoi witch case added')

# ── 8. finishRelocatePoi witch case ──────────────────────────────────────────
FINISH_ANCHOR = "  else if (type === 'supervisor') { saveSupervisorPosition(x, y); }\n"
assert FINISH_ANCHOR in content, 'FAIL: finishRelocatePoi supervisor case not found'
content = content.replace(
    FINISH_ANCHOR,
    FINISH_ANCHOR + "  else if (type === 'witch') { saveWitchPosition(x, y); }\n",
    1
)
print('8. finishRelocatePoi witch case added')

# ── 9. Main witch JS before last </script> ───────────────────────────────────
WITCH_JS = """
// ── BRUJA ADIVINA ──────────────────────────────────────
var BRU_PRE_PHRASES = [
  "Mmm... veamos qué nos depara el jardín...",
  "Estoy conectando con los espíritus del jardín...",
  "Las raíces me transmiten sus secretos...",
  "Los astros están alineándose para ti...",
  "Siento las energías concentrarse...",
  "El viento entre las hojas me habla de ti..."
];
var BRU_PROPHECIES = [
  "Veo mucha luz en tu interior. Si te arriesgas hoy, será un buen día.",
  "El jardín te dice: lo que buscas está más cerca de lo que crees.",
  "Una pequeña decisión hoy puede cambiar el rumbo de muchas cosas.",
  "Alguien piensa en ti con afecto en este preciso momento.",
  "Tu curiosidad es tu mayor fortaleza. Úsala sin miedo hoy.",
  "El universo conspira a tu favor. Confía en el proceso.",
  "Una sorpresa agradable llegará cuando menos la esperes.",
  "Tu energía de hoy es contagiosa. Compártela con quienes te rodean.",
  "Lo que plantes hoy crecerá en momentos de gran felicidad.",
  "Hay una puerta que no has abierto todavía. Hoy es el momento.",
  "Alguien valora más de lo que crees el tiempo que pasas con ellos.",
  "Un momento de silencio hoy te traerá una gran claridad mañana.",
  "Tu intuición es correcta. Sigue ese camino sin dudar.",
  "Los obstáculos de hoy son los recuerdos con los que reirás mañana.",
  "El jardín lo sabe: hoy vas a descubrir algo que te hará sonreír."
];
var _bruCinStep = 0, _bruCinTyping = false, _bruCinTimer = null;
var _bruCompatType = 'romance';

// ── MUSIC ───────────────────────────────────────────────
var _bruAudioCtx = null;
var _bruMasterGain = null;
var _bruMusicLoop = null;
var _bruMusicPlaying = false;
var _bruDelayNode = null;
// [freq_hz, start_sec, dur_sec, velocity_0to1]
var BRU_MELODY = [
  // Frase 1 — descendente D5→G4 (cuento, tranquilo)
  [587.33, 0.00, 0.55, 0.65],
  [523.25, 0.60, 0.35, 0.58],
  [493.88, 1.00, 0.35, 0.55],
  [440.00, 1.40, 0.55, 0.60],
  [392.00, 2.00, 0.90, 0.68],
  // Frase 2 — ascendente G4→D5 y vuelta
  [392.00, 3.00, 0.32, 0.52],
  [440.00, 3.38, 0.32, 0.52],
  [493.88, 3.76, 0.32, 0.55],
  [587.33, 4.14, 0.55, 0.62],
  [523.25, 4.74, 0.35, 0.58],
  [493.88, 5.14, 0.85, 0.62],
  // Frase 3 — pico E5 con adorno
  [659.25, 6.10, 0.55, 0.62],
  [587.33, 6.70, 0.32, 0.58],
  [523.25, 7.07, 0.32, 0.52],
  [493.88, 7.44, 0.32, 0.52],
  [440.00, 7.81, 0.32, 0.55],
  [493.88, 8.18, 0.32, 0.52],
  [523.25, 8.55, 0.55, 0.58],
  // Frase 4 — resolución final a G4
  [587.33, 9.40, 0.55, 0.65],
  [523.25, 9.98, 0.32, 0.58],
  [493.88,10.35, 0.32, 0.55],
  [440.00,10.72, 0.32, 0.55],
  [392.00,11.09, 1.20, 0.70],
  // Bajo suave
  [98.00,  0.00, 2.80, 0.17],
  [98.00,  3.00, 2.90, 0.17],
  [130.81, 6.10, 2.80, 0.17],
  [146.83, 9.40, 2.90, 0.17],
  // Armonía media (muy suave)
  [196.00, 0.00, 2.50, 0.11],
  [196.00, 3.00, 2.50, 0.11],
  [246.94, 0.00, 2.20, 0.13],
  [261.63, 6.10, 2.50, 0.11],
  [293.66, 9.40, 2.50, 0.13]
];
var BRU_MELODY_DUR = 12.5;
function bruStartMusic() {
  if (_bruMusicPlaying) return;
  try { _bruAudioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e) { return; }
  _bruMusicPlaying = true;
  _bruMasterGain = _bruAudioCtx.createGain();
  _bruMasterGain.gain.setValueAtTime(0, _bruAudioCtx.currentTime);
  _bruMasterGain.gain.linearRampToValueAtTime(0.32, _bruAudioCtx.currentTime + 2.5);
  _bruMasterGain.connect(_bruAudioCtx.destination);
  _bruDelayNode = _bruAudioCtx.createDelay(1.0);
  _bruDelayNode.delayTime.value = 0.28;
  var fb = _bruAudioCtx.createGain(); fb.gain.value = 0.26;
  var dOut = _bruAudioCtx.createGain(); dOut.gain.value = 0.38;
  _bruDelayNode.connect(fb); fb.connect(_bruDelayNode);
  _bruDelayNode.connect(dOut); dOut.connect(_bruMasterGain);
  bruScheduleMelody(_bruAudioCtx.currentTime + 0.1);
}
function bruScheduleMelody(t0) {
  if (!_bruMusicPlaying || !_bruAudioCtx) return;
  var ctx = _bruAudioCtx;
  BRU_MELODY.forEach(function(n) {
    var t = t0 + n[1];
    var osc = ctx.createOscillator();
    var env = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.value = n[0];
    osc.detune.value = Math.random() * 4 - 2;
    env.gain.setValueAtTime(0, t);
    env.gain.linearRampToValueAtTime(n[3] * 0.75, t + 0.018);
    env.gain.exponentialRampToValueAtTime(n[3] * 0.28, t + 0.07);
    env.gain.exponentialRampToValueAtTime(0.0001, t + n[2]);
    osc.connect(env);
    env.connect(_bruMasterGain);
    if (_bruDelayNode) env.connect(_bruDelayNode);
    osc.start(t); osc.stop(t + n[2] + 0.15);
  });
  var wait = Math.max(0, (t0 + BRU_MELODY_DUR - ctx.currentTime) * 1000 - 150);
  _bruMusicLoop = setTimeout(function() {
    if (_bruMusicPlaying) bruScheduleMelody(t0 + BRU_MELODY_DUR);
  }, wait);
}
function bruStopMusic() {
  if (!_bruMusicPlaying) return;
  _bruMusicPlaying = false;
  clearTimeout(_bruMusicLoop);
  if (_bruMasterGain && _bruAudioCtx) {
    var now = _bruAudioCtx.currentTime;
    _bruMasterGain.gain.setValueAtTime(_bruMasterGain.gain.value, now);
    _bruMasterGain.gain.linearRampToValueAtTime(0, now + 3.5);
    var ctx = _bruAudioCtx;
    setTimeout(function() { try { ctx.close(); } catch(e) {} }, 3700);
  }
  _bruAudioCtx = null; _bruMasterGain = null; _bruDelayNode = null;
}

function openWitchCinematic() {
  var ov = document.getElementById('bru-cin-overlay');
  ov.classList.add('active');
  _bruCinStep = 0; _bruCinTyping = false;
  document.getElementById('bru-choice-row').style.display = 'none';
  bruAddFireflies();
  bruStartMusic();
  bruTypeDialog(0);
}
function bruAddFireflies() {
  var fl = document.getElementById('bru-cin-flies');
  fl.innerHTML = '';
  for (var i = 0; i < 12; i++) {
    var d = document.createElement('div');
    d.className = 'cin-fly';
    d.style.cssText = 'left:'+(10+Math.random()*80)+'%;top:'+(10+Math.random()*60)+'%;'
      +'--dx:'+(Math.random()*60-30)+'px;--dy:'+(Math.random()*50-40)+'px;'
      +'--dur:'+(2+Math.random()*3)+'s;--del:-'+(Math.random()*3)+'s;'
      +'opacity:'+(0.5+Math.random()*0.5)+';';
    fl.appendChild(d);
  }
}
var BRU_DIALOGS = [
  "El jardín guarda secretos milenarios… y yo soy su voz. Acércate, viajero.",
  "Las plantas que te rodean son sabias. Cada hoja es una página de un libro antiguo.",
  "Siento en el aire una pregunta que aún no has formulado. ¿Qué deseas saber?"
];
function bruTypeDialog(idx) {
  if (idx >= BRU_DIALOGS.length) {
    document.getElementById('bru-choice-row').style.display = 'flex'; return;
  }
  _bruCinTyping = true; _bruCinStep = idx;
  var el = document.getElementById('bru-cin-text');
  el.textContent = '';
  var txt = BRU_DIALOGS[idx], i = 0;
  clearInterval(_bruCinTimer);
  _bruCinTimer = setInterval(function() {
    if (i < txt.length) { el.textContent += txt[i++]; }
    else { clearInterval(_bruCinTimer); _bruCinTyping = false; }
  }, 38);
}
function bruCinTap() {
  if (_bruCinTyping) {
    clearInterval(_bruCinTimer);
    document.getElementById('bru-cin-text').textContent = BRU_DIALOGS[_bruCinStep];
    _bruCinTyping = false;
  } else {
    bruTypeDialog(_bruCinStep + 1);
  }
}
function closeBruCinematic() {
  clearInterval(_bruCinTimer);
  bruStopMusic();
  document.getElementById('bru-cin-overlay').classList.remove('active');
}

// ── ORACLE (tap-to-advance) ──────────────────────────────
var _bruOracleSteps = [];
var _bruOracleIdx = 0;
var _bruOracleTyping = false;
var _bruOracleTimer = null;
var _bruOracleDone = false;

function bruChoiceOracle() {
  closeBruCinematic();
  var shuffled = BRU_PRE_PHRASES.slice().sort(function(){ return Math.random() - .5; });
  var prophecy = BRU_PROPHECIES[Math.floor(Math.random() * BRU_PROPHECIES.length)];
  _bruOracleSteps = [shuffled[0], shuffled[1], prophecy];
  _bruOracleIdx = 0;
  _bruOracleTyping = false;
  _bruOracleDone = false;
  clearInterval(_bruOracleTimer);
  var preEl = document.getElementById('bru-oracle-pre');
  var propEl = document.getElementById('bru-prophecy-text');
  preEl.textContent = '';
  preEl.style.display = 'block';
  propEl.textContent = '';
  propEl.classList.remove('visible');
  document.getElementById('bru-oracle-back').classList.remove('visible');
  bruAddOracleStars();
  document.getElementById('bru-oracle-overlay').classList.add('active');
  bruOracleShowStep(0);
  _bruOracleIdx = 1;
}
function bruAddOracleStars() {
  var c = document.getElementById('bru-oracle-stars');
  c.innerHTML = '';
  for (var i = 0; i < 40; i++) {
    var s = document.createElement('div');
    s.className = 'bru-star';
    var sz = 1 + Math.random() * 2;
    s.style.cssText = 'width:'+sz+'px;height:'+sz+'px;left:'+Math.random()*100+'%;top:'+Math.random()*100+'%;'
      +'--dur:'+(1.5+Math.random()*2.5)+'s;--del:-'+(Math.random()*3)+'s;';
    c.appendChild(s);
  }
}
function bruOracleShowStep(idx) {
  var isLast = (idx === _bruOracleSteps.length - 1);
  var text = _bruOracleSteps[idx];
  var preEl = document.getElementById('bru-oracle-pre');
  var propEl = document.getElementById('bru-prophecy-text');
  var el;
  if (isLast) {
    preEl.style.display = 'none';
    propEl.textContent = '';
    propEl.classList.remove('visible');
    setTimeout(function(){ propEl.classList.add('visible'); }, 40);
    el = propEl;
  } else {
    preEl.style.display = 'block';
    preEl.textContent = '';
    el = preEl;
  }
  var i = 0;
  _bruOracleTyping = true;
  clearInterval(_bruOracleTimer);
  _bruOracleTimer = setInterval(function() {
    if (i < text.length) {
      el.textContent += text[i++];
    } else {
      clearInterval(_bruOracleTimer);
      _bruOracleTyping = false;
      if (isLast) {
        setTimeout(function() {
          document.getElementById('bru-oracle-back').classList.add('visible');
          _bruOracleDone = true;
        }, 400);
      }
    }
  }, isLast ? 32 : 38);
}
function bruOracleTap() {
  if (_bruOracleDone) {
    closeBruOracle();
    return;
  }
  if (_bruOracleTyping) {
    clearInterval(_bruOracleTimer);
    _bruOracleTyping = false;
    var curIdx = _bruOracleIdx - 1;
    var isLast = (curIdx === _bruOracleSteps.length - 1);
    var el = isLast ? document.getElementById('bru-prophecy-text') : document.getElementById('bru-oracle-pre');
    el.textContent = _bruOracleSteps[curIdx];
    if (isLast) {
      el.classList.add('visible');
      setTimeout(function() {
        document.getElementById('bru-oracle-back').classList.add('visible');
        _bruOracleDone = true;
      }, 400);
    }
    return;
  }
  if (_bruOracleIdx < _bruOracleSteps.length) {
    bruOracleShowStep(_bruOracleIdx);
    _bruOracleIdx++;
  }
}
function closeBruOracle() {
  clearInterval(_bruOracleTimer);
  _bruOracleTyping = false;
  document.getElementById('bru-oracle-overlay').classList.remove('active');
}

// ── COMPATIBILIDAD ──────────────────────────────────────
function bruChoiceCompat() {
  closeBruCinematic();
  document.getElementById('bru-compat-type-sel').style.display = 'flex';
  document.getElementById('bru-compat-form').style.display = 'none';
  document.getElementById('bru-compat-result').style.display = 'none';
  document.getElementById('bru-name1').value = '';
  document.getElementById('bru-name2').value = '';
  document.getElementById('bru-compat-overlay').classList.add('active');
}
function bruSetCompatType(type) {
  _bruCompatType = type;
  var heartEl = document.getElementById('bru-heart-emoji');
  if (heartEl) heartEl.textContent = type === 'amistad' ? '💛' : '❤️';
  document.getElementById('bru-compat-type-sel').style.display = 'none';
  document.getElementById('bru-compat-form').style.display = 'flex';
}
function closeBruCompat() {
  document.getElementById('bru-compat-overlay').classList.remove('active');
}
function bruCompatReset() {
  _bruCompatType = 'romance';
  document.getElementById('bru-compat-type-sel').style.display = 'flex';
  document.getElementById('bru-compat-form').style.display = 'none';
  document.getElementById('bru-compat-result').style.display = 'none';
  document.getElementById('bru-name1').value = '';
  document.getElementById('bru-name2').value = '';
  var heartEl = document.getElementById('bru-heart-emoji');
  if (heartEl) heartEl.textContent = '❤️';
}
function bruCalcCompat() {
  var a = document.getElementById('bru-name1').value.trim();
  var b = document.getElementById('bru-name2').value.trim();
  if (!a || !b) { alert('Introduce los dos nombres para calcular la compatibilidad.'); return; }
  var seed = 0, combined = (a + b).toLowerCase();
  for (var i = 0; i < combined.length; i++) seed += combined.charCodeAt(i);
  var pct = 60 + (seed % 40);
  var phrasesAmist = [
    "Una amistad verdadera, de esas que duran toda la vida.",
    "Vuestra conexión es como las raíces de un árbol: profunda y firme.",
    "Hay una complicidad especial entre vosotros. El jardín lo confirma.",
    "Una chispa de amistad que puede convertirse en algo inquebrantable."
  ];
  var phrasesRom = [
    "Una conexión cósmica extraordinaria. Las estrellas os unieron.",
    "Vuestra armonía es como la de las flores y las abejas. Perfectos.",
    "Un lazo muy especial os une. El jardín lo puede sentir.",
    "Hay chispa entre vosotros. La magia ya ha comenzado a actuar."
  ];
  var phrases = _bruCompatType === 'amistad' ? phrasesAmist : phrasesRom;
  var phraseIdx = pct >= 90 ? 0 : pct >= 80 ? 1 : pct >= 70 ? 2 : 3;
  document.getElementById('bru-compat-form').style.display = 'none';
  var resultEl = document.getElementById('bru-compat-result');
  resultEl.style.display = 'flex';
  var pctEl = document.getElementById('bru-compat-pct');
  pctEl.textContent = '0%';
  document.getElementById('bru-compat-phrase').textContent = phrases[phraseIdx];
  var current = 0;
  var timer = setInterval(function() {
    if (current < pct) { current++; pctEl.textContent = current + '%'; }
    else clearInterval(timer);
  }, 25);
}
"""

last_idx = content.rfind('</script>')
assert last_idx >= 0, 'FAIL: </script> not found'
content = content[:last_idx] + WITCH_JS + '\n</script>' + content[last_idx + 9:]
print('9. Witch JS added')

# ── Write output ──────────────────────────────────────────────────────────────
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)
out_lines = len(content.splitlines())
print(f'\nDone! Written {out_lines} lines to ginkana_standalone.html')
