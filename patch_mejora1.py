import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. Estado S: añadir smoothGps: null ──────────────────────────────────────
OLD_S = '  lastRawGps: null\n};'
NEW_S = '  lastRawGps: null,\n  smoothGps: null\n};'
assert OLD_S in html, 'state S end not found'
html = html.replace(OLD_S, NEW_S)
print('1. smoothGps: null añadido al estado S')

# ── 2. initGPS: filtrado + suavizado exponencial ─────────────────────────────
OLD_GPS = (
    '  navigator.geolocation.watchPosition(pos=>{\n'
    '    S.lastRawGps = { lat: pos.coords.latitude, lon: pos.coords.longitude, accuracy: pos.coords.accuracy };\n'
    '    const { x: px, y: py } = gpsToPixels(pos.coords.latitude, pos.coords.longitude);\n'
    '    const xPct = px / 1190 * 100;\n'
    '    const yPct = py / 1971 * 100;\n'
    '    S.lastGpsPos = { x: xPct, y: yPct };\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '    updateProxDebug();\n'
    '  }, () => {\n'
    '    S.lastRawGps = null;\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '  }, {enableHighAccuracy:true,maximumAge:2000,timeout:10000});\n'
)
NEW_GPS = (
    '  navigator.geolocation.watchPosition(pos=>{\n'
    '    S.lastRawGps = { lat: pos.coords.latitude, lon: pos.coords.longitude, accuracy: pos.coords.accuracy };\n'
    '    // Descarta lecturas con accuracy > 40 m — conserva la última buena\n'
    '    if (pos.coords.accuracy > 40) { updateGpsDisplay(); updateProxSwitchGpsWarning(); updateProxDebug(); return; }\n'
    '    // Suavizado exponencial: k según precisión\n'
    '    var k = pos.coords.accuracy <= 10 ? 0.4 : pos.coords.accuracy <= 25 ? 0.25 : 0.15;\n'
    '    if (!S.smoothGps) {\n'
    '      S.smoothGps = { lat: pos.coords.latitude, lon: pos.coords.longitude };\n'
    '    } else {\n'
    '      S.smoothGps.lat += (pos.coords.latitude  - S.smoothGps.lat) * k;\n'
    '      S.smoothGps.lon += (pos.coords.longitude - S.smoothGps.lon) * k;\n'
    '    }\n'
    '    const { x: px, y: py } = gpsToPixels(S.smoothGps.lat, S.smoothGps.lon);\n'
    '    const xPct = px / 1190 * 100;\n'
    '    const yPct = py / 1971 * 100;\n'
    '    S.lastGpsPos = { x: xPct, y: yPct };\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '    updateProxDebug();\n'
    '  }, () => {\n'
    '    S.lastRawGps = null;\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '  }, {enableHighAccuracy:true,maximumAge:2000,timeout:10000});\n'
)
assert OLD_GPS in html, 'initGPS watchPosition block not found'
html = html.replace(OLD_GPS, NEW_GPS)
print('2. initGPS: filtrado accuracy>40 y suavizado exponencial aplicados')

# ── 3. resetAdventure: limpiar smoothGps ─────────────────────────────────────
OLD_RESET = '  S.ginkanaStartTime   = null;\n  S.firstTimePassport = true;'
NEW_RESET = '  S.ginkanaStartTime   = null;\n  S.smoothGps          = null;\n  S.firstTimePassport = true;'
assert OLD_RESET in html, 'resetAdventure block not found'
html = html.replace(OLD_RESET, NEW_RESET)
print('3. resetAdventure: S.smoothGps = null añadido')

with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
