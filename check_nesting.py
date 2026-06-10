import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    lines = f.readlines()

# Print lines 4320-4370
print('=== Lines 4320-4370 ===')
for i in range(4319, 4370):
    print(str(i+1)+': '+lines[i][:100].rstrip())

# Also check: where does poi-config-overlay CLOSE?
print('\n=== poi-config-overlay close ===')
for i,l in enumerate(lines):
    if 'id="poi-config-overlay"' in l:
        print(f'Opens at {i+1}')
        # find matching close
        depth = 0
        for j in range(i, min(i+200, len(lines))):
            d = lines[j].count('<div') - lines[j].count('</div>')
            depth += d
            if j > i and depth <= 0:
                print(f'Closes at {j+1}: {lines[j][:80].rstrip()}')
                break
        break

# Check for script tags not in head
print('\n=== openWitchCinematic, bruCalcCompat location ===')
for i,l in enumerate(lines):
    if 'function openWitchCinematic' in l: print(f'openWitchCinematic at line {i+1}')
    if 'function bruCalcCompat' in l: print(f'bruCalcCompat at line {i+1}')
    if 'var BRU_DIALOGS' in l: print(f'BRU_DIALOGS at line {i+1}')
