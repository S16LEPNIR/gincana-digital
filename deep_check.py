import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

# 1. Check context around bru-cin-overlay in HTML
print('\n=== HTML context around bru-cin-overlay ===')
for i, l in enumerate(lines):
    if 'bru-cin-overlay' in l and 'onclick' in l:
        for j in range(max(0,i-3), min(len(lines), i+4)):
            print(f'{j+1}: {lines[j][:100].rstrip()}')
        break

# 2. Check that the JS main block is INSIDE <script>...</script>
print('\n=== Script tag boundaries ===')
for i, l in enumerate(lines):
    if '<script>' in l and 'src=' not in l:
        print(f'<script> at line {i+1}')
    if '</script>' in l:
        print(f'</script> at line {i+1}')
    if 'function nextCard' in l:
        print(f'nextCard at line {i+1}')
    if 'function openWitchCinematic' in l:
        print(f'openWitchCinematic at line {i+1}')
    if 'var BRU_DIALOGS' in l:
        print(f'BRU_DIALOGS at line {i+1}')

# 3. Check for duplicate function definitions
print('\n=== Duplicate function definitions ===')
funcs = {}
for i, l in enumerate(lines):
    m = re.match(r'\s*function\s+(\w+)\s*\(', l)
    if m:
        name = m.group(1)
        funcs.setdefault(name, []).append(i+1)
for name, lns in funcs.items():
    if len(lns) > 1:
        print(f'  DUPLICATE: {name}() at lines {lns}')

# 4. Check for const/let re-declarations
print('\n=== Const/let redeclarations ===')
decls = {}
for i, l in enumerate(lines):
    m = re.match(r'\s*(const|let)\s+(\w+)\s*[=;(]', l)
    if m:
        name = m.group(2)
        decls.setdefault(name, []).append(i+1)
for name, lns in decls.items():
    if len(lns) > 1:
        print(f'  REDECL: {m.group(1)} {name} at lines {lns}')

# 5. Check the actual nextCard vicinity
print('\n=== nextCard function ===')
for i, l in enumerate(lines):
    if 'function nextCard' in l:
        for j in range(i, i+8):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
