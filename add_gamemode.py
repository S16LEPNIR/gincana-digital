"""
Implementa modo juego:
- Quita "Mi Pasaporte" y "Escáner de plantas" del menú mochila
- Añade botón "Modo juego" con código 314
- Oculta poi-menu-btn, poi-ctx-menu, #add-poi-btn y #add-poi-menu en modo juego
- Persiste estado en localStorage
"""
path = r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

errors = []

# ── 1. CSS: .mi-gamemode + game-mode hiding rules + modals ───
OLD_CSS = '.mi-reset-cin { background: linear-gradient(135deg, #7a4acc, #3a1a7a); }'
NEW_CSS = '''.mi-reset-cin { background: linear-gradient(135deg, #7a4acc, #3a1a7a); }
.mi-gamemode  { background: linear-gradient(135deg, #1a4a6a, #0a2040); }

/* Modo juego: ocultar herramientas de edición */
body.game-mode .poi-menu-btn,
body.game-mode .poi-ctx-menu,
body.game-mode #add-poi-btn,
body.game-mode #add-poi-menu { display: none !important; }

/* Indicador visual en botón modo juego cuando está activo */
.mi-gamemode.active { background: linear-gradient(135deg, #2a7a2a, #0f3d0f); }

/* Modales modo juego */
#gamemode-code-modal,
#gamemode-confirm-modal {
  position: fixed; inset: 0; z-index: 9600;
  background: rgba(0,0,0,.75);
  display: none; align-items: center; justify-content: center;
  padding: 24px; backdrop-filter: blur(4px);
}
#gamemode-code-modal.open,
#gamemode-confirm-modal.open { display: flex; animation: fadeIn .18s ease both; }
.gm-modal-box {
  background: rgba(8,17,8,.97);
  border: 1.5px solid rgba(201,168,76,.35);
  border-radius: 22px;
  padding: 28px 24px 22px;
  max-width: 300px; width: 100%;
  box-shadow: 0 20px 60px rgba(0,0,0,.8);
  display: flex; flex-direction: column; align-items: center; gap: 14px;
  text-align: center;
}
.gm-modal-icon { font-size: 38px; }
.gm-modal-title {
  font-family: var(--fnb); font-size: 16px; font-weight: 700;
  color: rgba(240,232,216,.95); line-height: 1.3;
}
.gm-modal-desc {
  font-family: var(--fnb); font-size: 13px;
  color: rgba(240,232,216,.55); line-height: 1.5;
}
#gm-code-input {
  width: 100%; text-align: center; font-size: 22px; letter-spacing: 8px;
  font-family: monospace; padding: 10px 0; background: rgba(255,255,255,.07);
  border: 1.5px solid rgba(201,168,76,.3); border-radius: 10px;
  color: rgba(240,232,216,.9); outline: none;
}
.gm-modal-btns { display: flex; gap: 10px; width: 100%; }
.gm-modal-btns .btn { flex: 1; padding: 12px 0; font-size: 14px; }'''

if OLD_CSS in c:
    c = c.replace(OLD_CSS, NEW_CSS, 1); print('[1] CSS added')
else:
    errors.append('[1] CSS marker not found')

# ── 2. Remove "Mi Pasaporte" button ─────────────────────────
OLD_PASS = '''      <button class="menu-item" onclick="openFromBackpack('passport')">
        <div class="mi-icon mi-passport">
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none">
            <rect x="3" y="2" width="14" height="17" rx="2" stroke="white" stroke-width="1.5"/>
            <line x1="3" y1="7" x2="17" y2="7" stroke="white" stroke-width="1.1"/>
            <circle cx="10" cy="13.5" r="2.2" stroke="white" stroke-width="1.3"/>
            <line x1="7" y1="4.5" x2="13" y2="4.5" stroke="white" stroke-width="1.1"/>
          </svg>
        </div>
        <div class="mi-label">
          <span class="mi-name">Mi Pasaporte</span>
          <span class="mi-desc">Sellos y progreso</span>
        </div>
      </button>'''
if OLD_PASS in c:
    c = c.replace(OLD_PASS, '', 1); print('[2] Mi Pasaporte removed')
else:
    errors.append('[2] Mi Pasaporte not found')

