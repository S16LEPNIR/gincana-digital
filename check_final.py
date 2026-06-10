import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    lines = f.readlines()

# nextCard function
print('=== nextCard ===')
for i,l in enumerate(lines):
    if 'function nextCard' in l:
        for j in range(i, min(i+8, len(lines))):
            print(str(j+1)+': '+lines[j][:100].rstrip())
        break

# witch POI in renderPOIs
print('\n=== renderPOIs closing area ===')
for i,l in enumerate(lines):
    if 'function renderPOIs' in l:
        start = i
        break
end_poi = None
for i,l in enumerate(lines):
    if 'poi-witch' in l:
        end_poi = i
for j in range(end_poi-2, end_poi+12):
    print(str(j+1)+': '+lines[j][:100].rstrip())

# witch relocate cases
print('\n=== startRelocatePoi witch ===')
for i,l in enumerate(lines):
    if "type === 'witch'" in l and 'startRelocate' not in l:
        pass
    if 'poi-witch' in l and 'poiEl' in l:
        print(str(i+1)+': '+lines[i][:100].rstrip())
    if "type === 'witch'" in l and 'saveWitch' in l:
        print(str(i+1)+': '+lines[i][:100].rstrip())

# witch position functions
print('\n=== witch position functions ===')
for i,l in enumerate(lines):
    if 'loadWitchPosition' in l or 'saveWitchPosition' in l:
        print(str(i+1)+': '+lines[i][:100].rstrip())
