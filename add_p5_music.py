"""
Adds ambient meditation music to Prueba 5.
- Starts when initP5Meditation() is called
- Fades out subtly when complete() detects activeTestIndex === 4
- Also stopped in resetAdventure()
All audio synthesised with Web Audio API (no external files).
"""

path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

errors = []

# ─────────────────────────────────────────────────────────────
# 1. INJECT P5 MUSIC FUNCTIONS (before the P1 section marker)
# ─────────────────────────────────────────────────────────────
P5_MUSIC_JS = r"""
// ── PRUEBA 5 — MÚSICA MEDITACIÓN ─────────────────────────────
let _p5AudioCtx  = null;
let _p5GainNode  = null;
let _p5Oscs      = [];   // [[osc, lfo], ...]
let _p5BellTimer = null;

function startP5Music() {
  stopP5Music();   // limpiar instancia anterior si existe
  try {
    _p5AudioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const now = _p5AudioCtx.currentTime;

    // ── Nodo maestro con fade-in de 4 s ──────────────────────
    _p5GainNode = _p5AudioCtx.createGain();
    _p5GainNode.gain.setValueAtTime(0, now);
    _p5GainNode.gain.linearRampToValueAtTime(0.38, now + 4);
    _p5GainNode.connect(_p5AudioCtx.destination);

    // ── Filtro lowpass para suavidad ─────────────────────────
    const lpf = _p5AudioCtx.createBiquadFilter();
    lpf.type = 'lowpass';
    lpf.frequency.value = 900;
    lpf.Q.value = 0.4;
    lpf.connect(_p5GainNode);

    // ── Capas del drone (A1–A3, ligeramente desafinadas) ─────
    const layers = [
      [55,    'sine',     0.22],   // A1  — bordón profundo
      [110,   'sine',     0.18],   // A2
      [110.4, 'sine',     0.12],   // A2  ligeramente desafinado
      [165,   'sine',     0.08],   // E3  — quinta
      [220,   'triangle', 0.07],   // A3
      [220.6, 'sine',     0.05],   // A3  detuned (calidez)
      [330,   'sine',     0.04],   // E4  — armónico lejano
    ];

    _p5Oscs = layers.map(function([freq, type, amp]) {
      const osc  = _p5AudioCtx.createOscillator();
      const gain = _p5AudioCtx.createGain();
      osc.type = type;
      osc.frequency.value = freq;
      gain.gain.value = amp;

      // LFO muy lento (0.03–0.08 Hz) — simula "respiración"
      const lfo     = _p5AudioCtx.createOscillator();
      const lfoGain = _p5AudioCtx.createGain();
      lfo.type = 'sine';
      lfo.frequency.value = 0.03 + Math.random() * 0.05;
      lfoGain.gain.value  = freq * 0.003;
      lfo.connect(lfoGain);
      lfoGain.connect(osc.frequency);
      lfo.start();

      osc.connect(gain);
      gain.connect(lpf);
      osc.start();
      return [osc, lfo];
    });

    // ── Campanillas esporádicas ──────────────────────────────
    _scheduleP5Bell(4000 + Math.random() * 3000);

  } catch(e) {}
}

function _scheduleP5Bell(delay) {
  if (!_p5AudioCtx) return;
  _p5BellTimer = setTimeout(function() {
    if (!_p5AudioCtx || !_p5GainNode) return;
    // Pentatónica de La: A4 C#5 E5 F#5 A5
    var freqs = [440, 554.37, 659.25, 739.99, 880];
    var freq  = freqs[Math.floor(Math.random() * freqs.length)];
    try {
      var osc  = _p5AudioCtx.createOscillator();
      var gain = _p5AudioCtx.createGain();
      var t    = _p5AudioCtx.currentTime;
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0, t);
      gain.gain.linearRampToValueAtTime(0.09, t + 0.06);  // ataque suave
      gain.gain.exponentialRampToValueAtTime(0.001, t + 5.5); // cola larga
      osc.connect(gain);
      gain.connect(_p5GainNode);
      osc.start(t);
      osc.stop(t + 6);
    } catch(e2) {}
    // Próxima campanilla: 6–13 s
    _scheduleP5Bell(6000 + Math.random() * 7000);
  }, delay);
}

function stopP5Music() {
  if (_p5BellTimer) { clearTimeout(_p5BellTimer); _p5BellTimer = null; }
  _p5Oscs.forEach(function([osc, lfo]) {
    try { osc.stop(); } catch(e) {}
    try { lfo.stop(); } catch(e) {}
  });
  _p5Oscs = [];
  if (_p5AudioCtx) {
    try { _p5AudioCtx.close(); } catch(e) {}
    _p5AudioCtx = null;
  }
  _p5GainNode = null;
}

function fadeOutP5Music() {
  if (!_p5AudioCtx || !_p5GainNode) return;
  // Detener nuevas campanillas
  if (_p5BellTimer) { clearTimeout(_p5BellTimer); _p5BellTimer = null; }
  // Atenuar durante 2.8 s
  var now = _p5AudioCtx.currentTime;
  _p5GainNode.gain.cancelScheduledValues(now);
  _p5GainNode.gain.setValueAtTime(0.38, now);
  _p5GainNode.gain.linearRampToValueAtTime(0, now + 2.8);
  setTimeout(stopP5Music, 3200);
}
// ─────────────────────────────────────────────────────────────

"""

