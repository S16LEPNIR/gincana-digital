import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

OLD = (
    'function tryOpenPoi(poiEl, callback) {\n'
    '  if (!S.proximityMode) { callback(); return; }\n'
    '  // GPS unavailable or too inaccurate → allow access\n'
    '  if (!S.lastRawGps || S.lastRawGps.accuracy > 50) { callback(); return; }\n'
    '  var xPct = parseFloat(poiEl.style.left);\n'
    '  var yPct = parseFloat(poiEl.style.top);\n'
    '  if (isNaN(xPct) || isNaN(yPct)) { callback(); return; }\n'
    '  var g = pctToGps(xPct, yPct);\n'
    '  var dist = haversineM(S.lastRawGps.lat, S.lastRawGps.lon, g.lat, g.lon);\n'
    '  if (dist <= 15) {\n'
    '    callback();\n'
    '  } else {\n'
    '    shakePoiEl(poiEl);\n'
    '    toast(\'\\uD83C\\uDF3F Ac\xe9rcate m\xe1s a este punto para poder interactuar con \xe9l\');\n'
    '  }\n'
    '}'
)

NEW = (
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

assert OLD in html, 'tryOpenPoi not found'
html = html.replace(OLD, NEW)

with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK')
