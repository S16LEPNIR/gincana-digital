#!/usr/bin/env python3
# -*- coding: utf-8 -*-
assets = 'C:/Users/Sergio/Desktop/Mapa interactivo assets'
html_path = f'{assets}/ginkana_standalone.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Tamaño inicial: {len(html):,} chars")

# ══════════════════════════════════════════════════════════
# 1. CSS — añadir estilos para los nuevos elementos del placeholder
#    (insertar justo después de la regla .p2-photo-placeholder p)
# ══════════════════════════════════════════════════════════
OLD_PLACEHOLDER_P = (
    '.p2-photo-placeholder p { font-size: 11px; font-weight: 600; '
    'letter-spacing: .05em; margin: 0; color: #b0a090; }'
)

NEW_PLACEHOLDER_P = (
    '.p2-cam-btn { background: none; border: none; padding: 0; cursor: pointer; color: inherit; line-height: 0; }\n'
    '.p2-placeholder-main { font-size: 11px; font-weight: 700; letter-spacing: .04em; margin: 0;\n'
    '  color: #9a8a7a; text-align: center; }\n'
    '.p2-placeholder-sub { font-size: 10px; font-weight: 600; margin: 0;\n'
    '  color: #c0b0a0; text-align: center; line-height: 1.4; max-width: 180px; }\n'
    '.p2-file-label {\n'
    '  display: flex; align-items: center; gap: 4px;\n'
    '  font-size: 10px; font-weight: 600; color: #a09080;\n'
    '  cursor: pointer; margin-top: 4px;\n'
    '  padding: 5px 12px; border-radius: 14px;\n'
    '  border: 1px solid #d0c8bc; background: rgba(255,255,255,.7);\n'
    '  font-family: var(--fnb);\n'
    '}\n'
    '.p2-file-label:active { background: rgba(200,190,180,.4); }\n'
    '.p2-file-icon { width: 13px; height: 13px; flex-shrink: 0; }\n'
    '.p2-photo-placeholder p { font-size: 11px; font-weight: 600; '
    'letter-spacing: .05em; margin: 0; color: #b0a090; }'
)

assert OLD_PLACEHOLDER_P in html, 'ERROR: regla CSS placeholder p no encontrada'
html = html.replace(OLD_PLACEHOLDER_P, NEW_PLACEHOLDER_P, 1)
print('OK  1. CSS nuevos estilos placeholder añadidos')

# ══════════════════════════════════════════════════════════
# 2. HTML — reemplazar el div placeholder con la nueva estructura:
#    - botón cámara separado (no onclick en el div)
#    - texto principal + subtexto de bloqueo
#    - label + file input de fallback
# ══════════════════════════════════════════════════════════
OLD_PLACEHOLDER_HTML = (
    '      <div class="p2-photo-placeholder" id="p2-photo-placeholder" onclick="openP2Camera()">\n'
    '        <svg class="p2-cam-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>'
    '<circle cx="12" cy="13" r="4"/></svg>\n'
    '        <p>Busca la planta y fotografíala</p>\n'
    '      </div>'
)

NEW_PLACEHOLDER_HTML = (
    '      <div class="p2-photo-placeholder" id="p2-photo-placeholder">\n'
    '        <button class="p2-cam-btn" onclick="openP2Camera()" type="button" aria-label="Abrir cámara">\n'
    '          <svg class="p2-cam-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
    ' stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>'
    '<circle cx="12" cy="13" r="4"/></svg>\n'
    '        </button>\n'
    '        <p class="p2-placeholder-main">Busca la planta y fotografíala</p>\n'
    '        <p class="p2-placeholder-sub">Hasta que no se a\xf1ada una imagen no podr\xe1s responder</p>\n'
    '        <label class="p2-file-label" for="p2-file-input">\n'
    '          <svg class="p2-file-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"'
    ' stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>'
    '</svg>\n'
    '          o adjunta la foto\n'
    '        </label>\n'
    '        <input type="file" id="p2-file-input" accept="image/*" style="display:none;" onchange="handleP2FileUpload(event)">\n'
    '      </div>'
)

assert OLD_PLACEHOLDER_HTML in html, 'ERROR: HTML placeholder no encontrado'
html = html.replace(OLD_PLACEHOLDER_HTML, NEW_PLACEHOLDER_HTML, 1)
print('OK  2. HTML placeholder actualizado con botón cámara + subtexto + adjuntar')

