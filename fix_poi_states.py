import sys
path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'
with open(path,'r',encoding='utf-8') as f:
    content = f.read()

# 1. CSS: visited state for info POIs
old1 = """.poi.info-poi .poi-pulse {
  background: rgba(40,100,220,0.2);
  box-shadow: 0 0 12px rgba(40,100,220,0.5);
  animation: poiPulseAnim 2.8s infinite ease-in-out;
}
.poi.info-poi .poi-core {
  background: radial-gradient(circle at 35% 35%, #4a90e2, #1a4aa0);
  font-size: 17px;
  font-weight: 700;
}"""
new1 = old1 + """
/* Info POI visitado */
.poi.info-poi.visited .poi-pulse {
  background: rgba(90,138,74,0.15);
  box-shadow: 0 0 10px rgba(90,138,74,0.4);
  animation: none;
}
.poi.info-poi.visited .poi-core {
  background: radial-gradient(circle at 35% 35%, #7aba5a, #2d5a1e);
  font-size: 15px;
  font-weight: 700;
}"""
if old1 in content:
    content = content.replace(old1, new1, 1); print('[1] CSS done')
else:
    print('[1] ERROR css')

# 2. JS: init _visitedInfoPois before S state
old2 = "// Estado global de la gincana (con soporte para calibración y offsets de GPS)\nconst S = {"
new2 = """// Info POIs visitados
const _visitedInfoPois = new Set(
  JSON.parse(localStorage.getItem('visitedInfoPois') || '[]')
);
function _markInfoPoiVisited(key) {
  const k = String(key);
  if (_visitedInfoPois.has(k)) return;
  _visitedInfoPois.add(k);
  try { localStorage.setItem('visitedInfoPois', JSON.stringify([..._visitedInfoPois])); } catch(e) {}
  const el = document.getElementById('poi-info-' + k)
    || (k.startsWith('dyn_') ? document.getElementById('poi-dyn-' + k.replace('dyn_','')) : null);
  if (el) {
    el.classList.add('visited');
    const core = el.querySelector('.poi-core');
    if (core) core.textContent = String.fromCharCode(10003);
  }
}

// Estado global de la gincana (con soporte para calibración y offsets de GPS)
const S = {"""
if old2 in content:
    content = content.replace(old2, new2, 1); print('[2] visitedInfoPois done')
else:
    print('[2] ERROR state')

# 3. Test POI core: always show number
old3 = "      <div class=\"poi-core\">${isCompleted ? '\\u2713' : (test.id + 1)}</div>"
new3 = "      <div class=\"poi-core\">${test.id + 1}</div>"
if old3 in content:
    content = content.replace(old3, new3, 1); print('[3] Test number done')
else:
    # Try alternate encoding
    import re
    m = re.search(r'<div class="poi-core">\$\{isCompleted \? .+? : \(test\.id \+ 1\)\}</div>', content)
    if m:
        content = content[:m.start()] + '      <div class="poi-core">${test.id + 1}</div>' + content[m.end():]
        print('[3] Test number done (regex)')
    else:
        print('[3] ERROR test number')

# 4. Info POI rendering: add visited class
old4 = "    poi.className = 'poi info-poi';\n    poi.id = `poi-info-${ip.id}`;"
new4 = "    const ipVisited = _visitedInfoPois.has(String(ip.id));\n    poi.className = 'poi info-poi' + (ipVisited ? ' visited' : '');\n    poi.id = `poi-info-${ip.id}`;"
if old4 in content:
    content = content.replace(old4, new4, 1); print('[4] Info POI class done')
else:
    print('[4] ERROR info class')

old4b = "      <div class=\"poi-core\">?</div>\n    `;\n    poi.addEventListener('click', (e) => {\n      if (S.isCalibrating) return;\n      if (e.target.closest('.poi-menu-btn') || e.target.closest('.poi-ctx-menu')) return;\n      e.stopPropagation();\n      tryOpenPoi(e.currentTarget, function(){ openInfoPoiModal(ip.id, ip.title, ip.desc); });"
new4b = "      <div class=\"poi-core\">${ipVisited ? '\\u2713' : '?'}</div>\n    `;\n    poi.addEventListener('click', (e) => {\n      if (S.isCalibrating) return;\n      if (e.target.closest('.poi-menu-btn') || e.target.closest('.poi-ctx-menu')) return;\n      e.stopPropagation();\n      tryOpenPoi(e.currentTarget, function(){ openInfoPoiModal(ip.id, ip.title, ip.desc); });"
if old4b in content:
    content = content.replace(old4b, new4b, 1); print('[4b] Info POI icon done')
else:
    print('[4b] ERROR info icon')

# 5. Dynamic POI rendering: add visited class
old5 = "    poi.className = dp.type === 'test' ? 'poi pending' : 'poi info-poi';\n    poi.id = `poi-dyn-${idx}`;"
new5 = "    const dynVisited = dp.type === 'info' && _visitedInfoPois.has('dyn_' + idx);\n    poi.className = dp.type === 'test' ? 'poi pending' : ('poi info-poi' + (dynVisited ? ' visited' : ''));\n    poi.id = `poi-dyn-${idx}`;"
if old5 in content:
    content = content.replace(old5, new5, 1); print('[5] Dyn POI class done')
else:
    print('[5] ERROR dyn class')

old5b = "      <div class=\"poi-core\">?</div>\n    `;\n    poi.addEventListener('click', (e) => {\n      if (S.isCalibrating) return;\n      if (e.target.closest('.poi-menu-btn') || e.target.closest('.poi-ctx-menu')) return;\n      e.stopPropagation();\n      tryOpenPoi(e.currentTarget, function(){ if (dp.type === 'info') openInfoPoiModal('dyn_' + idx"
new5b = "      <div class=\"poi-core\">${dynVisited ? '\\u2713' : '?'}</div>\n    `;\n    poi.addEventListener('click', (e) => {\n      if (S.isCalibrating) return;\n      if (e.target.closest('.poi-menu-btn') || e.target.closest('.poi-ctx-menu')) return;\n      e.stopPropagation();\n      tryOpenPoi(e.currentTarget, function(){ if (dp.type === 'info') openInfoPoiModal('dyn_' + idx"
if old5b in content:
    content = content.replace(old5b, new5b, 1); print('[5b] Dyn POI icon done')
else:
    print('[5b] ERROR dyn icon')

# 6. openInfoPoiModal: mark as visited on open
old6 = "function openInfoPoiModal(poiKey, defaultTitle, defaultDesc) {\n  if (startCinematicIfNeeded()) return; // Primera vez"
new6 = "function openInfoPoiModal(poiKey, defaultTitle, defaultDesc) {\n  if (startCinematicIfNeeded()) return; // Primera vez\n  _markInfoPoiVisited(poiKey);"
if old6 in content:
    content = content.replace(old6, new6, 1); print('[6] openInfoPoiModal done')
else:
    print('[6] ERROR openInfoPoiModal')

with open(path,'w',encoding='utf-8') as f:
    f.write(content)
print('Saved.')
