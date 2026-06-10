#!/usr/bin/env python3
# -*- coding: utf-8 -*-
assets = 'C:/Users/Sergio/Desktop/Mapa interactivo assets'
html_path = f'{assets}/ginkana_standalone.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Tamaño inicial: {len(html):,} chars")

# ─────────────────────────────────────────────
# CAMBIO 1 — Texto intro
# ─────────────────────────────────────────────
OLD_INTRO = '<p class="p1-intro-text">Antes de que existieran las farmacias, las plantas eran la única medicina. Los monjes botánicos del jardín sabían exactamente para qué servía cada una. ¿Tú también lo sabes?</p>'
NEW_INTRO = '<p class="p1-intro-text">Antes de que existieran las farmacias, las plantas eran la única medicina. ¿Sabes para qué sirve cada una de estas plantas?</p>'
assert OLD_INTRO in html, "ERROR: texto intro no encontrado"
html = html.replace(OLD_INTRO, NEW_INTRO, 1)
print("OK  Cambio 1: texto intro actualizado")

# ─────────────────────────────────────────────
# CAMBIO 2a — CSS photo-placeholder + cámara
# ─────────────────────────────────────────────
OLD_CSS = (
    '.p2-photo-placeholder {\n'
    '  display: flex;\n'
    '  flex-direction: column;\n'
    '  align-items: center;\n'
    '  justify-content: center;\n'
    '  gap: 6px;\n'
    '  color: #b0a090;\n'
    '  pointer-events: none;\n'
    '}\n'
    '\n'
    '.p2-photo-placeholder p { font-size: 11px; font-weight: 600; letter-spacing: .05em; margin: 0; }\n'
    '\n'
    '.p2-photo-img {\n'
    '  position: absolute; inset: 0;\n'
    '  width: 100%; height: 100%;\n'
    '  object-fit: cover; border-radius: 14px;\n'
    '  display: none;\n'
    '}\n'
    '\n'
    '.p2-photo-menu-btn {\n'
    '  position: absolute;\n'
    '  top: 8px; right: 8px;\n'
    '  width: 30px; height: 30px;\n'
    '  border-radius: 50%;\n'
    '  background: rgba(0,0,0,.46);\n'
    '  border: 1.5px solid rgba(255,255,255,.35);\n'
    '  color: #fff; font-size: 16px; line-height: 1;\n'
    '  cursor: pointer;\n'
    '  display: flex; align-items: center; justify-content: center;\n'
    '  z-index: 5;\n'
    '}\n'
    '.p2-photo-menu-btn:active { background: rgba(0,0,0,.7); }'
)

NEW_CSS = (
    '.p2-photo-placeholder {\n'
    '  position: absolute; inset: 0;\n'
    '  display: flex;\n'
    '  flex-direction: column;\n'
    '  align-items: center;\n'
    '  justify-content: center;\n'
    '  gap: 8px;\n'
    '  color: #b0a090;\n'
    '  cursor: pointer;\n'
    '  z-index: 1;\n'
    '}\n'
    '.p2-cam-icon { width: 48px; height: 48px; }\n'
    '\n'
    '.p2-photo-placeholder p { font-size: 11px; font-weight: 600; letter-spacing: .05em; margin: 0; color: #b0a090; }\n'
    '\n'
    '.p2-photo-img {\n'
    '  position: absolute; inset: 0;\n'
    '  width: 100%; height: 100%;\n'
    '  object-fit: cover; border-radius: 14px;\n'
    '  display: none; z-index: 2;\n'
    '}\n'
    '.p2-camera-view {\n'
    '  position: absolute; inset: 0;\n'
    '  display: none; z-index: 2;\n'
    '}\n'
    '.p2-camera-view video {\n'
    '  width: 100%; height: 100%; object-fit: cover; border-radius: 14px; display: block;\n'
    '}\n'
    '.p2-capture-btn {\n'
    '  position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%);\n'
    '  background: rgba(255,255,255,.9); border: 2px solid var(--verde);\n'
    '  color: var(--verde-oscuro); font-family: var(--fnb); font-weight: 700;\n'
    '  font-size: 14px; padding: 8px 28px; border-radius: 24px;\n'
    '  cursor: pointer; pointer-events: auto; z-index: 3;\n'
    '}\n'
    '.p2-retake-btn {\n'
    '  position: absolute; bottom: 8px; right: 8px;\n'
    '  background: rgba(0,0,0,.55); border: 1px solid rgba(255,255,255,.3);\n'
    '  color: #fff; font-family: var(--fnb); font-size: 11px; font-weight: 600;\n'
    '  padding: 5px 10px; border-radius: 12px;\n'
    '  cursor: pointer; display: none; z-index: 3; pointer-events: auto;\n'
    '}\n'
    '.p2-options.locked .p2-option-btn {\n'
    '  opacity: 0.35; cursor: not-allowed; pointer-events: none;\n'
    '}'
)