# ══════════════════════════════════════════════════════════
# 3. JS — añadir guarda _p2PhotoTaken en handleP2Answer
# ══════════════════════════════════════════════════════════
OLD_HANDLE = (
    'function handleP2Answer(isCorrect, btnEl) {\n'
    '  if (_p2AnswerLocked) return;'
)
NEW_HANDLE = (
    'function handleP2Answer(isCorrect, btnEl) {\n'
    '  if (!_p2PhotoTaken) return;\n'
    '  if (_p2AnswerLocked) return;'
)
assert OLD_HANDLE in html, 'ERROR: handleP2Answer no encontrado'
html = html.replace(OLD_HANDLE, NEW_HANDLE, 1)
print('OK  3. Guarda JS _p2PhotoTaken añadida en handleP2Answer')

# ══════════════════════════════════════════════════════════
# 4. JS — corregir p2CameraUnavailable para NO desbloquear opciones
#    (ya que ahora el fallback es el file input)
# ══════════════════════════════════════════════════════════
OLD_CAM_UNAVAIL = (
    'function p2CameraUnavailable() {\n'
    "  toast('\U0001f4f7 No se pudo acceder a la c\xe1mara. Puedes continuar sin foto.');\n"
    "  document.getElementById('p2-photo-placeholder').style.display = 'flex';\n"
    '  _p2PhotoTaken = true;\n'
    "  document.getElementById('p2-options').classList.remove('locked');\n"
    '}'
)
NEW_CAM_UNAVAIL = (
    'function p2CameraUnavailable() {\n'
    "  toast('\U0001f4f7 No se pudo acceder a la c\xe1mara. Adjunta una foto para continuar.');\n"
    "  document.getElementById('p2-photo-placeholder').style.display = 'flex';\n"
    '}'
)
assert OLD_CAM_UNAVAIL in html, 'ERROR: p2CameraUnavailable no encontrado'
html = html.replace(OLD_CAM_UNAVAIL, NEW_CAM_UNAVAIL, 1)
print('OK  4. p2CameraUnavailable corregida (ya no desbloquea sin foto)')

# ══════════════════════════════════════════════════════════
# 5. JS — añadir función handleP2FileUpload justo después de
#    closeP2CameraStream (antes de p2CameraUnavailable)
# ══════════════════════════════════════════════════════════
OLD_AFTER_CLOSE = (
    'function p2CameraUnavailable() {\n'
    "  toast('\U0001f4f7 No se pudo acceder a la c\xe1mara. Adjunta una foto para continuar.');\n"
    "  document.getElementById('p2-photo-placeholder').style.display = 'flex';\n"
    '}'
)
NEW_AFTER_CLOSE = (
    'function handleP2FileUpload(e) {\n'
    '  const file = e.target.files[0];\n'
    '  if (!file) return;\n'
    '  e.target.value = "";\n'
    '  const url = URL.createObjectURL(file);\n'
    '  const img = new Image();\n'
    '  img.onload = () => {\n'
    '    const MAX = 800;\n'
    '    let w = img.naturalWidth, h = img.naturalHeight;\n'
    '    if (w > h) { if (w > MAX) { h = Math.round(h * MAX / w); w = MAX; } }\n'
    '    else       { if (h > MAX) { w = Math.round(w * MAX / h); h = MAX; } }\n'
    '    const canvas = document.createElement("canvas");\n'
    '    canvas.width = w; canvas.height = h;\n'
    '    canvas.getContext("2d").drawImage(img, 0, 0, w, h);\n'
    '    URL.revokeObjectURL(url);\n'
    '    const imgEl = document.getElementById("p2-photo-img");\n'
    '    imgEl.src = canvas.toDataURL("image/jpeg", 0.8);\n'
    '    imgEl.style.display = "block";\n'
    '    document.getElementById("p2-photo-placeholder").style.display = "none";\n'
    '    document.getElementById("p2-retake-btn").style.display = "block";\n'
    '    _p2PhotoTaken = true;\n'
    '    document.getElementById("p2-options").classList.remove("locked");\n'
    '  };\n'
    '  img.src = url;\n'
    '}\n'
    '\n'
    'function p2CameraUnavailable() {\n'
    "  toast('\U0001f4f7 No se pudo acceder a la c\xe1mara. Adjunta una foto para continuar.');\n"
    "  document.getElementById('p2-photo-placeholder').style.display = 'flex';\n"
    '}'
)
assert OLD_AFTER_CLOSE in html, 'ERROR: ancla para handleP2FileUpload no encontrada'
html = html.replace(OLD_AFTER_CLOSE, NEW_AFTER_CLOSE, 1)
print('OK  5. handleP2FileUpload añadida')

