import json, re

HTML_PATH  = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'
JSON_PATH  = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\datos_gincana.json'

print('Reading files...')
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    datos = json.load(f)

json_str = json.dumps(datos, ensure_ascii=False, separators=(',', ':'))
print(f'JSON size: {len(json_str)//1024} KB')

# ─────────────────────────────────────────────────────────
# 1. Inject const DATOS_GINCANA before // Info POIs visitados
# ─────────────────────────────────────────────────────────
INJECT_MARKER = '// Info POIs visitados'
DATOS_BLOCK = f'const DATOS_GINCANA = {json_str};\n\n'
if INJECT_MARKER in content:
    content = content.replace(INJECT_MARKER, DATOS_BLOCK + INJECT_MARKER, 1)
    print('[1] DATOS_GINCANA injected')
else:
    print('[1] ERROR: inject marker not found')

# ─────────────────────────────────────────────────────────
# 2. loadInfoPoisPositions — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old2 = """function loadInfoPoisPositions() {
  try {
    const saved = JSON.parse(localStorage.getItem('infoPoisPositions') || '{}');
    return INFO_POIS_DEFAULT.map(p => ({
      ...p,
      x: saved[p.id] ? saved[p.id].x : p.x,
      y: saved[p.id] ? saved[p.id].y : p.y
    }));
  } catch(e) { return INFO_POIS_DEFAULT.slice(); }
}"""
new2 = """function loadInfoPoisPositions() {
  try {
    const lsRaw = localStorage.getItem('infoPoisPositions');
    const positions = (lsRaw ? JSON.parse(lsRaw) : null) || DATOS_GINCANA.infoPoisPositions || {};
    return INFO_POIS_DEFAULT.map(p => ({
      ...p,
      x: positions[p.id] ? positions[p.id].x : p.x,
      y: positions[p.id] ? positions[p.id].y : p.y
    }));
  } catch(e) { return INFO_POIS_DEFAULT.slice(); }
}"""
if old2 in content:
    content = content.replace(old2, new2, 1); print('[2] loadInfoPoisPositions done')
else:
    print('[2] ERROR loadInfoPoisPositions')

# ─────────────────────────────────────────────────────────
# 3. loadTestPoisPositions — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old3 = """function loadTestPoisPositions() {
  try {
    const saved = JSON.parse(localStorage.getItem('testPoisPositions') || '{}');
    if (Object.keys(saved).length > 0) {
      TESTS.forEach(t => { if (saved[t.id] !== undefined) { t.x = saved[t.id].x; t.y = saved[t.id].y; } });
    }
  } catch(e) {}
}"""
new3 = """function loadTestPoisPositions() {
  try {
    const lsRaw = localStorage.getItem('testPoisPositions');
    const positions = (lsRaw ? JSON.parse(lsRaw) : null) || DATOS_GINCANA.testPoisPositions || {};
    if (Object.keys(positions).length > 0) {
      TESTS.forEach(t => { if (positions[t.id] !== undefined) { t.x = positions[t.id].x; t.y = positions[t.id].y; } });
    }
  } catch(e) {}
}"""
if old3 in content:
    content = content.replace(old3, new3, 1); print('[3] loadTestPoisPositions done')
else:
    print('[3] ERROR loadTestPoisPositions')

# ─────────────────────────────────────────────────────────
# 4. loadDynamicPois — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old4 = "  try { _dynamicPois = JSON.parse(localStorage.getItem('dynamicPois') || '[]'); } catch(e) { _dynamicPois = []; }"
new4 = "  try { const lsRaw = localStorage.getItem('dynamicPois'); _dynamicPois = lsRaw !== null ? JSON.parse(lsRaw) : (DATOS_GINCANA.dynamicPois || []); } catch(e) { _dynamicPois = DATOS_GINCANA.dynamicPois || []; }"
if old4 in content:
    content = content.replace(old4, new4, 1); print('[4] loadDynamicPois done')
else:
    print('[4] ERROR loadDynamicPois')

# ─────────────────────────────────────────────────────────
# 5. loadSupervisorPosition — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old5 = """function loadSupervisorPosition() {
  try {
    const p = JSON.parse(localStorage.getItem('supervisorPos') || 'null');
    if (p && p.x !== undefined) return p;
  } catch(e) {}
  return { x: 46, y: 15 };
}"""
new5 = """function loadSupervisorPosition() {
  try {
    const p = JSON.parse(localStorage.getItem('supervisorPos') || 'null');
    if (p && p.x !== undefined) return p;
  } catch(e) {}
  const ep = DATOS_GINCANA.supervisorPos;
  if (ep && ep.x !== undefined) return ep;
  return { x: 46, y: 15 };
}"""
if old5 in content:
    content = content.replace(old5, new5, 1); print('[5] loadSupervisorPosition done')
else:
    print('[5] ERROR loadSupervisorPosition')

# ─────────────────────────────────────────────────────────
# 6. loadWitchPosition — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old6 = "  try { var p = JSON.parse(localStorage.getItem('witchPos')||'null'); if(p&&p.x!==undefined) return p; } catch(e){}\n  return { x: 62, y: 38 };"
new6 = "  try { var p = JSON.parse(localStorage.getItem('witchPos')||'null'); if(p&&p.x!==undefined) return p; } catch(e){}\n  var ep = DATOS_GINCANA.witchPos; if(ep&&ep.x!==undefined) return ep;\n  return { x: 62, y: 38 };"
if old6 in content:
    content = content.replace(old6, new6, 1); print('[6] loadWitchPosition done')
else:
    print('[6] ERROR loadWitchPosition')

# ─────────────────────────────────────────────────────────
# 7. loadHiddenPois — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old7 = "  try { return JSON.parse(localStorage.getItem('hiddenPois') || '{}'); } catch(e) { return {}; }"
new7 = "  try { const lsRaw = localStorage.getItem('hiddenPois'); return lsRaw !== null ? JSON.parse(lsRaw) : (DATOS_GINCANA.hiddenPois || {}); } catch(e) { return DATOS_GINCANA.hiddenPois || {}; }"
if old7 in content:
    content = content.replace(old7, new7, 1); print('[7] loadHiddenPois done')
else:
    print('[7] ERROR loadHiddenPois')

# ─────────────────────────────────────────────────────────
# 8. getPoiCode — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old8 = """function getPoiCode(type, id) {
  try {
    const saved = JSON.parse(localStorage.getItem('poiCodes') || '{}');
    const key = type + '-' + id;
    if (saved[key] !== undefined) return saved[key];
  } catch(e) {}"""
new8 = """function getPoiCode(type, id) {
  try {
    const lsRaw = localStorage.getItem('poiCodes');
    const saved = (lsRaw ? JSON.parse(lsRaw) : null) || DATOS_GINCANA.poiCodes || {};
    const key = type + '-' + id;
    if (saved[key] !== undefined) return saved[key];
  } catch(e) {}"""
if old8 in content:
    content = content.replace(old8, new8, 1); print('[8] getPoiCode done')
else:
    print('[8] ERROR getPoiCode')

# ─────────────────────────────────────────────────────────
# 9. loadAllPoiCodes — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old9 = """function loadAllPoiCodes() {
  try {
    const saved = JSON.parse(localStorage.getItem('poiCodes') || '{}');
    TESTS.forEach(t => {
      const k = 'test-' + t.id;
      if (saved[k] !== undefined) t.code = saved[k];
    });
    _dynamicPois.forEach((dp, i) => {
      const k = 'dyn-' + i;
      if (saved[k] !== undefined) dp.code = saved[k];"""
new9 = """function loadAllPoiCodes() {
  try {
    const lsRaw = localStorage.getItem('poiCodes');
    const saved = (lsRaw ? JSON.parse(lsRaw) : null) || DATOS_GINCANA.poiCodes || {};
    TESTS.forEach(t => {
      const k = 'test-' + t.id;
      if (saved[k] !== undefined) t.code = saved[k];
    });
    _dynamicPois.forEach((dp, i) => {
      const k = 'dyn-' + i;
      if (saved[k] !== undefined) dp.code = saved[k];"""
if old9 in content:
    content = content.replace(old9, new9, 1); print('[9] loadAllPoiCodes done')
else:
    print('[9] ERROR loadAllPoiCodes')

# ─────────────────────────────────────────────────────────
# 10. _poiConfigs init — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old10 = "  try { return JSON.parse(localStorage.getItem('poiAllConfigs') || '{}') || {}; } catch(e) { return {}; }"
new10 = "  try { const lsRaw = localStorage.getItem('poiAllConfigs'); return (lsRaw ? JSON.parse(lsRaw) : null) || DATOS_GINCANA.poiAllConfigs || {}; } catch(e) { return DATOS_GINCANA.poiAllConfigs || {}; }"
if old10 in content:
    content = content.replace(old10, new10, 1); print('[10] _poiConfigs done')
else:
    print('[10] ERROR _poiConfigs')

# ─────────────────────────────────────────────────────────
# 11. loadCIPhoto — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old11 = """function loadCIPhoto() {
  const saved = localStorage.getItem('testPhoto-' + S.activeTestIndex);
  if (saved) { showCIPhoto(saved); return; }
  // Foto por defecto para Prueba 4
  if (S.activeTestIndex === 3) { showCIPhoto(P4_DEFAULT_PHOTO); return; }
  showCIPhoto('');
}"""
new11 = """function loadCIPhoto() {
  const saved = localStorage.getItem('testPhoto-' + S.activeTestIndex);
  if (saved) { showCIPhoto(saved); return; }
  const embedded = DATOS_GINCANA['testPhoto-' + S.activeTestIndex];
  if (embedded) { showCIPhoto(embedded); return; }
  // Foto por defecto para Prueba 4
  if (S.activeTestIndex === 3) { showCIPhoto(P4_DEFAULT_PHOTO); return; }
  showCIPhoto('');
}"""
if old11 in content:
    content = content.replace(old11, new11, 1); print('[11] loadCIPhoto done')
else:
    print('[11] ERROR loadCIPhoto')

# ─────────────────────────────────────────────────────────
# 12. loadProximityModeSetting — use DATOS_GINCANA as fallback
# ─────────────────────────────────────────────────────────
old12 = """function loadProximityModeSetting() {
  S.proximityMode = (localStorage.getItem('proximityMode') === '1');
  _applyProxToggleUI();
  updateProxSwitchGpsWarning();
}"""
new12 = """function loadProximityModeSetting() {
  const lsVal = localStorage.getItem('proximityMode');
  S.proximityMode = lsVal !== null ? (lsVal === '1') : (DATOS_GINCANA.proximityMode === 1);
  _applyProxToggleUI();
  updateProxSwitchGpsWarning();
}"""
if old12 in content:
    content = content.replace(old12, new12, 1); print('[12] loadProximityModeSetting done')
else:
    print('[12] ERROR loadProximityModeSetting')

# ─────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done. File saved.')
print(f'New file size: {len(content)//1024} KB')
