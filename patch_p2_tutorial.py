import sys, base64, io
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'

# ── Codificar tarjeta planta.png — redimensionada y optimizada ───────────────
img = Image.open(base + '\\tarjeta planta.png').convert('RGBA')
# Reducir a 480px de ancho manteniendo proporciones
w, h = img.size
new_w = 480
new_h = int(h * new_w / w)
img = img.resize((new_w, new_h), Image.LANCZOS)
# Guardar como PNG con compresión máxima (fondo blanco implícito via composición)
bg = Image.new('RGB', img.size, (255, 255, 255))
bg.paste(img, mask=img.split()[3])
buf = io.BytesIO()
bg.save(buf, format='PNG', optimize=True, compress_level=9)
img_b64 = base64.b64encode(buf.getvalue()).decode('ascii')
img_src = f'data:image/png;base64,{img_b64}'
print(f'Imagen codificada: {len(img_b64):,} chars ({len(img_b64)//1333} KB aprox)')

# ── Leer HTML ────────────────────────────────────────────────────────────────
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Eliminar pantalla tutorial previa si existe (para re-aplicar limpio)
import re
html = re.sub(
    r'<!-- PRUEBA 2 — TUTORIAL TARJETA PLANTA -->.*?(?=<!-- PRUEBA 2 — INTRO -->)',
    '',
    html,
    flags=re.DOTALL
)

# ── 1. Insertar pantalla tutorial justo antes de screen-p2-intro ─────────────
TUTORIAL_SCREEN = f'''<!-- PRUEBA 2 — TUTORIAL TARJETA PLANTA -->
<div id="screen-p2-tutorial" class="screen">
  <div class="p1-intro-body" style="gap:14px;padding:24px 20px 32px;">
    <div class="p1-intro-tag" style="background:rgba(90,138,74,.15);color:var(--verde);">Plantas Medicinales · Antes de empezar</div>
    <h2 class="p1-intro-title" style="font-size:20px;">¿Cómo leer la tarjeta de la planta?</h2>
    <div style="width:100%;max-width:300px;border-radius:14px;overflow:hidden;box-shadow:0 4px 22px rgba(0,0,0,.18);">
      <img src="{img_src}" alt="Tarjeta de planta" style="width:100%;display:block;">
    </div>
    <p class="p1-intro-text" style="font-size:15px;text-align:left;max-width:320px;line-height:1.6;">
      Busca la planta por su <strong>nombre común</strong> — es el que aparece en la
      <strong>esquina inferior izquierda</strong> de la tarjeta identificativa
      (marcado como <strong>② Nombre Común</strong> en el diagrama).
      <br><br>
      Una vez la encuentres, recuerda su uso medicinal. ¡Lo necesitarás!
    </p>
    <button class="btn btn-verde" style="width:100%;max-width:340px;" onclick="go('screen-p2-game');initP2Game();">¡Entendido! Comenzar →</button>
  </div>
</div>

'''

ANCHOR = '<!-- PRUEBA 2 — INTRO -->'
assert ANCHOR in html, 'Anchor not found'
html = html.replace(ANCHOR, TUTORIAL_SCREEN + ANCHOR)
print('1. screen-p2-tutorial inserted')

# ── 2. Cambiar flujo en startChallenge si no está ya cambiado ────────────────
OLD_FLOW = '''  // Prueba 2: La Botica Secreta
  if (S.activeTestIndex === 1) {
    go('screen-p2-game');
    initP2Game();
    return;
  }'''

NEW_FLOW = '''  // Prueba 2: La Botica Secreta — muestra tutorial de tarjeta primero
  if (S.activeTestIndex === 1) {
    go('screen-p2-tutorial');
    return;
  }'''

ALREADY_PATCHED = "go('screen-p2-tutorial')"
if ALREADY_PATCHED not in html:
    assert OLD_FLOW in html, 'startChallenge p2 block not found'
    html = html.replace(OLD_FLOW, NEW_FLOW)
    print('2. startChallenge: prueba 2 → screen-p2-tutorial')
else:
    print('2. startChallenge already patched, skipping')

# ── Guardar ──────────────────────────────────────────────────────────────────
with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done - file saved')