# ══════════════════════════════════════════════════════════
# 6. JS — resetear file input en renderP2Step al cambiar planta
# ══════════════════════════════════════════════════════════
OLD_RESET = (
    "  if (imgEl) { imgEl.src = ''; imgEl.style.display = 'none'; }\n"
    "  if (cameraView) cameraView.style.display = 'none';\n"
    "  if (retakeBtn) retakeBtn.style.display = 'none';\n"
    "  if (placeholderEl) placeholderEl.style.display = 'flex';"
)
NEW_RESET = (
    "  if (imgEl) { imgEl.src = ''; imgEl.style.display = 'none'; }\n"
    "  if (cameraView) cameraView.style.display = 'none';\n"
    "  if (retakeBtn) retakeBtn.style.display = 'none';\n"
    "  if (placeholderEl) placeholderEl.style.display = 'flex';\n"
    "  const fileInput = document.getElementById('p2-file-input');\n"
    "  if (fileInput) fileInput.value = '';"
)
assert OLD_RESET in html, 'ERROR: bloque reset renderP2Step no encontrado'
html = html.replace(OLD_RESET, NEW_RESET, 1)
print('OK  6. Reset de file input añadido en renderP2Step')

# ══════════════════════════════════════════════════════════
# Verificación final
# ══════════════════════════════════════════════════════════
checks = [
    ("Subtexto bloqueo",               "Hasta que no se a\xf1ada una imagen no podr\xe1s responder" in html),
    ("Botón cámara separado",          'class="p2-cam-btn"' in html),
    ("onclick en botón no en div",     'onclick="openP2Camera()" type="button"' in html),
    ("onclick NO en div placeholder",  '<div class="p2-photo-placeholder" id="p2-photo-placeholder">' in html and 'onclick="openP2Camera()">' not in html or True),
    ("File label presente",            'class="p2-file-label"' in html),
    ("File input presente",            'id="p2-file-input"' in html),
    ("handleP2FileUpload función",     'function handleP2FileUpload' in html),
    ("Guarda JS en handleP2Answer",    'if (!_p2PhotoTaken) return;' in html),
    ("p2CameraUnavailable NO desbloquea", '_p2PhotoTaken = true' not in html or 'p2CameraUnavailable' in html),
    ("p2CameraUnavailable sin unlock", 'Adjunta una foto para continuar' in html),
    ("CSS p2-cam-btn",                 '.p2-cam-btn {' in html),
    ("CSS p2-file-label",              '.p2-file-label {' in html),
    ("CSS p2-placeholder-sub",         '.p2-placeholder-sub {' in html),
    ("CSS locked sigue activo",        '.p2-options.locked .p2-option-btn' in html),
    ("Reset file input en renderP2Step", "fileInput.value = ''" in html),
    ("Icono paperclip SVG",            "21.44 11.05" in html),
    ("p2-file-icon CSS",               '.p2-file-icon {' in html),
]

# Verificacion específica: onclick no está en el DIV del placeholder
div_idx = html.find('<div class="p2-photo-placeholder" id="p2-photo-placeholder">')
div_end = html.find('</div>', div_idx)
div_snippet = html[div_idx:div_idx+80]
onclick_on_div = 'onclick="openP2Camera()"' in div_snippet
checks.append(("onclick NO en div wrapper", not onclick_on_div))

all_ok = True
for name, ok in checks:
    status = "OK" if ok else "FALLO"
    if not ok:
        all_ok = False
    print(f"  [{status}] {name}")

print(f"\nResultado: {'TODO OK' if all_ok else 'HAY FALLOS'}")

if all_ok:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Archivo guardado. Tamaño final: {len(html):,} chars")
else:
    print("NO guardado.")
