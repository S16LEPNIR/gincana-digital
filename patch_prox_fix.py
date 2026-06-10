import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 — tryOpenPoi: eliminar bypasses que permiten acceso sin restricción
# ─────────────────────────────────────────────────────────────────────────────
OLD_TRY = (
    'var _unlockedPois = new Set(); // hist\xe9resis de proximidad (sesi\xf3n)\n'
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
NEW_TRY = (
    'var _unlockedPois = new Set(); // hist\xe9resis de proximidad (sesi\xf3n)\n'
    'function tryOpenPoi(poiEl, callback) {\n'
    '  if (!S.proximityMode) { callback(); return; }\n'
    '  // Sin hardware GPS: no se puede comprobar proximidad\n'
    '  if (!navigator.geolocation) { callback(); return; }\n'
    '  // Sin posici\xf3n todav\xeda: bloquear hasta que el GPS funcione\n'
    '  if (!S.lastGpsPos) {\n'
    '    toast(\'📍 Esperando se\xf1al GPS… Aseg\xfarate de que el GPS est\xe1 activado.\');\n'
    '    return;\n'
    '  }\n'
    '  var xPct = parseFloat(poiEl.style.left);\n'
    '  var yPct = parseFloat(poiEl.style.top);\n'
    '  if (isNaN(xPct) || isNaN(yPct)) { callback(); return; }\n'
    '  // Posici\xf3n renderizada del jugador (con calibraci\xf3n aplicada, igual que en el mapa)\n'
    '  var px = S.lastGpsPos.x + (S.hasCalibrated ? S.gpsOffset.x : 0);\n'
    '  var py = S.lastGpsPos.y + (S.hasCalibrated ? S.gpsOffset.y : 0);\n'
    '  var playerGps = pctToGps(px, py);\n'
    '  var poiGps    = pctToGps(xPct, yPct);\n'
    '  var dist  = haversineM(playerGps.lat, playerGps.lon, poiGps.lat, poiGps.lon);\n'
    '  var acc   = S.lastRawGps ? S.lastRawGps.accuracy : 25;\n'
    '  var radio = Math.max(20, Math.min(acc * 1.2, 35));\n'
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
assert OLD_TRY in html, 'tryOpenPoi block not found'
html = html.replace(OLD_TRY, NEW_TRY)
print('1. tryOpenPoi: bypasses de accuracy y null eliminados')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2 — initGPS: subir umbral de filtrado de 40 m a 60 m
# ─────────────────────────────────────────────────────────────────────────────
OLD_FILTER = (
    '    if (pos.coords.accuracy > 40) { updateGpsDisplay(); updateProxSwitchGpsWarning(); updateProxDebug(); return; }'
)
NEW_FILTER = (
    '    if (pos.coords.accuracy > 60) { updateGpsDisplay(); updateProxSwitchGpsWarning(); updateProxDebug(); return; }'
)
assert OLD_FILTER in html, 'initGPS accuracy filter line not found'
html = html.replace(OLD_FILTER, NEW_FILTER)
print('2. initGPS: umbral de filtrado 40 m → 60 m')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3 — initGPS error callback: añadir updateProxDebug()
# ─────────────────────────────────────────────────────────────────────────────
OLD_ERR = (
    '  }, () => {\n'
    '    S.lastRawGps = null;\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '  }, {enableHighAccuracy:true,maximumAge:2000,timeout:10000});'
)
NEW_ERR = (
    '  }, () => {\n'
    '    S.lastRawGps = null;\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '    updateProxDebug();\n'
    '  }, {enableHighAccuracy:true,maximumAge:2000,timeout:10000});'
)
assert OLD_ERR in html, 'initGPS error callback not found'
html = html.replace(OLD_ERR, NEW_ERR)
print('3. initGPS: error callback ahora llama updateProxDebug()')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4 — Triple-tap: llamar updateProxDebug() al abrir el panel
# ─────────────────────────────────────────────────────────────────────────────
OLD_TAP = (
    '    if (_taps.length >= 3) {\n'
    '      _taps = [];\n'
    '      var ov = document.getElementById(\'prox-debug\');\n'
    '      if (ov) ov.style.display = ov.style.display === \'none\' ? \'block\' : \'none\';\n'
    '    }'
)
NEW_TAP = (
    '    if (_taps.length >= 3) {\n'
    '      _taps = [];\n'
    '      var ov = document.getElementById(\'prox-debug\');\n'
    '      if (ov) {\n'
    '        ov.style.display = ov.style.display === \'none\' ? \'block\' : \'none\';\n'
    '        if (ov.style.display === \'block\') updateProxDebug();\n'
    '      }\n'
    '    }'
)
assert OLD_TAP in html, 'triple-tap block not found'
html = html.replace(OLD_TAP, NEW_TAP)
print('4. Triple-tap: llama updateProxDebug() al abrir el panel')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5 — updateProxSwitchGpsWarning: usar lastGpsPos como criterio real
# ─────────────────────────────────────────────────────────────────────────────
OLD_WARN = (
    '  var bad = S.proximityMode && (!S.lastRawGps || S.lastRawGps.accuracy > 50);'
)
NEW_WARN = (
    '  var bad = S.proximityMode && !S.lastGpsPos;'
)
assert OLD_WARN in html, 'updateProxSwitchGpsWarning bad line not found'
html = html.replace(OLD_WARN, NEW_WARN)
print('5. updateProxSwitchGpsWarning: criterio cambiado a !lastGpsPos')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6 — updateProxDebug: añadir línea de estado GPS
# ─────────────────────────────────────────────────────────────────────────────
OLD_DEBUG_ACC = (
    '  var acc = S.lastRawGps ? S.lastRawGps.accuracy.toFixed(1) + \' m\' : \'--\';\n'
    '  document.getElementById(\'pd-gps\').textContent   = \'GPS accuracy: \' + acc;'
)
NEW_DEBUG_ACC = (
    '  var acc = S.lastRawGps ? S.lastRawGps.accuracy.toFixed(1) + \' m\' : \'sin se\xf1al\';\n'
    '  var posOk = S.lastGpsPos ? \' ✔\' : \' (sin pos)\xf3n)\';\n'
    '  document.getElementById(\'pd-gps\').textContent   = \'GPS: \' + acc + posOk;'
)
assert OLD_DEBUG_ACC in html, 'updateProxDebug acc line not found'
html = html.replace(OLD_DEBUG_ACC, NEW_DEBUG_ACC)
print('6. updateProxDebug: l\xednea GPS muestra estado de sesi\xf3n')

with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\nDone — 6 fixes applied')
