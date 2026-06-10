import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Sergio\Desktop\Mapa interactivo assets\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the main <script> block (single block)
script_start = content.index('<script>\n', content.index('</style>'))
script_end   = content.rindex('</script>')
js = content[script_start+8 : script_end]
lines = js.split('\n')

print(f'JS block: {len(lines)} lines')

# Scan for single-quoted strings containing a real newline
# (look for opening ' that never closes on the same line)
errors = []
in_sq = False
in_dq = False
in_bt = False  # backtick template
in_line_comment = False
in_block_comment = False
sq_start = None

for ln_no, line in enumerate(lines, 1):
    i = 0
    while i < len(line):
        ch = line[i]
        nx = line[i+1] if i+1 < len(line) else ''

        if in_line_comment:
            break  # rest of line is comment

        if in_block_comment:
            if ch == '*' and nx == '/':
                in_block_comment = False; i += 2; continue
            i += 1; continue

        if ch == '\\':
            i += 2; continue  # skip escaped char

        if ch == '/' and nx == '/' and not in_sq and not in_dq and not in_bt:
            in_line_comment = True; break
        if ch == '/' and nx == '*' and not in_sq and not in_dq and not in_bt:
            in_block_comment = True; i += 2; continue

        if ch == "'" and not in_dq and not in_bt:
            if in_sq:
                in_sq = False
            else:
                in_sq = True; sq_start = ln_no
        elif ch == '"' and not in_sq and not in_bt:
            in_dq = not in_dq
        elif ch == '`' and not in_sq and not in_dq:
            in_bt = not in_bt
        i += 1

    in_line_comment = False

    # After processing the line: if still in a single-quoted string, that's a syntax error
    if in_sq:
        errors.append((ln_no, sq_start, lines[sq_start-1][:80]))
        in_sq = False  # reset to continue scanning

if errors:
    print(f'FOUND {len(errors)} unterminated single-quoted string(s):')
    for ln, start, text in errors:
        print(f'  Line {start}: {text}')
else:
    print('No unterminated single-quoted strings found.')

# Also check for common patterns
print()
bru_idx = js.find('BRU_DIALOGS')
if bru_idx >= 0:
    chunk = js[bru_idx:bru_idx+400]
    print('BRU_DIALOGS:')
    print(chunk)
