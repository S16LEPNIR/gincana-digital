"""
Aplica las actualizaciones al ginkana_standalone.html:
- Códigos de 4 dígitos → 3 dígitos
- Nuevos códigos para cada prueba
- Fotos por defecto en la pantalla de código para cada prueba
- Textos actualizados
"""
import base64
import io
import os
import re
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
SRC  = os.path.join(BASE, 'ginkana_standalone.html')
DST  = os.path.join(BASE, 'ginkana_standalone.html')
BAK  = os.path.join(BASE, 'ginkana_standalone_backup_3digit.html')

# ── Imagen → base64 data-URI, recortada a 9:16 ──────────────────────────────
def image_to_b64(filename, target_w=540, target_h=960):
    path = os.path.join(BASE, filename)
    img  = Image.open(path).convert('RGB')
    w, h = img.size

    # Calcular recorte para 9:16
    target_ratio = target_w / target_h   # 0.5625
    current_ratio = w / h
    if current_ratio > target_ratio:
        # Demasiado ancha: recortar lados
        new_w = int(h * target_ratio)
        left  = (w - new_w) // 2
        img   = img.crop((left, 0, left + new_w, h))
    elif current_ratio < target_ratio:
        # Demasiado alta: recortar arriba/abajo (centrado)
        new_h = int(w / target_ratio)
        top   = (h - new_h) // 2
        img   = img.crop((0, top, w, top + new_h))

    img = img.resize((target_w, target_h), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=82, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return f'data:image/jpeg;base64,{b64}'

print('Procesando imágenes...')
photos = {
    0: image_to_b64('Imágen planta prueba 1.jpeg'),
    1: image_to_b64('Foto inicio prueba 2.jpg'),
    2: image_to_b64('foto inicio umbraculo.jpg'),
    4: image_to_b64('Foto incio prueba 5.jpeg'),
    5: image_to_b64('Foto incio prueba 6.jpeg'),
}
print('  ✓ 5 imágenes procesadas')

# ── Leer HTML ────────────────────────────────────────────────────────────────
print('Leyendo HTML...')
with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ── Backup ───────────────────────────────────────────────────────────────────
with open(BAK, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'  ✓ Backup en {BAK}')

# ── 1. Cambiar codes en el array TESTS ──────────────────────────────────────
CODES = {0: '081', 1: '042', 2: '615', 3: '391', 4: '893', 5: '241'}

# El array tiene bloques separados por líneas enormes de base64.
# Sustituimos las 6 ocurrencias de code:"1111" en orden.
count = [0]
def replace_code(m):
    idx = count[0]
    count[0] += 1
    return f'code: "{CODES[idx]}"'

html = re.sub(r'code:\s*"1111"', replace_code, html)
assert count[0] == 6, f'Se esperaban 6 sustituciones de código, se hicieron {count[0]}'
print(f'  ✓ Códigos actualizados: {CODES}')

# ── 2. Cambiar hints de "4 dígitos" a "3 dígitos" en TESTS ──────────────────
html = html.replace(
    'Necesitarás los primeros 4 dígitos para iniciar la prueba.',
    'Necesitarás los primeros 3 dígitos para iniciar la prueba.'
)
html = html.replace(
    'Necesitarás los primeros 4 dígitos para iniciar la prueba.',
    'Necesitarás los primeros 3 dígitos para iniciar la prueba.'
)

# ── 3. Texto de tutorial ─────────────────────────────────────────────────────
html = html.replace(
    'introduce los 4 primeros dígitos de su número de referencia',
    'introduce los 3 primeros dígitos de su número de referencia'
)

# ── 4. fp-hint-text ──────────────────────────────────────────────────────────
html = html.replace(
    'Necesitarás los primeros 4 dígitos para iniciar la prueba.',
    'Necesitarás los primeros 3 dígitos para iniciar la prueba.'
)

# Limpiar cualquier variante restante
html = html.replace('primeros 4 dígitos', 'primeros 3 dígitos')
html = html.replace('los 4 primeros dígitos', 'los 3 primeros dígitos')
print('  ✓ Textos de ayuda actualizados')

# ── 5. Casilla de código: eliminar el 4.º input (c3) ────────────────────────
OLD_INPUTS = (
    '        <input class="code-box" id="c0" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(0)" onkeydown="ck(event,0)">\n'
    '        <input class="code-box" id="c1" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(1)" onkeydown="ck(event,1)">\n'
    '        <input class="code-box" id="c2" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(2)" onkeydown="ck(event,2)">\n'
    '        <input class="code-box" id="c3" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(3)" onkeydown="ck(event,3)">'
)
NEW_INPUTS = (
    '        <input class="code-box" id="c0" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(0)" onkeydown="ck(event,0)">\n'
    '        <input class="code-box" id="c1" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(1)" onkeydown="ck(event,1)">\n'
    '        <input class="code-box" id="c2" maxlength="1" type="text" inputmode="numeric" autocomplete="off" oninput="ci(2)" onkeydown="ck(event,2)">'
)
assert OLD_INPUTS in html, 'No se encontró el bloque de 4 inputs'
html = html.replace(OLD_INPUTS, NEW_INPUTS)
print('  ✓ Input box c3 eliminado')

# ── 6. Actualizar función ci() ───────────────────────────────────────────────
OLD_CI = (
    '// CÓDIGO INPUT LOGIC — auto-envío al rellenar el 4º dígito\n'
    'function ci(i) {\n'
    '  const el = document.getElementById(\'c\' + i);\n'
    '  const v = el.value.replace(/\\D/g,\'\').slice(-1);\n'
    '  el.value = v; el.classList.toggle(\'filled\', !!v);\n'
    '  document.getElementById(\'code-err\').classList.remove(\'show\');\n'
    '  if (v && i < 3) {\n'
    '    document.getElementById(\'c\' + (i+1)).focus();\n'
    '  } else if (v && i === 3) {\n'
    '    // Último dígito — iniciar automáticamente\n'
    '    const allFilled = [0,1,2,3].every(j => document.getElementById(\'c\'+j).value);\n'
    '    if (allFilled) setTimeout(startChallenge, 250);\n'
    '  }\n'
    '}'
)
NEW_CI = (
    '// CÓDIGO INPUT LOGIC — auto-envío al rellenar el 3er dígito\n'
    'function ci(i) {\n'
    '  const el = document.getElementById(\'c\' + i);\n'
    '  const v = el.value.replace(/\\D/g,\'\').slice(-1);\n'
    '  el.value = v; el.classList.toggle(\'filled\', !!v);\n'
    '  document.getElementById(\'code-err\').classList.remove(\'show\');\n'
    '  if (v && i < 2) {\n'
    '    document.getElementById(\'c\' + (i+1)).focus();\n'
    '  } else if (v && i === 2) {\n'
    '    // Último dígito — iniciar automáticamente\n'
    '    const allFilled = [0,1,2].every(j => document.getElementById(\'c\'+j).value);\n'
    '    if (allFilled) setTimeout(startChallenge, 250);\n'
    '  }\n'
    '}'
)
assert OLD_CI in html, 'No se encontró la función ci()'
html = html.replace(OLD_CI, NEW_CI)
print('  ✓ Función ci() actualizada')

# ── 7. Actualizar función clearCode() ───────────────────────────────────────
OLD_CLEAR = (
    'function clearCode() {\n'
    '  [0,1,2,3].forEach(i => {\n'
    '    const el = document.getElementById(\'c\'+i);\n'
    '    el.value = \'\'; el.classList.remove(\'filled\'); el.style.borderColor = \'\';\n'
    '  });\n'
    '  document.getElementById(\'code-err\').classList.remove(\'show\');\n'
    '}'
)
NEW_CLEAR = (
    'function clearCode() {\n'
    '  [0,1,2].forEach(i => {\n'
    '    const el = document.getElementById(\'c\'+i);\n'
    '    el.value = \'\'; el.classList.remove(\'filled\'); el.style.borderColor = \'\';\n'
    '  });\n'
    '  document.getElementById(\'code-err\').classList.remove(\'show\');\n'
    '}'
)
assert OLD_CLEAR in html, 'No se encontró la función clearCode()'
html = html.replace(OLD_CLEAR, NEW_CLEAR)
print('  ✓ Función clearCode() actualizada')

# ── 8. Actualizar función startChallenge() ───────────────────────────────────
OLD_SC = (
    'function startChallenge() {\n'
    '  const v = [0,1,2,3].map(i => document.getElementById(\'c\'+i).value).join(\'\');\n'
    '  const activeTest = getTestById(S.activeTestIndex);\n'
    '  if (!activeTest) return;\n'
    '\n'
    '  if (v !== activeTest.code) {\n'
    '    document.getElementById(\'code-err\').classList.add(\'show\');\n'
    '    [0,1,2,3].forEach(i => {\n'
    '      const el = document.getElementById(\'c\'+i);\n'
    '      el.style.borderColor = \'var(--rojo)\';\n'
    '      setTimeout(() => el.style.borderColor = \'\', 1000);\n'
    '    });\n'
    '    return;\n'
    '  }'
)
NEW_SC = (
    'function startChallenge() {\n'
    '  const v = [0,1,2].map(i => document.getElementById(\'c\'+i).value).join(\'\');\n'
    '  const activeTest = getTestById(S.activeTestIndex);\n'
    '  if (!activeTest) return;\n'
    '\n'
    '  if (v !== activeTest.code) {\n'
    '    document.getElementById(\'code-err\').classList.add(\'show\');\n'
    '    [0,1,2].forEach(i => {\n'
    '      const el = document.getElementById(\'c\'+i);\n'
    '      el.style.borderColor = \'var(--rojo)\';\n'
    '      setTimeout(() => el.style.borderColor = \'\', 1000);\n'
    '    });\n'
    '    return;\n'
    '  }'
)
assert OLD_SC in html, 'No se encontró la función startChallenge()'
html = html.replace(OLD_SC, NEW_SC)
print('  ✓ Función startChallenge() actualizada')

# ── 9. Actualizar loadCIPhoto() para todas las pruebas ───────────────────────
OLD_LOAD = (
    'function loadCIPhoto() {\n'
    '  const saved = localStorage.getItem(\'testPhoto-\' + S.activeTestIndex);\n'
    '  if (saved) { showCIPhoto(saved); return; }\n'
    '  const embedded = DATOS_GINCANA[\'testPhoto-\' + S.activeTestIndex];\n'
    '  if (embedded) { showCIPhoto(embedded); return; }\n'
    '  // Foto por defecto para Prueba 4\n'
    '  if (S.activeTestIndex === 3) { showCIPhoto(P4_DEFAULT_PHOTO); return; }\n'
    '  showCIPhoto(\'\');\n'
    '}'
)
NEW_LOAD = (
    'function loadCIPhoto() {\n'
    '  const saved = localStorage.getItem(\'testPhoto-\' + S.activeTestIndex);\n'
    '  if (saved) { showCIPhoto(saved); return; }\n'
    '  const embedded = DATOS_GINCANA[\'testPhoto-\' + S.activeTestIndex];\n'
    '  if (embedded) { showCIPhoto(embedded); return; }\n'
    '  // Fotos por defecto para cada prueba\n'
    '  const defaults = [P1_DEFAULT_PHOTO, P2_DEFAULT_PHOTO, P3_DEFAULT_PHOTO, P4_DEFAULT_PHOTO, P5_DEFAULT_PHOTO, P6_DEFAULT_PHOTO];\n'
    '  if (defaults[S.activeTestIndex]) { showCIPhoto(defaults[S.activeTestIndex]); return; }\n'
    '  showCIPhoto(\'\');\n'
    '}'
)
assert OLD_LOAD in html, 'No se encontró la función loadCIPhoto()'
html = html.replace(OLD_LOAD, NEW_LOAD)
print('  ✓ Función loadCIPhoto() actualizada')

# ── 10. Insertar constantes de fotos por defecto justo antes de P4_DEFAULT_PHOTO ──
P4_MARKER = 'const P4_DEFAULT_PHOTO = "data:image/jpeg;base64,'
assert P4_MARKER in html, 'No se encontró P4_DEFAULT_PHOTO'

NEW_PHOTO_CONSTS = (
    f'const P1_DEFAULT_PHOTO = "{photos[0]}";\n'
    f'const P2_DEFAULT_PHOTO = "{photos[1]}";\n'
    f'const P3_DEFAULT_PHOTO = "{photos[2]}";\n'
    f'const P5_DEFAULT_PHOTO = "{photos[4]}";\n'
    f'const P6_DEFAULT_PHOTO = "{photos[5]}";\n'
)
html = html.replace(P4_MARKER, NEW_PHOTO_CONSTS + P4_MARKER)
print('  ✓ Constantes de fotos por defecto añadidas')

# ── 11. Actualizar el comentario de la función ci ────────────────────────────
# Ya se hizo arriba al reemplazar OLD_CI

# ── Escribir resultado ───────────────────────────────────────────────────────
print('Escribiendo HTML modificado...')
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'\n✅ ¡Listo! Archivo guardado: {DST}')
print(f'   Backup en: {BAK}')
