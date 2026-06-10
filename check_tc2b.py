import sys
sys.stdout.reconfigure(encoding="utf-8")
with open(r"C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone_backup.html","r",encoding="utf-8") as f:
    lines = f.readlines()

# Find end of tc2
in_tc2 = False
depth = 0
for i, l in enumerate(lines):
    if 'id="tc2"' in l:
        in_tc2 = True
        depth = 0
    if in_tc2:
        for ch in l:
            if ch == '<':
                pass
        # Count div open/close
        import re
        opens = len(re.findall(r'<div', l))
        closes = len(re.findall(r'</div>', l))
        if i > 3291:  # after the tc2 opening line
            depth += opens - closes
            if depth <= 0 and i > 3292:
                print(f"tc2 ends at line {i+1}: {l[:80].rstrip()}")
                # Print around end
                for j in range(max(0,i-3), min(len(lines), i+5)):
                    print(str(j+1)+': '+lines[j][:100].rstrip())
                break

# Find CSS #tc2 > p
print("\n=== #tc2 CSS ===")
for i, l in enumerate(lines):
    if '#tc2' in l and i < 400:
        print(str(i+1)+': '+l[:120].rstrip())
