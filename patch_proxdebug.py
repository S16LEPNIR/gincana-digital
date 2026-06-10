import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. HTML overlay — antes de </body> ───────────────────────────────────────
OVERLAY_HTML = '''<!-- DEBUG PROXIMIDAD — oculto por defecto, triple-tap en brújula -->
<div id="prox-debug" style="display:none;position:fixed;top:10px;left:10px;z-index:99999;background:rgba(0,0,0,.78);color:#fff;font-size:11px;font-family:monospace;padding:8px 11px;border-radius:9px;line-height:1.75;pointer-events:none;max-width:230px;">
  <div id="pd-gps">GPS: --</div>
  <div id="pd-radio">Radio: --</div>
  <div id="pd-nearest">Cercano: --</div>
  <div id="pd-dist">Dist: --</div>
</div>

'''
BODY_CLOSE = '</body>'
assert BODY_CLOSE in html
html = html.replace(BODY_CLOSE, OVERLAY_HTML + BODY_CLOSE)
print('1. HTML overlay insertado')

# ── 2. JS — updateProxDebug() + triple-tap — antes de </script> final ────────
DEBUG_JS = '''
// ── OVERLAY DEBUG PROXIMIDAD ──────────────────────────────────────────────
function updateProxDebug() {
  var ov = document.getElementById('prox-debug');
  if (!ov || ov.style.display === 'none') return;

  var acc = S.lastRawGps ? S.lastRawGps.accuracy.toFixed(1) + ' m' : '--';
  document.getElementById('pd-gps').textContent   = 'GPS accuracy: ' + acc;

  var radio = S.lastRawGps
    ? Math.max(15, Math.min(S.lastRawGps.accuracy * 1.2, 30)).toFixed(1) + ' m'
    : '--';
  document.getElementById('pd-radio').textContent = 'Radio tryOpen: ' + radio;

  if (!S.lastGpsPos || !S.lastRawGps) {
    document.getElementById('pd-nearest').textContent = 'Cercano: sin GPS';
    document.getElementById('pd-dist').textContent    = 'Dist: --';
    return;
  }

  // Misma lógica que tryOpenPoi: posición calibrada del jugador
  var px = S.lastGpsPos.x + (S.hasCalibrated ? S.gpsOffset.x : 0);
  var py = S.lastGpsPos.y + (S.hasCalibrated ? S.gpsOffset.y : 0);
  var playerGps = pctToGps(px, py);

  // Iterar todos los .poi visibles en el mapa
  var bestLabel = null, bestDist = Infinity;
  document.querySelectorAll('.poi').forEach(function(el) {
    var xPct = parseFloat(el.style.left);
    var yPct = parseFloat(el.style.top);
    if (isNaN(xPct) || isNaN(yPct)) return;
    var poiGps = pctToGps(xPct, yPct);
    var d = haversineM(playerGps.lat, playerGps.lon, poiGps.lat, poiGps.lon);
    if (d < bestDist) {
      bestDist = d;
      bestLabel = el.id || (el.className.split(' ').slice(1).join(' ') || '?');
    }
  });

  document.getElementById('pd-nearest').textContent =
    'Cercano: ' + (bestLabel || 'ninguno');
  document.getElementById('pd-dist').textContent =
    bestLabel ? 'Dist: ' + bestDist.toFixed(1) + ' m' : 'Dist: --';
}

// Triple-tap en #compass-base activa/desactiva el overlay
(function() {
  var _taps = [];
  var el = document.getElementById('compass-base');
  if (!el) return;
  el.addEventListener('click', function() {
    var now = Date.now();
    _taps = _taps.filter(function(t) { return now - t < 600; });
    _taps.push(now);
    if (_taps.length >= 3) {
      _taps = [];
      var ov = document.getElementById('prox-debug');
      if (ov) ov.style.display = ov.style.display === 'none' ? 'block' : 'none';
    }
  });
})();
// ─────────────────────────────────────────────────────────────────────────────
'''

SCRIPT_CLOSE = '// ────────────────────────────────────────────────────────────────\n</script>'
assert SCRIPT_CLOSE in html, 'script close anchor not found'
html = html.replace(SCRIPT_CLOSE, '// ────────────────────────────────────────────────────────────────\n' + DEBUG_JS + '</script>')
print('2. updateProxDebug() y triple-tap insertados')

# ── 3. Llamada a updateProxDebug() en el callback GPS ────────────────────────
OLD_GPS = (
    '    S.lastGpsPos = { x: xPct, y: yPct };\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
)
NEW_GPS = (
    '    S.lastGpsPos = { x: xPct, y: yPct };\n'
    '    updateGpsDisplay();\n'
    '    updateProxSwitchGpsWarning();\n'
    '    updateProxDebug();\n'
)
assert OLD_GPS in html, 'GPS callback block not found'
html = html.replace(OLD_GPS, NEW_GPS)
print('3. updateProxDebug() enganchado al callback GPS')

# ── Guardar ───────────────────────────────────────────────────────────────────
with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
