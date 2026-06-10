import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html','r',encoding='utf-8') as f:
    lines = f.readlines()

# Find renderPOIs and its end
for i,l in enumerate(lines):
    if 'function renderPOIs' in l:
        start = i
        break

print(f'renderPOIs starts at line {start+1}')
# Print from witchPoi area
for i in range(start, len(lines)):
    if 'witch-witch' in lines[i] or 'witchPoi' in lines[i] or 'poi-witch' in lines[i]:
        for j in range(max(start, i-1), min(len(lines), i+20)):
            print(str(j+1)+': '+lines[j][:120].rstrip())
        break

# Also print renderPOIs last 10 lines
print('\n=== Last lines of renderPOIs ===')
# Find end of renderPOIs (the } at indent 0 after it)
depth = 0
for i in range(start, min(start+500, len(lines))):
    for ch in lines[i]:
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
    if depth == 0 and i > start:
        for j in range(max(0, i-5), i+3):
            print(str(j+1)+': '+lines[j][:120].rstrip())
        break
