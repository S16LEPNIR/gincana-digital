import sys, re
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'
OUT = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'

with open(SRC, 'r', encoding='utf-8') as f:
    content = f.read()

orig_len = len(content)

# ─────────────────────────────────────────────────────────────────
# 1. ADD CSS (before the last </style>)
# ─────────────────────────────────────────────────────────────────
PROX_CSS = """
/* ── MODO PROXIMIDAD ────────────────────────────────────── */
.prox-switch-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px 14px 16px;
  border-top: 1px solid rgba(255,255,255,.10);
  gap: 12px;
}
.prox-switch-left {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  flex: 1;
  min-width: 0;
}
.prox-sw-icon { font-size: 22px; flex-shrink: 0; margin-top: 1px; }
.prox-sw-text { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.prox-sw-title { font-family: var(--fnb); font-size: 13px; font-weight: 700; color: #fff; }
.prox-sw-desc  { font-family: var(--fnb); font-size: 11px; color: rgba(255,255,255,.58); line-height: 1.4; }
.prox-sw-warn  { font-family: var(--fnb); font-size: 10px; color: #ffcc44; line-height: 1.35; margin-top: 2px; }
.prox-toggle-wrap {
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 2px;
  cursor: pointer;
  flex-shrink: 0;
  user-select: none;
  -webkit-user-select: none;
}
.prox-toggle-track {
  position: relative;
  width: 46px;
  height: 26px;
  border-radius: 13px;
  background: #777;
  transition: background .25s;
  flex-shrink: 0;
}
.prox-toggle-track.on { background: #3dba5a; }
.prox-toggle-thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 5px rgba(0,0,0,.30);
  transition: transform .25s;
}
.prox-toggle-track.on .prox-toggle-thumb { transform: translateX(20px); }
.prox-toggle-label {
  font-family: var(--fnb);
  font-size: 10px;
  font-weight: 700;
  color: rgba(255,255,255,.70);
  letter-spacing: .02em;
}
/* proximity dot on POI */
.prox-dot {
  position: absolute;
  bottom: -3px;
  right: -3px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,.9);
  z-index: 5;
  transition: background .4s;
  pointer-events: none;
}
.prox-dot.prox-near    { background: #3dba5a; }
.prox-dot.prox-far     { background: #e84040; }
.prox-dot.prox-unknown { background: #888; }
/* shake */
@keyframes poiShake {
  0%,100%{ transform: translate(-50%,-50%); }
  15%    { transform: translate(calc(-50% - 6px),-50%); }
  30%    { transform: translate(calc(-50% + 6px),-50%); }
  50%    { transform: translate(calc(-50% - 4px),-50%); }
  70%    { transform: translate(calc(-50% + 4px),-50%); }
  85%    { transform: translate(calc(-50% - 2px),-50%); }
}
.poi-shake { animation: poiShake .52s ease-in-out; }
/* ─────────────────────────────────────────────────────────── */
"""

style_close = content.rfind('</style>')
assert style_close != -1, 'No </style> found'
content = content[:style_close] + PROX_CSS + '</style>' + content[style_close+8:]
print('✓ CSS injected')

# ─────────────────────────────────────────────────────────────────
# 2. ADD PROXIMITY SWITCH HTML in backpack menu
# ─────────────────────────────────────────────────────────────────
PROX_SWITCH_ANCHOR = """        </div>
      </button>
    </div>

    <!-- Menú tipo de POI a añadir -->"""

PROX_SWITCH_REPLACEMENT = """        </div>
      </button>
      <!-- MODO PROXIMIDAD -->
      <div class="prox-switch-row">
        <div class="prox-switch-left">
          <span class="prox-sw-icon">📡</span>
          <div class="prox-sw-text">
            <span class="prox-sw-title">Modo Proximidad</span>
            <span class="prox-sw-desc">Solo podrás interactuar con los puntos si estás cerca de ellos.</span>
            <span class="prox-sw-warn" id="prox-gps-warn" style="display:none">⚠️ GPS no disponible o muy impreciso.</span>
          </div>
        </div>
        <div class="prox-toggle-wrap" onclick="toggleProximityMode()">
          <div class="prox-toggle-track" id="prox-toggle-track">
            <div class="prox-toggle-thumb"></div>
          </div>
          <span class="prox-toggle-label" id="prox-toggle-label">OFF</span>
        </div>
      </div>
    </div>

    <!-- Menú tipo de POI a añadir -->"""

assert PROX_SWITCH_ANCHOR in content, 'Backpack menu anchor not found'
content = content.replace(PROX_SWITCH_ANCHOR, PROX_SWITCH_REPLACEMENT, 1)
print('✓ Switch HTML injected')

# ─────────────────────────────────────────────────────────────────
# 3. PATCH S STATE — add proximityMode and lastRawGps
# ─────────────────────────────────────────────────────────────────
S_OLD = '  _relocateMode: false\n};'
S_NEW = '  _relocateMode: false,\n  proximityMode: false,\n  lastRawGps: null\n};'
assert S_OLD in content, 'S state anchor not found'
content = content.replace(S_OLD, S_NEW, 1)
print('✓ S state patched')

