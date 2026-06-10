import sys
sys.stdout.reconfigure(encoding="utf-8")
with open(r"C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone_backup.html","r",encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

idx = content.find('id="tc2"')
print("Found at char:", idx)

# Find line number
char_count = 0
for i, l in enumerate(lines):
    char_count += len(l)
    if char_count > idx:
        print(f"Line number: {i+1}")
        # Print context
        for j in range(max(0,i-2), min(len(lines), i+45)):
            print(str(j+1) + ": " + lines[j][:120].rstrip())
        break