P5_SECTION_MARKER = (
    '// ══════════════════════════════════════════════════════════\n'
    '//  PRUEBA 1'
)
if P5_SECTION_MARKER in c:
    c = c.replace(P5_SECTION_MARKER, P5_MUSIC_JS + P5_SECTION_MARKER, 1)
    print('[1] P5 music functions injected')
else:
    errors.append('[1] P5/P1 boundary marker not found')

# ─────────────────────────────────────────────────────────────
# 2. CALL startP5Music() in initP5Meditation() after timer setup
# ─────────────────────────────────────────────────────────────
OLD_TIMER = (
    '  S.timerSec = 0;\n'
    '  if (S.timerInt) clearInterval(S.timerInt);\n'
    '  S.timerInt = setInterval(() => S.timerSec++, 1000);\n'
    '\n'
    '  const phraseEl = document.getElementById(\'p5-phrase\');'
)
NEW_TIMER = (
    '  S.timerSec = 0;\n'
    '  if (S.timerInt) clearInterval(S.timerInt);\n'
    '  S.timerInt = setInterval(() => S.timerSec++, 1000);\n'
    '  startP5Music();\n'
    '\n'
    '  const phraseEl = document.getElementById(\'p5-phrase\');'
)
if OLD_TIMER in c:
    c = c.replace(OLD_TIMER, NEW_TIMER, 1)
    print('[2] startP5Music() call added in initP5Meditation()')
else:
    errors.append('[2] initP5Meditation timer block not found')

# ─────────────────────────────────────────────────────────────
# 3. CALL fadeOutP5Music() in complete() for P5 only
# ─────────────────────────────────────────────────────────────
OLD_COMPLETE_TOP = (
    'function complete() {\n'
    '  if (S.timerInt) clearInterval(S.timerInt);\n'
    '\n'
    '  const activeTest = getTestById(S.activeTestIndex);'
)
NEW_COMPLETE_TOP = (
    'function complete() {\n'
    '  if (S.timerInt) clearInterval(S.timerInt);\n'
    '  if (S.activeTestIndex === 4) fadeOutP5Music();\n'
    '\n'
    '  const activeTest = getTestById(S.activeTestIndex);'
)
if OLD_COMPLETE_TOP in c:
    c = c.replace(OLD_COMPLETE_TOP, NEW_COMPLETE_TOP, 1)
    print('[3] fadeOutP5Music() call added in complete()')
else:
    errors.append('[3] complete() top not found')

# ─────────────────────────────────────────────────────────────
# 4. CALL stopP5Music() in resetAdventure()
# ─────────────────────────────────────────────────────────────
OLD_RESET = (
    '  if (S.timerInt) { clearInterval(S.timerInt); S.timerInt = null; }\n'
    '  if (_wsHintTimer)'
)
NEW_RESET = (
    '  if (S.timerInt) { clearInterval(S.timerInt); S.timerInt = null; }\n'
    '  stopP5Music();\n'
    '  if (_wsHintTimer)'
)
if OLD_RESET in c:
    c = c.replace(OLD_RESET, NEW_RESET, 1)
    print('[4] stopP5Music() call added in resetAdventure()')
else:
    errors.append('[4] resetAdventure timer block not found')

# ─────────────────────────────────────────────────────────────
if errors:
    print('\nERRORS:', errors)
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'\nAll OK — saved. {len(c)//1024} KB')