# ─────────────────────────────────────────────────────────────────
# 4. PATCH MAP INIT — call loadProximityModeSetting after initGPS
# ─────────────────────────────────────────────────────────────────
INIT_OLD = '  initGPS();\n  initCompass();\n  updateGpsDisplay();\n}'
INIT_NEW = '  initGPS();\n  initCompass();\n  updateGpsDisplay();\n  loadProximityModeSetting();\n}'
assert INIT_OLD in content, 'Map init anchor not found'
content = content.replace(INIT_OLD, INIT_NEW, 1)
print('✓ Map init patched')

# ─────────────────────────────────────────────────────────────────
# 5. PATCH watchPosition — store raw GPS + call proximity updates
# ─────────────────────────────────────────────────────────────────
WP_OLD = """  navigator.geolocation.watchPosition(pos=>{
    const { x: px, y: py } = gpsToPixels(pos.coords.latitude, pos.coords.longitude);
    const xPct = px / 1190 * 100;
    const yPct = py / 1971 * 100;
    S.lastGpsPos = { x: xPct, y: yPct };
    updateGpsDisplay();
  }, () => {
    updateGpsDisplay();
  }, {enableHighAccuracy:true,maximumAge:2000,timeout:10000});"""

WP_NEW = """  navigator.geolocation.watchPosition(pos=>{
    S.lastRawGps = { lat: pos.coords.latitude, lon: pos.coords.longitude, accuracy: pos.coords.accuracy };
    const { x: px, y: py } = gpsToPixels(pos.coords.latitude, pos.coords.longitude);
    const xPct = px / 1190 * 100;
    const yPct = py / 1971 * 100;
    S.lastGpsPos = { x: xPct, y: yPct };
    updateGpsDisplay();
    updateProximityDots();
    updateProxSwitchGpsWarning();
  }, () => {
    S.lastRawGps = null;
    updateGpsDisplay();
    updateProxSwitchGpsWarning();
  }, {enableHighAccuracy:true,maximumAge:2000,timeout:10000});"""

assert WP_OLD in content, 'watchPosition anchor not found'
content = content.replace(WP_OLD, WP_NEW, 1)
print('✓ watchPosition patched')

# ─────────────────────────────────────────────────────────────────
# 6. PATCH POI CLICK HANDLERS — wrap with tryOpenPoi
# ─────────────────────────────────────────────────────────────────

# 6a. Test POI
TEST_OLD = """      e.stopPropagation();
      handlePoiClick(test.id);
    });"""
TEST_NEW = """      e.stopPropagation();
      tryOpenPoi(e.currentTarget, function(){ handlePoiClick(test.id); });
    });"""
assert TEST_OLD in content, 'Test POI click anchor not found'
content = content.replace(TEST_OLD, TEST_NEW, 1)
print('✓ Test POI click patched')

# 6b. Info POI
INFO_OLD = """      e.stopPropagation();
      openInfoPoiModal(ip.id, ip.title, ip.desc);
    });"""
INFO_NEW = """      e.stopPropagation();
      tryOpenPoi(e.currentTarget, function(){ openInfoPoiModal(ip.id, ip.title, ip.desc); });
    });"""
assert INFO_OLD in content, 'Info POI click anchor not found'
content = content.replace(INFO_OLD, INFO_NEW, 1)
print('✓ Info POI click patched')

# 6c. Dynamic POI
DYN_OLD = """      e.stopPropagation();
      if (dp.type === 'info') openInfoPoiModal('dyn_' + idx, 'Punto de interés', 'Punto añadido manualmente.');
    });"""
DYN_NEW = """      e.stopPropagation();
      tryOpenPoi(e.currentTarget, function(){ if (dp.type === 'info') openInfoPoiModal('dyn_' + idx, 'Punto de interés', 'Punto añadido manualmente.'); });
    });"""
assert DYN_OLD in content, 'Dyn POI click anchor not found'
content = content.replace(DYN_OLD, DYN_NEW, 1)
print('✓ Dyn POI click patched')

# 6d. Supervisor POI
SUP_OLD = """      e.stopPropagation();
      handleSupervisorClick();
    });"""
SUP_NEW = """      e.stopPropagation();
      tryOpenPoi(e.currentTarget, function(){ handleSupervisorClick(); });
    });"""
assert SUP_OLD in content, 'Supervisor POI click anchor not found'
content = content.replace(SUP_OLD, SUP_NEW, 1)
print('✓ Supervisor POI click patched')

# 6e. Witch POI
WITCH_OLD = """      e.stopPropagation();
      openWitchCinematic();
    });"""
WITCH_NEW = """      e.stopPropagation();
      tryOpenPoi(e.currentTarget, function(){ openWitchCinematic(); });
    });"""
assert WITCH_OLD in content, 'Witch POI click anchor not found'
content = content.replace(WITCH_OLD, WITCH_NEW, 1)
print('✓ Witch POI click patched')