assert OLD_CSS in html, "ERROR: CSS antiguo no encontrado"
html = html.replace(OLD_CSS, NEW_CSS, 1)
print("OK  Cambio 2a: CSS camara actualizado")

# ─────────────────────────────────────────────
# CAMBIO 2b — HTML photo-wrap
# ─────────────────────────────────────────────
OLD_PHOTO_HTML = (
    '    <div class="p2-photo-wrap">\n'
    '      <div class="p2-photo-placeholder" id="p2-photo-placeholder">\n'
    '        <span id="p2-photo-icon" style="font-size:40px;"></span>\n'
    '        <p>Añade la foto de la planta</p>\n'
    '      </div>\n'
    '      <img class="p2-photo-img" id="p2-photo-img" src="" alt="">\n'
    '      <label class="p2-photo-menu-btn" for="p2-photo-input">⋮</label>\n'
    '      <input type="file" id="p2-photo-input" accept="image/*"\n'
    '             style="position:fixed;top:-999px;left:-999px;width:1px;height:1px;opacity:0;"\n'
    '             onchange="handleP2PhotoUpload(event)">\n'
    '    </div>'
)

NEW_PHOTO_HTML = (
    '    <div class="p2-photo-wrap" id="p2-photo-wrap">\n'
    '      <div class="p2-photo-placeholder" id="p2-photo-placeholder" onclick="openP2Camera()">\n'
    '        <svg class="p2-cam-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>\n'
    '        <p>Busca la planta y fotografíala</p>\n'
    '      </div>\n'
    '      <div class="p2-camera-view" id="p2-camera-view">\n'
    '        <video id="p2-camera-video" autoplay playsinline muted></video>\n'
    '        <button class="p2-capture-btn" onclick="captureP2Photo(event)">Capturar</button>\n'
    '      </div>\n'
    '      <img class="p2-photo-img" id="p2-photo-img" src="" alt="">\n'
    '      <button class="p2-retake-btn" id="p2-retake-btn" onclick="retakeP2Photo(event)">&#8629; Repetir foto</button>\n'
    '    </div>'
)

assert OLD_PHOTO_HTML in html, "ERROR: HTML photo-wrap no encontrado"
html = html.replace(OLD_PHOTO_HTML, NEW_PHOTO_HTML, 1)
print("OK  Cambio 2b: HTML photo-wrap actualizado")

# ─────────────────────────────────────────────
# CAMBIO 3 — JS: reemplazar bloque P2 completo
# ─────────────────────────────────────────────
OLD_JS_START = 'const P2_PLANTS = ['
OLD_JS_END = (
    "function playP2Buzz() {\n"
    "  try {\n"
    "    const ctx = new (window.AudioContext||window.webkitAudioContext)();\n"
    "    const o = ctx.createOscillator(), g = ctx.createGain();\n"
    "    o.connect(g); g.connect(ctx.destination);\n"
    "    o.frequency.value = 140; o.type = 'sawtooth';\n"
    "    g.gain.setValueAtTime(.1, ctx.currentTime);\n"
    "    g.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + .22);\n"
    "    o.start(); o.stop(ctx.currentTime + .22);\n"
    "  } catch(e) {}\n"
    "}"
)

idx_start = html.find(OLD_JS_START)
idx_end   = html.find(OLD_JS_END) + len(OLD_JS_END)
assert idx_start != -1, "ERROR: inicio bloque JS P2 no encontrado"
assert idx_end > len(OLD_JS_END), "ERROR: fin bloque JS P2 no encontrado"
print(f"   Bloque JS P2: chars {idx_start}-{idx_end}")