# ── 3. Remove "Escáner de plantas" button ───────────────────
OLD_SCAN = '''      <button class="menu-item" onclick="openFromBackpack('scanner')">
        <div class="mi-icon mi-scanner">
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none">
            <path d="M10 16V10" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M10 10C10 10 6.5 10 5 7" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
            <path d="M10 10C10 10 13.5 10 15 7" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
            <path d="M7.5 4L10 7L12.5 4" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M7 16h6" stroke="white" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="mi-label">
          <span class="mi-name">Escáner de plantas</span>
          <span class="mi-desc">Introducir código de placa</span>
        </div>
      </button>'''
if OLD_SCAN in c:
    c = c.replace(OLD_SCAN, '', 1); print('[3] Escáner de plantas removed')
else:
    errors.append('[3] Escáner not found')

# ── 4. Add "Modo juego" button after reset-cin button ────────
OLD_RESET_BTN = '''      <button class="menu-item" onclick="showResetCinConfirm()">
        <div class="mi-icon mi-reset-cin">
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none">
            <path d="M10 4.5A5.5 5.5 0 1 1 5.1 7.5" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            <polyline points="4,4.5 5.1,7.5 8,6.2" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="mi-label">
          <span class="mi-name">Reiniciar cinemáticas</span>
          <span class="mi-desc">Volver a ver las intro de una vez</span>
        </div>
      </button>'''
NEW_RESET_BTN = OLD_RESET_BTN + '''
      <button class="menu-item" id="gamemode-bp-btn" onclick="openGameModeModal()">
        <div class="mi-icon mi-gamemode" id="gamemode-bp-icon">
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none">
            <rect x="2" y="6" width="16" height="9" rx="3" stroke="white" stroke-width="1.4"/>
            <line x1="5" y1="10.5" x2="7" y2="10.5" stroke="white" stroke-width="1.3" stroke-linecap="round"/>
            <line x1="6" y1="9.5" x2="6" y2="11.5" stroke="white" stroke-width="1.3" stroke-linecap="round"/>
            <circle cx="13" cy="9.5" r=".9" fill="white"/>
            <circle cx="15" cy="11.2" r=".9" fill="white"/>
          </svg>
        </div>
        <div class="mi-label">
          <span class="mi-name" id="gamemode-bp-label">Modo juego</span>
          <span class="mi-desc" id="gamemode-bp-desc">Activar modo para jugadores</span>
        </div>
      </button>'''
if OLD_RESET_BTN in c:
    c = c.replace(OLD_RESET_BTN, NEW_RESET_BTN, 1); print('[4] Modo juego button added')
else:
    errors.append('[4] Reset cin button not found')

# ── 5. Add modal HTML before </body> ─────────────────────────
OLD_BODY_END = '<div id="reset-cin-modal">'
NEW_BODY_END = '''<!-- MODAL MODO JUEGO — código -->
<div id="gamemode-code-modal">
  <div class="gm-modal-box">
    <div class="gm-modal-icon" id="gm-code-icon">🎮</div>
    <div class="gm-modal-title" id="gm-code-title">Modo juego</div>
    <div class="gm-modal-desc" id="gm-code-desc">Introduce el código de 3 dígitos</div>
    <input type="text" id="gm-code-input" inputmode="numeric" maxlength="3"
           placeholder="···" autocomplete="off" oninput="this.value=this.value.replace(/\\D/g,'')"
           onkeydown="if(event.key==='Enter')submitGameModeCode()">
    <div class="gm-modal-btns">
      <button class="btn btn-gris" onclick="closeGameModeCodeModal()">Cancelar</button>
      <button class="btn btn-dorado" onclick="submitGameModeCode()">Confirmar</button>
    </div>
  </div>
</div>

<!-- MODAL MODO JUEGO — confirmación -->
<div id="gamemode-confirm-modal">
  <div class="gm-modal-box">
    <div class="gm-modal-icon" id="gm-confirm-icon">🎮</div>
    <div class="gm-modal-title" id="gm-confirm-title">Modo juego</div>
    <div class="gm-modal-desc" id="gm-confirm-desc"></div>
    <div class="gm-modal-btns">
      <button class="btn btn-gris" onclick="cancelGameModeConfirm()">Cancelar</button>
      <button class="btn btn-dorado" onclick="applyGameMode()">Aceptar</button>
    </div>
  </div>
</div>

<div id="reset-cin-modal">'''
if OLD_BODY_END in c:
    c = c.replace(OLD_BODY_END, NEW_BODY_END, 1); print('[5] Modal HTML added')