# ─────────────────────────────────────────────────────────────────
# 7. ADD PROXIMITY JS (before last </script>)
# ─────────────────────────────────────────────────────────────────
PROX_JS = """
// ── MODO PROXIMIDAD ─────────────────────────────────────────────
// Calibration: A = GPS(39.47740,-0.38690) → pixel(479,565)
//              B = GPS(39.47553,-0.38635) → pixel(403,1880)
//              map dims: 1190×1971 px
var _PROX_SCL = (function(){
  var sLon = (403-479)/(-0.38635-(-0.38690));  // px per degree lon
  var sLat = (1880-565)/(39.47553-39.47740);   // px per degree lat (negative)
  return { sLon:sLon, sLat:sLat };
})();

function pctToGps(xPct, yPct) {
  var px = xPct/100*1190;
  var py = yPct/100*1971;
  return {
    lat: 39.47740 + (py-565)/_PROX_SCL.sLat,
    lon: -0.38690 + (px-479)/_PROX_SCL.sLon
  };
}

function haversineM(lat1,lon1,lat2,lon2) {
  var R=6371000, toR=Math.PI/180;
  var dLat=(lat2-lat1)*toR, dLon=(lon2-lon1)*toR;
  var a=Math.sin(dLat/2)*Math.sin(dLat/2)+
        Math.cos(lat1*toR)*Math.cos(lat2*toR)*Math.sin(dLon/2)*Math.sin(dLon/2);
  return R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
}

function tryOpenPoi(poiEl, callback) {
  if (!S.proximityMode) { callback(); return; }
  // GPS unavailable or too inaccurate → allow access
  if (!S.lastRawGps || S.lastRawGps.accuracy > 50) { callback(); return; }
  var xPct = parseFloat(poiEl.style.left);
  var yPct = parseFloat(poiEl.style.top);
  if (isNaN(xPct) || isNaN(yPct)) { callback(); return; }
  var g = pctToGps(xPct, yPct);
  var dist = haversineM(S.lastRawGps.lat, S.lastRawGps.lon, g.lat, g.lon);
  if (dist <= 15) {
    callback();
  } else {
    shakePoiEl(poiEl);
    toast('\\uD83C\\uDF3F Acércate más a este punto para poder interactuar con él');
  }
}

function shakePoiEl(el) {
  el.classList.remove('poi-shake');
  void el.offsetWidth;
  el.classList.add('poi-shake');
  setTimeout(function(){ el.classList.remove('poi-shake'); }, 600);
}

function toggleProximityMode() {
  S.proximityMode = !S.proximityMode;
  localStorage.setItem('proximityMode', S.proximityMode ? '1' : '0');
  _applyProxToggleUI();
  updateProximityDots();
  updateProxSwitchGpsWarning();
}

function loadProximityModeSetting() {
  S.proximityMode = (localStorage.getItem('proximityMode') === '1');
  _applyProxToggleUI();
  updateProximityDots();
  updateProxSwitchGpsWarning();
}

function _applyProxToggleUI() {
  var track = document.getElementById('prox-toggle-track');
  var label = document.getElementById('prox-toggle-label');
  if (track) track.classList.toggle('on', S.proximityMode);
  if (label) label.textContent = S.proximityMode ? 'ON' : 'OFF';
}

function updateProximityDots() {
  var container = document.getElementById('pois-container');
  if (!container) return;
  if (!S.proximityMode) {
    container.querySelectorAll('.prox-dot').forEach(function(d){ d.remove(); });
    return;
  }
  container.querySelectorAll('.poi').forEach(function(poi) {
    var xPct = parseFloat(poi.style.left);
    var yPct = parseFloat(poi.style.top);
    var dot = poi.querySelector('.prox-dot');
    if (!dot) {
      dot = document.createElement('div');
      poi.appendChild(dot);
    }
    if (!S.lastRawGps || S.lastRawGps.accuracy > 50) {
      dot.className = 'prox-dot prox-unknown'; return;
    }
    var g = pctToGps(xPct, yPct);
    var dist = haversineM(S.lastRawGps.lat, S.lastRawGps.lon, g.lat, g.lon);
    dot.className = 'prox-dot ' + (dist <= 15 ? 'prox-near' : 'prox-far');
  });
}

function updateProxSwitchGpsWarning() {
  var warn = document.getElementById('prox-gps-warn');
  if (!warn) return;
  var bad = S.proximityMode && (!S.lastRawGps || S.lastRawGps.accuracy > 50);
  warn.style.display = bad ? 'block' : 'none';
}
// ────────────────────────────────────────────────────────────────
"""

last_script = content.rfind('</script>')
assert last_script != -1, 'No </script> found'
content = content[:last_script] + PROX_JS + '</script>' + content[last_script+9:]
print('✓ Proximity JS injected')

# ─────────────────────────────────────────────────────────────────
# 8. WRITE OUTPUT
# ─────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n✅ Done. {orig_len} → {len(content)} chars (+{len(content)-orig_len})')
