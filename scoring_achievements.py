"""
Full scoring system + achievements for ginkana_standalone.html
Steps:
  1. Update RANKS minScore thresholds
  2. Rewrite calcScore() for 6 tests + pages + speed + witch
  3. Hook witch visit marking in bruChoiceOracle + bruCalcCompat
  4. Call checkAchievements() in complete() and _markInfoPoiVisited()
  5. Add achievement CSS
  6. Add achievement HTML popup
  7. Add achievement JS (ACHIEVEMENTS, checkAchievements, popup, chime)
"""

path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

errors = []

# ──────────────────────────────────────────────────────────
# 1. UPDATE RANKS minScore THRESHOLDS
# ──────────────────────────────────────────────────────────
rank_map = [
    ('minScore:88,', 'minScore:92,'),
    ('minScore:70,', 'minScore:80,'),
    ('minScore:50,', 'minScore:65,'),
    ('minScore:30,', 'minScore:48,'),
    ('minScore:12,', 'minScore:30,'),
]
for old, new in rank_map:
    if old in c:
        c = c.replace(old, new, 1)
        print(f'[1] {old} -> {new}')
    else:
        errors.append(f'rank not found: {old}')

# ──────────────────────────────────────────────────────────
# 2. REWRITE calcScore()
#    Strategy: find unique start and end anchors, replace between them
# ──────────────────────────────────────────────────────────
CALCSCORE_START = 'function calcScore() {'
CALCSCORE_END   = '\nfunction setupCitizenshipStats() {'

NEW_CALCSCORE = '''function calcScore() {
  // A) Pruebas completadas: 8 pts c/u, max 48
  const done       = S.completedTests.filter(Boolean).length;
  const scoreTests = done * 8;

  // B) Paginas descubiertas: 3 pts c/u, max 27 (tope 9 paginas)
  const pages      = Math.min(_visitedInfoPois.size, 9);
  const scorePages = pages * 3;

  // C) Velocidad media de las pruebas completadas: max 20
  const times = S.completionTimes.filter(t => t !== null);
  let scoreSpeed = 0;
  if (times.length) {
    const avg = times.reduce((a, b) => a + b, 0) / times.length;
    if      (avg < 60)  scoreSpeed = 20;
    else if (avg < 120) scoreSpeed = 15;
    else if (avg < 180) scoreSpeed = 10;
    else if (avg < 300) scoreSpeed = 5;
    else                scoreSpeed = 2;
  }

  // D) Bruja consultada: 5 pts
  const scoreWitch = localStorage.getItem('witchVisited') === '1' ? 5 : 0;

  return Math.min(100, scoreTests + scorePages + scoreSpeed + scoreWitch);
}'''

idx_s = c.find(CALCSCORE_START)
idx_e = c.find(CALCSCORE_END)
if idx_s != -1 and idx_e != -1:
    c = c[:idx_s] + NEW_CALCSCORE + c[idx_e:]
    print('[2] calcScore() rewritten')
else:
    errors.append(f'[2] calcScore anchors not found (start={idx_s}, end={idx_e})')

# ──────────────────────────────────────────────────────────
# 3. MARK WITCH VISITED in bruChoiceOracle()
# ──────────────────────────────────────────────────────────
OLD_ORACLE = 'function bruChoiceOracle() {\n  closeBruCinematic();'
NEW_ORACLE = (
    'function bruChoiceOracle() {\n'
    '  closeBruCinematic();\n'
    "  if (!localStorage.getItem('witchVisited')) { localStorage.setItem('witchVisited', '1'); checkAchievements(); }"
)
if OLD_ORACLE in c:
    c = c.replace(OLD_ORACLE, NEW_ORACLE, 1)
    print('[3] witch visited hook in bruChoiceOracle')
else:
    errors.append('[3] bruChoiceOracle not found')

# ──────────────────────────────────────────────────────────
# 4. MARK WITCH VISITED in bruCalcCompat() (after name validation)
# ──────────────────────────────────────────────────────────
OLD_COMPAT = (
    "  if (!a || !b) { alert('Introduce los dos nombres para calcular la compatibilidad.'); return; }\n"
    '  var seed = 0, combined = (a + b).toLowerCase();'
)
NEW_COMPAT = (
    "  if (!a || !b) { alert('Introduce los dos nombres para calcular la compatibilidad.'); return; }\n"
    "  if (!localStorage.getItem('witchVisited')) { localStorage.setItem('witchVisited', '1'); checkAchievements(); }\n"
    '  var seed = 0, combined = (a + b).toLowerCase();'
)
if OLD_COMPAT in c:
    c = c.replace(OLD_COMPAT, NEW_COMPAT, 1)
    print('[4] witch visited hook in bruCalcCompat')
