"""
Fija las posiciones de los puntos de interés azules (info POIs) con
coordenadas limpias hardcodeadas, ignorando localStorage y DATOS_GINCANA.

Fuentes de posición usadas (tomadas del estado actual del app):
  · INFO_POIS_DEFAULT (ip0-ip2): posiciones ajustadas con DATOS_GINCANA override
  · dynamicPois (9 items tipo 'info'): posiciones de DATOS_GINCANA.dynamicPois
"""

path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

errors = []

# ────────────────────────────────────────────────────────────
# 1. Actualizar INFO_POIS_DEFAULT con coordenadas limpias
#    ip1 usa el override de DATOS_GINCANA (x=84.20, y=13.30),
#    que es donde el admin lo posicionó realmente.
# ────────────────────────────────────────────────────────────
OLD_DEFAULTS = """\
const INFO_POIS_DEFAULT = [
  {
    id: 'ip0',
    title: 'Estufa Fría — Invernadero Histórico',
    desc: 'Construida en 1862, la Estufa Fría es uno de los edificios más emblemáticos del jardín. Alberga plantas subtropicales y mediterráneas que necesitan protección durante el invierno. Su estructura de hierro y vidrio es un ejemplo único del patrimonio botánico valenciano.',
    x: 68.60000000000001, y: 55.07484380013968
  },
  {
    id: 'ip1',
    title: 'Jardín de los Olivos Milenarios',
    desc: 'Este rincón acoge ejemplares de Olea europaea de más de 500 años de antigüedad, traídos de las comarcas valencianas. Los olivos monumentales son testimonio vivo del paisaje mediterráneo y del vínculo histórico entre el jardín y el territorio.',
    x: 68.8, y: 49.88013666308021
  },
  {
    id: 'ip2',
    title: 'Estanque de los Nenúfares',
    desc: 'El estanque central está ocupado por Victoria amazonica, el nenúfar gigante del Amazonas, y por diversas especies de Nymphaea. Sus hojas pueden alcanzar más de 1,5 metros de diámetro y son capaces de soportar el peso de un niño. Las flores abren solo durante dos noches consecutivas.',
    x: 84.6, y: 13.39637956094154
  }
];\
"""

NEW_DEFAULTS = """\
const INFO_POIS_DEFAULT = [
  {
    id: 'ip0',
    title: 'Estufa Fría — Invernadero Histórico',
    desc: 'Construida en 1862, la Estufa Fría es uno de los edificios más emblemáticos del jardín. Alberga plantas subtropicales y mediterráneas que necesitan protección durante el invierno. Su estructura de hierro y vidrio es un ejemplo único del patrimonio botánico valenciano.',
    x: 68.60, y: 55.07
  },
  {
    id: 'ip1',
    title: 'Jardín de los Olivos Milenarios',
    desc: 'Este rincón acoge ejemplares de Olea europaea de más de 500 años de antigüedad, traídos de las comarcas valencianas. Los olivos monumentales son testimonio vivo del paisaje mediterráneo y del vínculo histórico entre el jardín y el territorio.',
    x: 84.20, y: 13.30
  },
  {
    id: 'ip2',
    title: 'Estanque de los Nenúfares',
    desc: 'El estanque central está ocupado por Victoria amazonica, el nenúfar gigante del Amazonas, y por diversas especies de Nymphaea. Sus hojas pueden alcanzar más de 1,5 metros de diámetro y son capaces de soportar el peso de un niño. Las flores abren solo durante dos noches consecutivas.',
    x: 84.60, y: 13.40
  }
];\
"""

if OLD_DEFAULTS in c:
    c = c.replace(OLD_DEFAULTS, NEW_DEFAULTS, 1)
    print('[1] INFO_POIS_DEFAULT actualizado con coordenadas limpias')
else:
    errors.append('[1] INFO_POIS_DEFAULT no encontrado exactamente')

