import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. Declarar _unlockedPois justo antes de tryOpenPoi ──────────────────────
OLD_TRY = 'function tryOpenPoi(poiEl, callback) {'
NEW_TRY = 'var _unlockedPois = new Set(); // histéresis de proximidad (sesión)\nfunction tryOpenPoi(poiEl, callback) {'
assert OLD_TRY in html, 'tryOpenPoi declaration not found'
html = html.replace(OLD_TRY, NEW_TRY, 1)
print('1. _unlockedPois Set declarado')

# ── 2. Reemplazar el cuerpo de tryOpenPoi ────────────────────────────────────
OLD_BODY = (
    'function tryOpenPoi(poiEl, callback) {\n'
    '  if (!S.proximityMode) { callback(); return; }\n'
    '  // GPS unavailable or too inaccurate → allow access\n'
    '  if (!S.lastRawGps || S.lastRawGps.accuracy > 50) { callback(); return; }\n'
    '  if (!S.lastGpsPos) { callback(); return; }\n'
    '  var xPct = parseFloat(poiEl.style.left);\n'
    '  var yPct = parseFloat(poiEl.style.top);\n'
    '  if (isNaN(xPct) || isNaN(yPct)) { callback(); return; }\n'
    '  // Posici\xf3n renderizada del jugador (con calibraci\xf3n aplicada, igual que en el mapa)\n'
    '  var px = S.lastGpsPos.x + (S.hasCalibrated ? S.gpsOffset.x : 0);\n'
    '  var py = S.lastGpsPos.y + (S.hasCalibrated ? S.gpsOffset.y : 0);\n'
    '  var playerGps = pctToGps(px, py);\n'
    '  var poiGps    = pctToGps(xPct, yPct);\n'
    '  var dist  = haversineM(playerGps.lat, playerGps.lon, poiGps.lat, poiGps.lon);\n'
    '  var radio = Math.max(15, Math.min(S.lastRawGps.accuracy * 1.2, 30));\n'
    '  if (dist <= radio) {\n'
    '    callback();\n'
    '  } else {\n'
    '    shakePoiEl(poiEl);\n'
    '    toast(\'\\uD83C\\uDF3F Ac\xe9rcate m\xe1s a este punto para poder interactuar con \xe9l\');\n'
    '  }\n'
    '}'
)
NEW_BODY = (
    'function tryOpenPoi(poiEl, callback) {\n'
    '  if (!S.proximityMode) { callback(); return; }\n'
    '  // GPS unavailable or too inaccurate → allow access\n'
    '  if (!S.lastRawGps || S.lastRawGps.accuracy > 50) { callback(); return; }\n'
    '  if (!S.lastGpsPos) { callback(); return; }\n'
    '  var xPct = parseFloat(poiEl.style.left);\n'
    '  var yPct = parseFloat(poiEl.style.top);\n'
    '  if (isNaN(xPct) || isNaN(yPct)) { callback(); return; }\n'
    '  // Posici\xf3n renderizada del jugador (con calibraci\xf3n aplicada, igual que en el mapa)\n'
    '  var px = S.lastGpsPos.x + (S.hasCalibrated ? S.gpsOffset.x : 0);\n'
    '  var py = S.lastGpsPos.y + (S.hasCalibrated ? S.gpsOffset.y : 0);\n'
    '  var playerGps = pctToGps(px, py);\n'
    '  var poiGps    = pctToGps(xPct, yPct);\n'
    '  var dist  = haversineM(playerGps.lat, playerGps.lon, poiGps.lat, poiGps.lon);\n'
    '  var radio = Math.max(20, Math.min(S.lastRawGps.accuracy * 1.2, 35));\n'
    '  // Hist\xe9resis: radio ampliado si el POI ya se desbloqu\xe9 en esta sesi\xf3n\n'
    '  var poiKey = poiEl.id || (poiEl.style.left + \',\' + poiEl.style.top);\n'
    '  if (_unlockedPois.has(poiKey)) radio += 15;\n'
    '  if (dist <= radio) {\n'
    '    _unlockedPois.add(poiKey);\n'
    '    callback();\n'
    '  } else {\n'
    '    shakePoiEl(poiEl);\n'
    '    toast(\'\\uD83C\\uDF3F Ac\xe9rcate m\xe1s a este punto para poder interactuar con \xe9l\');\n'
    '  }\n'
    '}'
)
assert OLD_BODY in html, 'tryOpenPoi body not found'
html = html.replace(OLD_BODY, NEW_BODY)
print('2. tryOpenPoi: radio 20-35, histéresis +15 para POIs ya desbloqueados')

# ── 3. updateProxDebug: actualizar radio y mostrar estado histéresis ──────────
OLD_DEBUG_RADIO = (
    '  var radio = S.lastRawGps\n'
    '    ? Math.max(15, Math.min(S.lastRawGps.accuracy * 1.2, 30)).toFixed(1) + \' m\'\n'
    '    : \'--\';\n'
    '  document.getElementById(\'pd-radio\').textContent = \'Radio tryOpen: \' + radio;'
)
NEW_DEBUG_RADIO = (
    '  var radio = S.lastRawGps\n'
    '    ? Math.max(20, Math.min(S.lastRawGps.accuracy * 1.2, 35)).toFixed(1) + \' m\'\n'
    '    : \'--\';\n'
    '  document.getElementById(\'pd-radio\').textContent = \'Radio tryOpen: \' + radio;'
)
assert OLD_DEBUG_RADIO in html, 'updateProxDebug radio line not found'
html = html.replace(OLD_DEBUG_RADIO, NEW_DEBUG_RADIO)
print('3. updateProxDebug: radio actualizado a 20-35')

# Mostrar indicador de histéresis en el elemento más cercano
OLD_DEBUG_NEAR = (
    '  document.getElementById(\'pd-nearest\').textContent =\n'
    '    \'Cercano: \' + (bestLabel || \'ninguno\');\n'
    '  document.getElementById(\'pd-dist\').textContent =\n'
    '    bestLabel ? \'Dist: \' + bestDist.toFixed(1) + \' m\' : \'Dist: --\';'
)
NEW_DEBUG_NEAR = (
    '  var bestKey = bestLabel ? (document.getElementById(bestLabel) ? bestLabel : null) : null;\n'
    '  var histeresis = bestKey && _unlockedPois.has(bestKey) ? \' [+15 hist]\' : \'\';\n'
    '  document.getElementById(\'pd-nearest\').textContent =\n'
    '    \'Cercano: \' + (bestLabel || \'ninguno\') + histeresis;\n'
    '  document.getElementById(\'pd-dist\').textContent =\n'
    '    bestLabel ? \'Dist: \' + bestDist.toFixed(1) + \' m\' : \'Dist: --\';'
)
assert OLD_DEBUG_NEAR in html, 'updateProxDebug nearest block not found'
html = html.replace(OLD_DEBUG_NEAR, NEW_DEBUG_NEAR)
print('4. updateProxDebug: indicador [+15 hist] para POIs ya desbloqueados')

with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
