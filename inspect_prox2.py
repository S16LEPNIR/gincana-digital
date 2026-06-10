import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    lines = f.readlines()

def show(label, start, end):
    print(f'\n=== {label} ===')
    for i in range(start, min(end, len(lines))):
        print(str(i+1)+': '+lines[i].rstrip())

# Full dyn POI click handler
for i,l in enumerate(lines):
    if "dp.type === 'info'" in l:
        show('DYN POI FULL', i-5, i+5)
        break

# S state - last 3 lines
for i,l in enumerate(lines):
    if '_relocateMode: false' in l:
        show('S STATE END', i-1, i+3)
        break

# startGame or init function
for i,l in enumerate(lines):
    if 'function startGame' in l:
        show('startGame', i, i+10)
        break

# Where renderPOIs is called on startup
for i,l in enumerate(lines):
    if 'renderPOIs()' in l and 'function' not in l:
        print(str(i+1)+': '+l.rstrip())

# where toast element is in HTML
for i,l in enumerate(lines):
    if 'id="toast"' in l:
        show('TOAST HTML', i, i+3)
        break

# gpsToPixels function
for i,l in enumerate(lines):
    if 'function gpsToPixels' in l:
        show('gpsToPixels', i, i+8)
        break
