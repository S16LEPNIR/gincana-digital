"""
Embeds PASAPORTE.png, PASAPORTE-ABIERTO.png and PRUEBA-1..6.png
as base64 JS constants in ginkana_standalone.html so the file
works on mobile without needing sibling files.
"""
import os, io, base64, json
from PIL import Image

FOLDER   = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
HTML_PATH = os.path.join(FOLDER, 'ginkana_standalone.html')

# ── image specs ──────────────────────────────────────────────
# (filename, max_long_side, jpeg_quality, const_name)
IMAGES = [
    ('PASAPORTE.png',        900, 88, 'IMG_PASAPORTE'),
    ('PASAPORTE-ABIERTO.png',1100, 88, 'IMG_PASAPORTE_ABIERTO'),
    ('PRUEBA-1.png',          700, 85, None),   # will go into PRUEBA_IMGS[1]
    ('PRUEBA-2.png',          700, 85, None),
    ('PRUEBA-3.png',          700, 85, None),
    ('PRUEBA-4.png',          700, 85, None),
    ('PRUEBA-5.png',          700, 85, None),
    ('PRUEBA-6.png',          700, 85, None),
]

def img_to_b64(filename, max_side, quality):
    p = os.path.join(FOLDER, filename)
    with Image.open(p) as img:
        # convert RGBA/P → RGB (needed for JPEG)
        if img.mode in ('RGBA', 'P', 'LA'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        # resize if larger than max_side
        w, h = img.size
        if max(w, h) > max_side:
            scale = max_side / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        data = buf.getvalue()
        print(f'  {filename}: {w}x{h} -> {img.size[0]}x{img.size[1]}, '
              f'{os.path.getsize(p)//1024} KB -> {len(data)//1024} KB')
        return 'data:image/jpeg;base64,' + base64.b64encode(data).decode()

print('Optimizing images...')
encoded = {}
prueba_imgs = ['']   # index 0 unused
for filename, max_side, quality, const in IMAGES:
    b64 = img_to_b64(filename, max_side, quality)
    if const:
        encoded[const] = b64
    else:
        prueba_imgs.append(b64)

# Build JS block
lines = []
lines.append('// ── Imágenes embebidas (base64) ─────────────────────────')
lines.append(f'const IMG_PASAPORTE = {json.dumps(encoded["IMG_PASAPORTE"])};')
lines.append(f'const IMG_PASAPORTE_ABIERTO = {json.dumps(encoded["IMG_PASAPORTE_ABIERTO"])};')
lines.append('const PRUEBA_IMGS = [')
lines.append('  \'\',   // índice 0 no usado')
for i, b64 in enumerate(prueba_imgs[1:], 1):
    comma = ',' if i < len(prueba_imgs) - 1 else ''
    lines.append(f'  {json.dumps(b64)}{comma}  // PRUEBA-{i}.png')
lines.append('];')
js_block = '\n'.join(lines) + '\n\n'

print('\nReading HTML...')
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Inject JS block before // Info POIs visitados ────────
MARKER = '// Info POIs visitados'
if MARKER in content:
    content = content.replace(MARKER, js_block + MARKER, 1)
    print('[1] JS block injected')
else:
    print('[1] ERROR: marker not found')

# ── 2. Replace HTML src for PASAPORTE.png ───────────────────
OLD_PASAPORTE = 'src="PASAPORTE.png"'
NEW_PASAPORTE = 'id="img-pasaporte-tcard" src=""'
if OLD_PASAPORTE in content:
    content = content.replace(OLD_PASAPORTE, NEW_PASAPORTE, 1)
    print('[2] PASAPORTE.png src attribute cleared (will set via JS)')
else:
    print('[2] ERROR: PASAPORTE.png src not found')

# ── 3. Replace HTML src for PASAPORTE-ABIERTO.png ───────────
OLD_ABIERTO = 'src="PASAPORTE-ABIERTO.png"'
NEW_ABIERTO = 'id="img-pasaporte-abierto" src=""'
if OLD_ABIERTO in content:
    content = content.replace(OLD_ABIERTO, NEW_ABIERTO, 1)
    print('[3] PASAPORTE-ABIERTO.png src attribute cleared (will set via JS)')
else:
    print('[3] ERROR: PASAPORTE-ABIERTO.png src not found')

# ── 4. Set the static img srcs via JS on init ────────────────
# We'll inject 2 lines into the DOMContentLoaded / init section.
# The safest injection point is right after the JS block is defined.
# Add a tiny init snippet after the PRUEBA_IMGS const block.
AFTER_BLOCK_MARKER = '];  // PRUEBA_IMGS end — set static srcs on load'
if AFTER_BLOCK_MARKER not in content:
    # Replace the end of the PRUEBA_IMGS block
    OLD_PRUEBA_END = '];\n\n// ── Imágenes embebidas'  # won't match - use different approach
    # Instead, append a self-executing initializer at the end of the JS block
    content = content.replace(
        js_block + MARKER,
        js_block +
        '(function(){\n'
        '  function _setEmbeddedSrcs(){\n'
        '    var e1=document.getElementById("img-pasaporte-tcard"); if(e1) e1.src=IMG_PASAPORTE;\n'
        '    var e2=document.getElementById("img-pasaporte-abierto"); if(e2) e2.src=IMG_PASAPORTE_ABIERTO;\n'
        '  }\n'
        '  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",_setEmbeddedSrcs);\n'
        '  else _setEmbeddedSrcs();\n'
        '})();\n\n' +
        MARKER,
        1
    )
    print('[4] Static src initializer injected')
else:
    print('[4] Already present')

# ── 5. Replace JS dynamic PRUEBA-${test.id+1}.png references ─
OLD_DYN1 = '`<img class="stamp-img" src="PRUEBA-${test.id + 1}.png" alt="${test.name}">`'
NEW_DYN1 = '`<img class="stamp-img" src="${PRUEBA_IMGS[test.id + 1]}" alt="${test.name}">`'
if OLD_DYN1 in content:
    content = content.replace(OLD_DYN1, NEW_DYN1, 1)
    print('[5a] stamp-img dynamic src replaced')
else:
    print('[5a] ERROR: stamp-img src not found')

OLD_DYN2 = '`<img src="PRUEBA-${test.id + 1}.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;display:block;">`'
NEW_DYN2 = '`<img src="${PRUEBA_IMGS[test.id + 1]}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;display:block;">`'
if OLD_DYN2 in content:
    content = content.replace(OLD_DYN2, NEW_DYN2, 1)
    print('[5b] share stamp dynamic src replaced')
else:
    print('[5b] ERROR: share stamp src not found')

print('\nWriting HTML...')
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Done. File size: {os.path.getsize(HTML_PATH)//1024//1024} MB')
