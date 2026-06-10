"""
Adds two new tutorial cards (tc4 objetivos, tc5 normas) and updates
dot indicators on all existing cards from 4 to 6.
"""
path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ── Helper: 6-dot row with position p lit (0-indexed) ────────
def dots6(lit):
    return '<div class="dots">' + ''.join(
        f'<div class="dot{"  on" if i == lit else ""}"></div>' for i in range(6)
    ).replace('dot  on', 'dot on') + '</div>'

# ── 1. Update dot rows on existing cards (4→6 dots) ──────────
replacements = [
    (  # tc0  (dot 0 on)
        '<div class="dots"><div class="dot on"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>',
        dots6(0)
    ),
    (  # tc1  (dot 1 on)
        '<div class="dots"><div class="dot"></div><div class="dot on"></div><div class="dot"></div><div class="dot"></div></div>',
        dots6(1)
    ),
    (  # tc2  (dot 2 on)
        '<div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot on"></div><div class="dot"></div></div>',
        dots6(2)
    ),
    (  # tc3  (dot 3 on)
        '<div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot on"></div></div>',
        dots6(3)
    ),
]
for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'[dots] updated: {old[:60]}...')
    else:
        errors.append(f'dots not found: {old[:60]}')
        print(f'ERROR: {old[:60]}')

# ── 2. Change tc3 button: startGame → nextCard(3) ─────────────
OLD_BTN = '<button class="btn btn-oscuro" onclick="startGame()">¡Empezar la aventura! 🌱</button>'
NEW_BTN = '<button class="btn btn-verde" onclick="nextCard(3)">Siguiente →</button>'
if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    print('[tc3] button changed to nextCard(3)')
else:
    errors.append('tc3 button not found')
    print('ERROR: tc3 button not found')

# ── 3. Build tc4 and tc5 HTML ─────────────────────────────────
tc4 = f"""  <div class="tcard" id="tc4">
    <div class="tcard-tag">El objetivo</div>
    <h2>¿Quién gana El Último Jardín?</h2>
    <div class="tcard-emoji">🏆</div>
    <p>Gana el equipo que complete la gincana en <strong>menos tiempo</strong>. Para conseguir el Pasaporte del Jardín debes superar las <strong>6 pruebas</strong>: cada una te da puntos.</p>
    <p>Pero no solo las pruebas puntúan — recoger las <strong>páginas perdidas</strong> del jardín también suma. ¡Encuentra toda la historia!</p>
    <div class="tcard-footer">
      {dots6(4)}
      <button class="btn btn-verde" onclick="nextCard(4)">Siguiente →</button>
    </div>
  </div>"""

tc5 = f"""  <div class="tcard" id="tc5">
    <div class="tcard-tag">Normas del jardín</div>
    <h2>Respeta el Jardín Botánico</h2>
    <div class="tcard-emoji">🌿</div>
    <p>Incumplir estas normas supone la <strong>descalificación</strong>:</p>
    <ul style="text-align:left;margin:8px 0 0 0;padding-left:20px;line-height:1.8;font-size:14px;">
      <li>🚶 Camina solo por los <strong>pasillos habilitados</strong></li>
      <li>🚫 No entres en zonas ajardinadas ni parterres</li>
      <li>🌳 Prohibido subirse a los árboles o arrancar cualquier parte de una planta</li>
      <li>✅ Solo podrás recoger partes que se hayan desprendido en los pasillos</li>
    </ul>
    <div class="tcard-footer">
      {dots6(5)}
      <button class="btn btn-oscuro" onclick="startGame()">¡Empezar la aventura! 🌱</button>
    </div>
  </div>"""

# ── 4. Insert tc4+tc5 before the closing </div> of tutorial ───
# The closing tag is after tc3's </div>
CLOSE_MARKER = '  </div>\n</div>\n\n<!-- MAPA -->'
INSERT = f'  </div>\n{tc4}\n{tc5}\n</div>\n\n<!-- MAPA -->'
if CLOSE_MARKER in content:
    content = content.replace(CLOSE_MARKER, INSERT, 1)
    print('[insert] tc4+tc5 inserted before tutorial close')
else:
    errors.append('tutorial close marker not found')
    print('ERROR: tutorial close marker not found')
    # fallback: try to find just the section end
    ALT_MARKER = '  </div>\n</div>\n\n<!-- MAPA'
    if ALT_MARKER in content:
        content = content.replace(ALT_MARKER, f'  </div>\n{tc4}\n{tc5}\n</div>\n\n<!-- MAPA', 1)
        print('[insert] fallback insert succeeded')

if errors:
    print('\nErrors:', errors)
else:
    print('\nAll OK — saving...')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved.')