else:
    errors.append('[5] reset-cin-modal marker not found')

# ── 6. Add JS after mochila section ─────────────────────────
OLD_JS = 'function openPlantScanner() {'
NEW_JS = '''// ── MODO JUEGO ─────────────────────────────────────────────
let _gameModeActive = localStorage.getItem('gameMode') === '1';

function _applyGameModeUI() {
  if (_gameModeActive) {
    document.body.classList.add('game-mode');
  } else {
    document.body.classList.remove('game-mode');
  }
  var icon = document.getElementById('gamemode-bp-icon');
  var label = document.getElementById('gamemode-bp-label');
  var desc  = document.getElementById('gamemode-bp-desc');
  if (icon)  icon.classList.toggle('active', _gameModeActive);
  if (label) label.textContent = _gameModeActive ? 'Modo juego (ON)' : 'Modo juego';
  if (desc)  desc.textContent  = _gameModeActive ? 'Activo · toca para desactivar' : 'Activar modo para jugadores';
}

function openGameModeModal() {
  closeBackpackMenu();
  var inp = document.getElementById('gm-code-input');
  if (inp) inp.value = '';
  document.getElementById('gm-code-icon').textContent  = _gameModeActive ? '🛠️' : '🎮';
  document.getElementById('gm-code-title').textContent = _gameModeActive ? 'Modo edición' : 'Modo juego';
  document.getElementById('gm-code-desc').textContent  = _gameModeActive
    ? 'Introduce el código para volver al modo edición'
    : 'Introduce el código para activar el modo juego';
  document.getElementById('gamemode-code-modal').classList.add('open');
  setTimeout(function(){ var i=document.getElementById('gm-code-input'); if(i) i.focus(); }, 200);
}

function closeGameModeCodeModal() {
  document.getElementById('gamemode-code-modal').classList.remove('open');
}

function submitGameModeCode() {
  var val = document.getElementById('gm-code-input').value;
  if (val !== '314') { toast('Código incorrecto'); return; }
  closeGameModeCodeModal();
  if (_gameModeActive) {
    document.getElementById('gm-confirm-icon').textContent  = '🛠️';
    document.getElementById('gm-confirm-title').textContent = 'Volver al modo edición';
    document.getElementById('gm-confirm-desc').textContent  = 'Actualmente estás en modo juego. ¿Quieres pasar a modo edición? Los puntos de tres y el botón + volverán a ser visibles.';
  } else {
    document.getElementById('gm-confirm-icon').textContent  = '🎮';
    document.getElementById('gm-confirm-title').textContent = 'Activar modo juego';
    document.getElementById('gm-confirm-desc').textContent  = 'Estás a punto de entrar en modo juego. Las herramientas de edición quedarán ocultas para los jugadores.';
  }
  document.getElementById('gamemode-confirm-modal').classList.add('open');
}

function cancelGameModeConfirm() {
  document.getElementById('gamemode-confirm-modal').classList.remove('open');
}

function applyGameMode() {
  _gameModeActive = !_gameModeActive;
  localStorage.setItem('gameMode', _gameModeActive ? '1' : '0');
  _applyGameModeUI();
  cancelGameModeConfirm();
  toast(_gameModeActive ? '🎮 Modo juego activado' : '🛠️ Modo edición activado');
}
// ────────────────────────────────────────────────────────────

function openPlantScanner() {'''
if 'function openPlantScanner() {' in c:
    c = c.replace('function openPlantScanner() {', NEW_JS, 1); print('[6] JS added')
else:
    errors.append('[6] openPlantScanner not found')

# ── 7. Initialize _applyGameModeUI on map init ───────────────
OLD_INIT = '''  loadTestPoisPositions();
  loadDynamicPois();
  loadAllPoiCodes();
  go('screen-map');
  renderPOIs();'''
NEW_INIT = '''  loadTestPoisPositions();
  loadDynamicPois();
  loadAllPoiCodes();
  _applyGameModeUI();
  go('screen-map');
  renderPOIs();'''
if OLD_INIT in c:
    c = c.replace(OLD_INIT, NEW_INIT, 1); print('[7] init call added')
else:
    errors.append('[7] _initMap sequence not found')

if errors:
    print('ERRORS:', errors)
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('\nAll OK — saved.')
