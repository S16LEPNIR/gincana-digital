import sys
sys.stdout.reconfigure(encoding="utf-8")
with open(r"C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone_backup.html","r",encoding="utf-8") as f:
    lines = f.readlines()

# Print lines 3292 to 3430 (around tc2)
print("=== Lines 3336-3430 ===")
for i in range(3335, 3430):
    print(str(i+1)+': '+lines[i][:120].rstrip())

# CSS around #tc2
print("\n=== CSS around #tc2 (lines 179-200) ===")
for i in range(178, 200):
    print(str(i+1)+': '+lines[i][:120].rstrip())
