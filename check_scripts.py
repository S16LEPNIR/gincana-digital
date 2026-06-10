import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone_backup.html','r',encoding='utf-8') as f:
    lines = f.readlines()
# Find all script tags
for i,l in enumerate(lines):
    if '<script' in l or '</script' in l:
        print(str(i+1)+': '+l[:100].rstrip())