NEW_JS = (
'const P2_PLANTS = [\n'
'  { id: 0, name: "Romero", icon: "\U0001f33f" },\n'
'  { id: 1, name: "Menta",  icon: "\U0001f331" },\n'
'  { id: 2, name: "Adelfa", icon: "\U0001f338" },\n'
'  { id: 3, name: "Laurel", icon: "\U0001f343" },\n'
'];\n'
'\n'
'const P2_CORRECT_USES = [\n'
'  "Digestivo, estimula la circulaci\xf3n",\n'
'  "Alivia el dolor de cabeza y n\xe1useas",\n'
'  "Planta ornamental con uso medicinal hist\xf3rico muy restringido por su alta toxicidad",\n'
'  "Condimento culinario y digestivo, con uso tradicional antiinflamatorio",\n'
'];\n'
'\n'
'const P2_WRONG_USES_FIXED = [\n'
'  null,\n'
'  null,\n'
'  ["Infusi\xf3n relajante para el dolor de cabeza", "Condimento habitual en la cocina mediterr\xe1nea", "Remedio tradicional para digestiones pesadas"],\n'
'  ["Planta venenosa usada solo con fines ornamentales", "Estimulante card\xedaco en dosis controladas", "Infusi\xf3n calmante para el insomnio"],\n'
'];\n'
'\n'
'const P2_WRONG_USES = [\n'
'  "Baja la fiebre instant\xe1neamente",\n'
'  "Cura fracturas \xf3seas",\n'
'  "Estimula el crecimiento del cabello",\n'
'  "Elimina las caries dentales",\n'
'  "Regenera tejido nervioso da\xf1ado",\n'
'  "Protege frente a la radiaci\xf3n solar",\n'
'];\n'
'\n'
'const P2_SUMMARIES = [\n'
'  { icon:"\U0001f33f", plant:"Romero",  latin:"Rosmarinus officinalis", desc:"Usado desde la antig\xfcedad para estimular la memoria y la circulaci\xf3n." },\n'
'  { icon:"\U0001f331", plant:"Menta",   latin:"Mentha pulegium",        desc:"El mentol que contiene act\xfaa directamente sobre los receptores del dolor." },\n'
'  { icon:"\U0001f338", plant:"Adelfa",  latin:"Nerium oleander",        desc:"Todas sus partes contienen gluc\xf3sidos cardiot\xf3xicos. En la Antig\xfcedad se intent\xf3 usar como tratamiento cardiol\xf3gico, pero sus dosis seguras son pr\xe1cticamente indetectables." },\n'
'  { icon:"\U0001f343", plant:"Laurel",  latin:"Laurus nobilis",         desc:"Sus hojas contienen cineol con efectos digestivos y antiinflamatorios. En la Antigua Roma los h\xe9roes y poetas eran coronados con laurel, s\xedmbolo de excelencia." },\n'
'];\n'
'\n'
'const P2_RIDDLES = [\n'
'  "Me ponen en el guiso para que el est\xf3mago vaya bien, y los deportistas romanos se daban masajes conmigo antes de competir para \'activar la sangre\'. \xbfPara qu\xe9 sirvo?",\n'
'  "Te mareas en el autob\xfas o tienes un dolor de cabeza. Te dan algo de sabor fr\xedo y refrescante que te alivia en minutos. \xbfQu\xe9 propiedad tengo?",\n'
'  "Hermosa y peligrosa. Sus flores adornan jardines mediterr\xe1neos, pero todas sus partes son t\xf3xicas. Hist\xf3ricamente se intent\xf3 usar en medicina, pero nunca de forma segura.",\n'
'  "Sus hojas arom\xe1ticas llevan siglos en las cocinas del mundo. Tambi\xe9n fue s\xedmbolo de gloria en la Antigua Grecia y tiene propiedades digestivas reconocidas.",\n'
'];\n'
'\n'
'const P2_CURIOSITIES = [\n'
'  "Los estudiantes griegos colocaban ramas de romero en la cabeza mientras estudiaban. Estudios modernos confirman que su aroma mejora la concentraci\xf3n y la memoria.",\n'
'  "El mentol enga\xf1a a tus receptores del fr\xedo sin bajar la temperatura real. Por eso la menta \'refresca\': activa los mismos nervios que el fr\xedo, pero sin cambio t\xe9rmico.",\n'
'  "En la Guerra de Independencia espa\xf1ola, soldados franceses usaron ramas de adelfa para asar carne. Varios murieron intoxicados: incluso quemada, libera compuestos t\xf3xicos.",\n'
'  "La palabra \'bachiller\' deriva del lat\xedn \'baccalaureus\', que significa \'coronado con laurel\'. En la Antigua Roma se daban coronas de laurel a los poetas y generales victoriosos.",\n'
'];\n'
'\n'
'let _p2Order = [];\n'
'let _p2CurrentStep = 0;\n'
'let _p2Score = 0;\n'
'let _p2AnswerLocked = false;\n'
'let _p2PhotoTaken = false;\n'
'let _p2CameraStream = null;\n'
'\n'
'function startP2Challenge() {\n'
'  clearCode();\n'
'  loadCIPhoto();\n'
"  go('screen-challenge-intro');\n"
"  setTimeout(() => document.getElementById('c0').focus(), 300);\n"
'}\n'
'\n'
'function initP2Game() {\n'
'  _p2Order = [...Array(P2_PLANTS.length).keys()].sort(() => Math.random() - .5);\n'
'  _p2CurrentStep = 0;\n'
'  _p2Score = 0;\n'
'  _p2AnswerLocked = false;\n'
'  S.timerSec = 0;\n'
'  if (S.timerInt) clearInterval(S.timerInt);\n'
'  S.timerInt = setInterval(() => S.timerSec++, 1000);\n'
'  renderP2Step();\n'
'}\n'
'\n'
'function renderP2Step() {\n'
'  _p2AnswerLocked = false;\n'
'  _p2PhotoTaken = false;\n'
'  closeP2CameraStream();\n'
'\n'
'  const plantIdx = _p2Order[_p2CurrentStep];\n'
'  const plant = P2_PLANTS[plantIdx];\n'
'\n'
"  document.getElementById('p2-progress').textContent = `Planta ${_p2CurrentStep + 1} de ${P2_PLANTS.length}`;\n"
"  document.getElementById('p2-score').textContent = `${_p2Score} pts`;\n"
"  document.getElementById('p2-plant-title').textContent = plant.name;\n"
'\n'
"  const imgEl = document.getElementById('p2-photo-img');\n"
"  const placeholderEl = document.getElementById('p2-photo-placeholder');\n"
"  const cameraView = document.getElementById('p2-camera-view');\n"
"  const retakeBtn = document.getElementById('p2-retake-btn');\n"
"  if (imgEl) { imgEl.src = ''; imgEl.style.display = 'none'; }\n"
"  if (cameraView) cameraView.style.display = 'none';\n"
"  if (retakeBtn) retakeBtn.style.display = 'none';\n"
"  if (placeholderEl) placeholderEl.style.display = 'flex';\n"
'\n'
'  const correctText = P2_CORRECT_USES[plantIdx];\n'
'  let wrongPool;\n'
'  if (P2_WRONG_USES_FIXED[plantIdx]) {\n'
'    wrongPool = P2_WRONG_USES_FIXED[plantIdx].slice();\n'
'  } else {\n'
'    wrongPool = P2_WRONG_USES\n'
'      .concat(P2_CORRECT_USES.filter((_, i) => i !== plantIdx))\n'
'      .sort(() => Math.random() - .5)\n'
'      .slice(0, 3);\n'
'  }\n'
'  const options = [{ text: correctText, correct: true }, ...wrongPool.map(t => ({ text: t, correct: false }))];\n'
'  options.sort(() => Math.random() - .5);\n'
'\n'
"  const container = document.getElementById('p2-options');\n"
"  container.innerHTML = '';\n"
"  container.classList.add('locked');\n"
'  options.forEach(opt => {\n'
"    const btn = document.createElement('button');\n"
"    btn.className = 'p2-option-btn';\n"
'    btn.textContent = opt.text;\n'
'    btn.addEventListener(\'click\', () => handleP2Answer(opt.correct, btn));\n'
'    container.appendChild(btn);\n'
'  });\n'
'}\n'
'\n'
'function openP2Camera() {\n'
'  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {\n'
'    p2CameraUnavailable(); return;\n'
'  }\n'
"  navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } }, audio: false })\n"
'    .then(stream => {\n'
'      _p2CameraStream = stream;\n'
"      const video = document.getElementById('p2-camera-video');\n"
'      video.srcObject = stream;\n'
"      document.getElementById('p2-photo-placeholder').style.display = 'none';\n"
"      document.getElementById('p2-camera-view').style.display = 'block';\n"
'    })\n'
'    .catch(() => { p2CameraUnavailable(); });\n'
'}\n'
'\n'
'function captureP2Photo(e) {\n'
'  if (e) e.stopPropagation();\n'
"  const video = document.getElementById('p2-camera-video');\n"
"  const canvas = document.createElement('canvas');\n"
'  const w = video.videoWidth || 640, h = video.videoHeight || 480;\n'
'  canvas.width = w; canvas.height = h;\n'
'  canvas.getContext(\'2d\').drawImage(video, 0, 0, w, h);\n'
'  closeP2CameraStream();\n'
"  const imgEl = document.getElementById('p2-photo-img');\n"
"  imgEl.src = canvas.toDataURL('image/jpeg', 0.8);\n"
"  imgEl.style.display = 'block';\n"
"  document.getElementById('p2-camera-view').style.display = 'none';\n"
"  document.getElementById('p2-retake-btn').style.display = 'block';\n"
'  _p2PhotoTaken = true;\n'
"  document.getElementById('p2-options').classList.remove('locked');\n"
'}\n'
'\n'
'function retakeP2Photo(e) {\n'
'  if (e) e.stopPropagation();\n'
"  const imgEl = document.getElementById('p2-photo-img');\n"
"  imgEl.src = ''; imgEl.style.display = 'none';\n"
"  document.getElementById('p2-retake-btn').style.display = 'none';\n"
'  _p2PhotoTaken = false;\n'
"  document.getElementById('p2-options').classList.add('locked');\n"
'  openP2Camera();\n'
'}\n'
'\n'
'function closeP2CameraStream() {\n'
'  if (_p2CameraStream) {\n'
'    _p2CameraStream.getTracks().forEach(t => t.stop());\n'
'    _p2CameraStream = null;\n'
'  }\n'
"  const video = document.getElementById('p2-camera-video');\n"
'  if (video) video.srcObject = null;\n'
'}\n'
'\n'
'function p2CameraUnavailable() {\n'
'  toast(\'\U0001f4f7 No se pudo acceder a la c\xe1mara. Puedes continuar sin foto.\');\n'
"  document.getElementById('p2-photo-placeholder').style.display = 'flex';\n"
'  _p2PhotoTaken = true;\n'
"  document.getElementById('p2-options').classList.remove('locked');\n"
'}\n'
'\n'
'function handleP2Answer(isCorrect, btnEl) {\n'
'  if (_p2AnswerLocked) return;\n'
'  _p2AnswerLocked = true;\n'
'  if (isCorrect) {\n'
"    btnEl.classList.add('correct');\n"
'    _p2Score++;\n'
'    playChime();\n'
'    showP2Plus1(btnEl);\n'
'    setTimeout(showP2Feedback, 350);\n'
'  } else {\n'
"    btnEl.classList.add('wrong');\n"
'    playP2Buzz();\n'
'    setTimeout(() => {\n'
"      btnEl.classList.remove('wrong');\n"
'      _p2AnswerLocked = false;\n'
'    }, 460);\n'
'  }\n'
'}\n'
'\n'
'function showP2Plus1(fromEl) {\n'
'  const rect = fromEl.getBoundingClientRect();\n'
"  const el = document.createElement('div');\n"
"  el.className = 'p2-plus1';\n"
"  el.textContent = '+1';\n"
'  el.style.left = (rect.left + rect.width / 2 - 22) + \'px\';\n'
'  el.style.top = (rect.top - 8) + \'px\';\n'
'  document.body.appendChild(el);\n'
'  setTimeout(() => el.remove(), 920);\n'
'}\n'
'\n'
'function showP2Feedback() {\n'
'  const plantIdx = _p2Order[_p2CurrentStep];\n'
'  const sum = P2_SUMMARIES[plantIdx];\n'
"  document.getElementById('p2-feedback-icon').textContent = sum.icon;\n"
"  document.getElementById('p2-feedback-plant').textContent = sum.plant;\n"
"  document.getElementById('p2-feedback-latin').textContent = sum.latin;\n"
"  document.getElementById('p2-feedback-text').textContent = P2_CURIOSITIES[plantIdx];\n"
"  document.getElementById('p2-feedback-overlay').classList.add('open');\n"
'}\n'
'\n'
'function p2NextPlant() {\n'
"  document.getElementById('p2-feedback-overlay').classList.remove('open');\n"
'  _p2CurrentStep++;\n'
'  if (_p2CurrentStep >= P2_PLANTS.length) {\n'
'    setTimeout(completeP2, 300);\n'
'  } else {\n'
'    renderP2Step();\n'
'  }\n'
'}\n'
'\n'
'function showP2HintModal() {\n'
'  const plantIdx = _p2Order[_p2CurrentStep];\n'
'  const plant = P2_PLANTS[plantIdx];\n'
"  document.getElementById('p2-hint-emoji').textContent = plant.icon;\n"
"  document.getElementById('p2-hint-riddle').textContent = P2_RIDDLES[plantIdx];\n"
"  document.getElementById('p2-hint-overlay').classList.add('open');\n"
'}\n'
'\n'
'function closeP2Hint() {\n'
"  document.getElementById('p2-hint-overlay').classList.remove('open');\n"
'}\n'
'\n'
'function completeP2() {\n'
'  closeP2CameraStream();\n'
"  document.getElementById('res-name-el').textContent = 'La Botica Secreta';\n"
'  complete();\n'
'}\n'
'\n'
'function closeP2Game() {\n'
'  closeP2CameraStream();\n'
'  if (S.timerInt) { clearInterval(S.timerInt); S.timerInt = null; }\n'
"  document.getElementById('p2-feedback-overlay').classList.remove('open');\n"
"  go('screen-map');\n"
'}\n'
'\n'
'function playP2Buzz() {\n'
'  try {\n'
'    const ctx = new (window.AudioContext||window.webkitAudioContext)();\n'
'    const o = ctx.createOscillator(), g = ctx.createGain();\n'
'    o.connect(g); g.connect(ctx.destination);\n'
"    o.frequency.value = 140; o.type = 'sawtooth';\n"
'    g.gain.setValueAtTime(.1, ctx.currentTime);\n'
'    g.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + .22);\n'
'    o.start(); o.stop(ctx.currentTime + .22);\n'
'  } catch(e) {}\n'
'}'
)

