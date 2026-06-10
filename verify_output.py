import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    content = f.read()
    lines = content.splitlines()

print(f'Total lines: {len(lines)}')

# 1. Where is bru-cin-overlay in HTML?
print('\n=== bru-cin-overlay placement ===')
for i,l in enumerate(lines):
    if 'bru-cin-overlay' in l and 'onclick' in l:
        for j in range(max(0,i-4), i+2):
            print(f'{j+1}: {lines[j][:100]}')
        break

# 2. Is the witch HTML at body top-level (not inside poi-config-overlay)?
print('\n=== poi-config-overlay vs bru-cin-overlay order ===')
poi_cfg_line = None
bru_cin_line = None
for i,l in enumerate(lines):
    if 'id="poi-config-overlay"' in l and poi_cfg_line is None:
        poi_cfg_line = i+1
    if 'id="bru-cin-overlay"' in l and bru_cin_line is None:
        bru_cin_line = i+1
print(f'poi-config-overlay at line: {poi_cfg_line}')
print(f'bru-cin-overlay at line: {bru_cin_line}')
print(f'bru-cin-overlay comes BEFORE poi-config-overlay: {bru_cin_line < poi_cfg_line}')

# 3. Script tag and key functions
print('\n=== Script / function positions ===')
for i,l in enumerate(lines):
    if '<script>' in l and 'src=' not in l: print(f'<script> at {i+1}')
    if '</script>' in l: print(f'</script> at {i+1}')
    if 'function nextCard' in l: print(f'nextCard at {i+1}')
    if 'function openWitchCinematic' in l: print(f'openWitchCinematic at {i+1}')
    if 'function bruCalcCompat' in l: print(f'bruCalcCompat at {i+1}')
    if 'function renderPOIs' in l: print(f'renderPOIs at {i+1}')

# 4. Check for JS string literal errors (single-quoted strings with real newlines)
print('\n=== JS string literal check ===')
script_start = content.index('<script>\n', content.index('</style>'))
script_end   = content.rindex('</script>')
js = content[script_start+8 : script_end]
js_lines = js.split('\n')
errors = []
in_sq = in_dq = in_bt = in_lc = in_bc = False
sq_start = None
for ln_no, line in enumerate(js_lines, 1):
    i = 0
    while i < len(line):
        ch = line[i]; nx = line[i+1] if i+1<len(line) else ''
        if in_lc: break
        if in_bc:
            if ch=='*' and nx=='/': in_bc=False; i+=2; continue
            i+=1; continue
        if ch=='\\': i+=2; continue
        if ch=='/' and nx=='/' and not in_sq and not in_dq and not in_bt: in_lc=True; break
        if ch=='/' and nx=='*' and not in_sq and not in_dq and not in_bt: in_bc=True; i+=2; continue
        if ch=="'" and not in_dq and not in_bt:
            in_sq = not in_sq
            if in_sq: sq_start=ln_no
        elif ch=='"' and not in_sq and not in_bt: in_dq=not in_dq
        elif ch=='`' and not in_sq and not in_dq: in_bt=not in_bt
        i+=1
    in_lc=False
    if in_sq:
        errors.append((ln_no, sq_start, js_lines[sq_start-1][:80]))
        in_sq=False
if errors:
    print(f'FOUND {len(errors)} unterminated single-quoted strings:')
    for ln,start,txt in errors: print(f'  Line {start}: {txt}')
else:
    print('No unterminated single-quoted strings found. JS looks OK.')

# 5. tc2 content check
print('\n=== TC2 content check ===')
for i,l in enumerate(lines):
    if 'Busca la placa' in l:
        print(f'NEW tc2 text found at line {i+1}')
    if 'Cada prueba' in l and 'vinculada' in l:
        print(f'OLD tc2 text still at line {i+1} - BAD!')
    if 'tcard-img' in l and i > 3200 and i < 3400:
        print(f'tcard-img at line {i+1}: {l[:80]}')