# ────────────────────────────────────────────────────────────
# 2. loadInfoPoisPositions() siempre devuelve los defaults,
#    ignorando localStorage y DATOS_GINCANA
# ────────────────────────────────────────────────────────────
OLD_LOAD_INFO = """\
// Cargamos posiciones persistidas de localStorage
function loadInfoPoisPositions() {
  try {
    const lsRaw = localStorage.getItem('infoPoisPositions');
    const positions = (lsRaw ? JSON.parse(lsRaw) : null) || DATOS_GINCANA.infoPoisPositions || {};
    return INFO_POIS_DEFAULT.map(p => ({
      ...p,
      x: positions[p.id] ? positions[p.id].x : p.x,
      y: positions[p.id] ? positions[p.id].y : p.y
    }));
  } catch(e) { return INFO_POIS_DEFAULT.slice(); }
}\
"""

NEW_LOAD_INFO = """\
// Posiciones fijas — siempre usa INFO_POIS_DEFAULT, ignora localStorage
function loadInfoPoisPositions() {
  return INFO_POIS_DEFAULT.slice();
}\
"""

if OLD_LOAD_INFO in c:
    c = c.replace(OLD_LOAD_INFO, NEW_LOAD_INFO, 1)
    print('[2] loadInfoPoisPositions() simplificado a valores fijos')
else:
    errors.append('[2] loadInfoPoisPositions() no encontrada exactamente')

# ────────────────────────────────────────────────────────────
# 3. Añadir constante DYNAMIC_POIS_FIXED_COORDS con las 9
#    posiciones limpias de los dynamic info POIs
#    y aplicarla en loadDynamicPois()
# ────────────────────────────────────────────────────────────

# Posiciones tomadas de DATOS_GINCANA.dynamicPois, redondeadas a 2 dec
FIXED_COORDS = [
    (32.56, 74.31),
    (84.35, 13.72),
    (68.17, 55.21),
    (73.63, 49.95),
    (35.77, 44.27),
    (10.02, 17.43),
    (44.78, 44.32),
    (10.25, 55.98),
    (54.54, 81.23),
]
coords_js = ',\n  '.join(f'{{x:{x}, y:{y}}}' for x, y in FIXED_COORDS)

FIXED_CONST = f"""\
// Posiciones fijas para los POIs dinámicos (no se sobreescriben desde localStorage)
const DYNAMIC_POIS_FIXED_COORDS = [
  {coords_js}
];

"""

OLD_LOAD_DYN = """\
// POIs dinámicos añadidos por el usuario
let _dynamicPois = [];
function loadDynamicPois() {
  try { const lsRaw = localStorage.getItem('dynamicPois'); _dynamicPois = lsRaw !== null ? JSON.parse(lsRaw) : (DATOS_GINCANA.dynamicPois || []); } catch(e) { _dynamicPois = DATOS_GINCANA.dynamicPois || []; }
}\
"""

NEW_LOAD_DYN = f"""\
{FIXED_CONST}// POIs dinámicos añadidos por el usuario
let _dynamicPois = [];
function loadDynamicPois() {{
  try {{ const lsRaw = localStorage.getItem('dynamicPois'); _dynamicPois = lsRaw !== null ? JSON.parse(lsRaw) : (DATOS_GINCANA.dynamicPois || []); }} catch(e) {{ _dynamicPois = DATOS_GINCANA.dynamicPois || []; }}
  // Aplicar posiciones fijas — ignora coordenadas almacenadas
  _dynamicPois.forEach(function(dp, i) {{
    if (DYNAMIC_POIS_FIXED_COORDS[i]) {{
      dp.x = DYNAMIC_POIS_FIXED_COORDS[i].x;
      dp.y = DYNAMIC_POIS_FIXED_COORDS[i].y;
    }}
  }});
}}\
"""

if OLD_LOAD_DYN in c:
    c = c.replace(OLD_LOAD_DYN, NEW_LOAD_DYN, 1)
    print('[3] loadDynamicPois() aplica posiciones fijas')
else:
    errors.append('[3] loadDynamicPois() no encontrada exactamente')

# ────────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:', errors)
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'\nAll OK — guardado. {len(c)//1024} KB')
