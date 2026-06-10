import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    lines = f.readlines()

def show(label, start, end):
    print(f'\n=== {label} (lines {start+1}-{end+1}) ===')
    for i in range(start, min(end, len(lines))):
        print(str(i+1)+': '+lines[i][:110].rstrip())

# 1. S state object
for i,l in enumerate(lines):
    if 'const S = {' in l or 'var S = {' in l:
        show('S STATE', i, i+22)
        break

# 2. backpack menu end
for i,l in enumerate(lines):
    if 'id="backpack-menu"' in l:
        show('BACKPACK MENU', i, i+65)
        break

# 3. watchPosition callback
for i,l in enumerate(lines):
    if 'watchPosition' in l:
        show('WATCH_POSITION', i-2, i+20)
        break

# 4. Test POI click handler
for i,l in enumerate(lines):
    if 'handlePoiClick' in l and 'addEventListener' not in l and 'function' not in l:
        show('TEST POI CLICK', i-5, i+3)
        break

# 5. Info POI click handler
for i,l in enumerate(lines):
    if 'openInfoPoiModal' in l and 'addEventListener' not in l and 'function' not in l:
        show('INFO POI CLICK', i-5, i+3)
        break

# 6. Supervisor click handler
for i,l in enumerate(lines):
    if 'handleSupervisorClick' in l and 'function' not in l:
        show('SUPERVISOR CLICK', i-5, i+3)
        break

# 7. Witch click handler
for i,l in enumerate(lines):
    if 'openWitchCinematic' in l and 'function' not in l and 'addEventListener' not in l:
        show('WITCH CLICK', i-5, i+3)
        break

# 8. Dynamic POI click
for i,l in enumerate(lines):
    if 'dp.type' in l and 'openInfoPoiModal' in l:
        show('DYN POI CLICK', i-5, i+3)
        break

# 9. updateGpsDisplay or similar function
for i,l in enumerate(lines):
    if 'function updateGpsDisplay' in l or 'function initGPS' in l:
        show('GPS_INIT', i, i+30)
        break