else:
    errors.append('[4] bruCalcCompat seed line not found')

# ──────────────────────────────────────────────────────────
# 5. CALL checkAchievements() in complete() after setting times
# ──────────────────────────────────────────────────────────
OLD_COMPLETE = (
    '  S.completedTests[S.activeTestIndex] = true;\n'
    '  S.completionTimes[S.activeTestIndex] = S.timerSec;\n'
    '  S.sealPending = true;'
)
NEW_COMPLETE = (
    '  S.completedTests[S.activeTestIndex] = true;\n'
    '  S.completionTimes[S.activeTestIndex] = S.timerSec;\n'
    '  checkAchievements();\n'
    '  S.sealPending = true;'
)
if OLD_COMPLETE in c:
    c = c.replace(OLD_COMPLETE, NEW_COMPLETE, 1)
    print('[5] checkAchievements() in complete()')
else:
    errors.append('[5] complete() block not found')

# ──────────────────────────────────────────────────────────
# 6. CALL checkAchievements() in _markInfoPoiVisited()
# ──────────────────────────────────────────────────────────
OLD_MARK = (
    "  try { localStorage.setItem('visitedInfoPois', JSON.stringify([..._visitedInfoPois])); } catch(e) {}\n"
    "  const el = document.getElementById('poi-info-' + k)"
)
NEW_MARK = (
    "  try { localStorage.setItem('visitedInfoPois', JSON.stringify([..._visitedInfoPois])); } catch(e) {}\n"
    "  checkAchievements();\n"
    "  const el = document.getElementById('poi-info-' + k)"
)
if OLD_MARK in c:
    c = c.replace(OLD_MARK, NEW_MARK, 1)
    print('[6] checkAchievements() in _markInfoPoiVisited()')
else:
    errors.append('[6] _markInfoPoiVisited localStorage line not found')

# ──────────────────────────────────────────────────────────
# 7. ACHIEVEMENT CSS — inject before #reset-cin-modal {
# ──────────────────────────────────────────────────────────
ACHIEVEMENT_CSS = '''/* ── LOGROS — Achievement Popup ────────────────── */
#achievement-popup {
  position: fixed;
  top: -120px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9800;
  width: min(320px, 90vw);
  background: rgba(6,22,6,.97);
  border: 1.5px solid rgba(201,168,76,.55);
  border-radius: 16px;
  padding: 12px 16px 12px 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,.75), 0 0 24px rgba(201,168,76,.08);
  display: flex;
  align-items: center;
  gap: 14px;
  transition: top .45s cubic-bezier(.16,1,.3,1);
  pointer-events: none;
  user-select: none;
}
#achievement-popup.show { top: 16px; }
#achievement-popup.hide {
  top: -120px;
  transition: top .38s cubic-bezier(.7,0,.85,.4);
}
#ach-icon-wrap {
  width: 48px; height: 48px; flex-shrink: 0;
  background: rgba(201,168,76,.12);
  border: 1.5px solid rgba(201,168,76,.28);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
}
#ach-text { flex: 1; min-width: 0; }
#ach-label {
  font-family: var(--fnb);
  font-size: 9px; font-weight: 700;
  letter-spacing: 1.8px; text-transform: uppercase;
  color: rgba(201,168,76,.9);
  margin-bottom: 3px;
}
#ach-name {
  font-family: var(--fnb);
  font-size: 15px; font-weight: 700;
  color: rgba(240,232,216,.95);
  line-height: 1.2;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

'''
CSS_ANCHOR = '#reset-cin-modal {'
if CSS_ANCHOR in c:
    c = c.replace(CSS_ANCHOR, ACHIEVEMENT_CSS + CSS_ANCHOR, 1)
    print('[7] Achievement CSS injected')
else:
    errors.append('[7] CSS anchor #reset-cin-modal not found')

# ──────────────────────────────────────────────────────────
# 8. ACHIEVEMENT HTML — inject before game mode code modal
# ──────────────────────────────────────────────────────────
ACHIEVEMENT_HTML = '''<!-- LOGRO POPUP -->
<div id="achievement-popup">
  <div id="ach-icon-wrap"><span id="ach-icon">🌱</span></div>
  <div id="ach-text">
    <div id="ach-label">¡Logro desbloqueado!</div>
    <div id="ach-name">Primer Brote</div>
  </div>
</div>

'''
HTML_ANCHOR = '<!-- MODAL MODO JUEGO'
if HTML_ANCHOR in c:
    c = c.replace(HTML_ANCHOR, ACHIEVEMENT_HTML + HTML_ANCHOR, 1)
    print('[8] Achievement HTML injected')
