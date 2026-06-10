import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    lines = f.readlines()

# Oracle overlay
print('=== Oracle overlay ===')
for i,l in enumerate(lines):
    if 'bru-oracle-overlay' in l and 'id=' in l:
        for j in range(i, min(i+12, len(lines))):
            print(str(j+1)+': '+lines[j][:100].rstrip())
        break

# Compat overlay
print('\n=== Compat overlay ===')
for i,l in enumerate(lines):
    if 'bru-compat-overlay' in l and 'id=' in l:
        for j in range(i, min(i+25, len(lines))):
            print(str(j+1)+': '+lines[j][:100].rstrip())
        break

# Key oracle JS functions
print('\n=== Oracle JS ===')
for i,l in enumerate(lines):
    if 'function bruOracleSequence' in l or 'function bruChoiceOracle' in l or 'function bruSetCompatType' in l:
        print(str(i+1)+': '+l[:80].rstrip())