html = html[:idx_start] + NEW_JS + html[idx_end:]
print("OK  Cambio 3: bloque JS P2 reemplazado")

# ─────────────────────────────────────────────
# Verificacion final
# ─────────────────────────────────────────────
checks = [
    ("Texto intro nuevo",                    "Sabes para qu\xe9 sirve cada una de estas plantas?" in html),
    ("Texto intro viejo eliminado",           "Los monjes bot\xe1nicos" not in html),
    ("Adelfa en datos",                       '"Adelfa"' in html),
    ("Laurel en datos",                       '"Laurel"' in html),
    ("Romero en datos",                       '"Romero"' in html),
    ("Menta en datos",                        '"Menta"' in html),
    ("Lavanda eliminada",                     '"Lavanda"' not in html),
    ("Tomillo eliminado",                     '"Tomillo"' not in html),
    ("Valeriana eliminada",                   '"Valeriana"' not in html),
    ("Aloe vera eliminada",                   '"Aloe vera"' not in html),
    ("Camera icon SVG",                       'p2-cam-icon' in html),
    ("openP2Camera",                          'openP2Camera' in html),
    ("captureP2Photo",                        'captureP2Photo' in html),
    ("retakeP2Photo",                         'retakeP2Photo' in html),
    ("closeP2CameraStream",                   'closeP2CameraStream' in html),
    ("p2CameraUnavailable",                   'p2CameraUnavailable' in html),
    ("locked class en options",               'p2-options.locked' in html),
    ("file input eliminado",                  'p2-photo-input' not in html),
    ("handleP2PhotoUpload eliminado",         'handleP2PhotoUpload' not in html),
    ("Opciones bloqueadas CSS",               'pointer-events: none' in html),
    ("Pista de Adelfa",                       "Hermosa y peligrosa" in html),
    ("Pista de Laurel",                       "s\xedmbolo de gloria" in html),
    ("Opciones incorrectas Adelfa",           "Condimento habitual en la cocina mediterr\xe1nea" in html),
    ("Opciones incorrectas Laurel",           "Estimulante card\xedaco" in html),
    ("Video element camara",                  'p2-camera-video' in html),
    ("Retake button",                         'p2-retake-btn' in html),
    ("Busca la planta texto",                 "Busca la planta y fotografíala" in html),
    ("Planta 1 de 4 logica",                  'P2_PLANTS.length' in html),
    ("Nerium oleander",                       'Nerium oleander' in html),
    ("Laurus nobilis",                        'Laurus nobilis' in html),
]

all_ok = True
for name, ok in checks:
    status = "OK" if ok else "FALLO"
    if not ok: all_ok = False
    print(f"  [{status}] {name}")

print(f"\nResultado: {'TODO OK' if all_ok else 'HAY FALLOS'}")

if all_ok:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Archivo guardado. Tamano final: {len(html):,} chars")
else:
    print("NO se ha guardado el archivo.")