else:
    errors.append('[8] HTML anchor <!-- MODAL MODO JUEGO not found')

# ──────────────────────────────────────────────────────────
# 9. ACHIEVEMENT JS — inject after setupCitizenshipStats() closing brace
# ──────────────────────────────────────────────────────────
SETUPSTATS_END = (
    "    ? String(Math.floor(avgSec/60)).padStart(2,'0')+':'+String(avgSec%60).padStart(2,'0')\n"
    "    : '--:--';\n"
    "}"
)

ACHIEVEMENT_JS = '''

// ══════════════════════════════════════════════════════════
// SISTEMA DE LOGROS
// ══════════════════════════════════════════════════════════

const ACHIEVEMENTS = [
  { id: 'primer_brote',      icon: '🌱', name: 'Primer Brote',
    check: function() { return S.completedTests.filter(Boolean).length >= 1; } },
  { id: 'raton_biblioteca',  icon: '📖', name: 'Ratón de Biblioteca',
    check: function() { return _visitedInfoPois.size >= 1; } },
  { id: 'cartografo',        icon: '🗺️', name: 'Cartógrafo',
    check: function() { return _visitedInfoPois.size >= 5; } },
  { id: 'archivero',         icon: '📚', name: 'Archivero del Jardín',
    check: function() { return _visitedInfoPois.size >= 9; } },
  { id: 'rayo_vegetal',      icon: '⚡', name: 'Rayo Vegetal',
    check: function() { return S.completionTimes.some(function(t){ return t !== null && t < 60; }); } },
  { id: 'ecuador',           icon: '🧗', name: 'Ecuador',
    check: function() { return S.completedTests.filter(Boolean).length >= 3; } },
  { id: 'credulo',           icon: '🔮', name: 'Crédulo',
    check: function() { return localStorage.getItem('witchVisited') === '1'; } },
  { id: 'pasaporte_sellado', icon: '🏅', name: 'Pasaporte Sellado',
    check: function() { return S.completedTests.filter(Boolean).length >= 6; } },
];

let _unlockedAchievements = new Set(
  JSON.parse(localStorage.getItem('unlockedAchievements') || '[]')
);
let _achQueue = [];
let _achShowing = false;

function checkAchievements() {
  ACHIEVEMENTS.forEach(function(a) {
    if (!_unlockedAchievements.has(a.id) && a.check()) {
      _unlockedAchievements.add(a.id);
      try {
        localStorage.setItem('unlockedAchievements',
          JSON.stringify([..._unlockedAchievements]));
      } catch(e) {}
      _achQueue.push(a);
    }
  });
  if (!_achShowing) _showNextAchievement();
}

function _showNextAchievement() {
  if (_achQueue.length === 0) { _achShowing = false; return; }
  _achShowing = true;
  var a = _achQueue.shift();
  var popup = document.getElementById('achievement-popup');
  if (!popup) { _achShowing = false; _showNextAchievement(); return; }
  document.getElementById('ach-icon').textContent = a.icon;
  document.getElementById('ach-name').textContent = a.name;
  popup.classList.remove('hide');
  void popup.offsetWidth;          // force reflow so transition fires
  popup.classList.add('show');
  _playAchievementChime();
  setTimeout(function() {
    popup.classList.remove('show');
    popup.classList.add('hide');
    setTimeout(function() {
      popup.classList.remove('hide');
      _achShowing = false;
      _showNextAchievement();
    }, 450);
  }, 3500);
}

function _playAchievementChime() {
  try {
    var ctx = new (window.AudioContext || window.webkitAudioContext)();
    // Ascending C major arpeggio: C5 E5 G5 C6
    [523.25, 659.25, 783.99, 1046.5].forEach(function(freq, i) {
      var osc  = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.value = freq;
      var t = ctx.currentTime + i * 0.13;
      gain.gain.setValueAtTime(0, t);
      gain.gain.linearRampToValueAtTime(0.14, t + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.55);
      osc.start(t);
      osc.stop(t + 0.6);
    });
  } catch(e) {}
}'''

if SETUPSTATS_END in c:
    c = c.replace(SETUPSTATS_END, SETUPSTATS_END + ACHIEVEMENT_JS, 1)
    print('[9] Achievement JS injected after setupCitizenshipStats')
else:
    errors.append('[9] setupCitizenshipStats end not found')

# ──────────────────────────────────────────────────────────
# SAVE
# ──────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'\nAll OK — saved. File size: {len(c)//1024} KB')
