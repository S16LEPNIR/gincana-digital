import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

changes = [
    # 1. P2_PLANTS[3]
    (
        '  { id: 3, name: "Laurel", icon: "🍃" },',
        '  { id: 3, name: "Hinojo", icon: "🌿" },',
        'P2_PLANTS[3]'
    ),
    # 2. P2_CORRECT_USES[3]
    (
        '  "Condimento culinario y digestivo, con uso tradicional antiinflamatorio",',
        '  "Digestivo y carminativo, alivia gases, distensión abdominal y espasmos intestinales",',
        'P2_CORRECT_USES[3]'
    ),
    # 3. P2_WRONG_USES_FIXED[3]
    (
        '  ["Planta venenosa usada solo con fines ornamentales", "Estimulante cardíaco en dosis controladas", "Infusión calmante para el insomnio"],',
        '  ["Antibiótico natural eficaz contra infecciones bacterianas", "Analgésico potente para dolores musculares", "Estimulante cardíaco en dosis controladas"],',
        'P2_WRONG_USES_FIXED[3]'
    ),
    # 4. P2_SUMMARIES[3]
    (
        '  { icon:"🍃", plant:"Laurel",  latin:"Laurus nobilis",         desc:"Sus hojas contienen cineol con efectos digestivos y antiinflamatorios. En la Antigua Roma los héroes y poetas eran coronados con laurel, símbolo de excelencia." },',
        '  { icon:"🌿", plant:"Hinojo",  latin:"Foeniculum vulgare",      desc:"Su anetol le da ese característico aroma a anís. Los romanos lo comían creyendo que prevenía la obesidad y mejoraba la visión. Hoy se usa como digestivo, carminativo y expectorante suave." },',
        'P2_SUMMARIES[3]'
    ),
    # 5. P2_RIDDLES[3]
    (
        '  "Sus hojas aromáticas llevan siglos en las cocinas del mundo. También fue símbolo de gloria en la Antigua Grecia y tiene propiedades digestivas reconocidas.",',
        '  "Hueles algo que recuerda al anís. La abuela lo prepara en infusión cuando tienes el estómago hinchado o gases después de comer. Sus semillas, hojas y bulbo se usan en la cocina mediterránea. ¿Para qué sirve?",',
        'P2_RIDDLES[3]'
    ),
    # 6. P2_CURIOSITIES[3]
    (
        "  \"La palabra 'bachiller' deriva del latín 'baccalaureus', que significa 'coronado con laurel'. En la Antigua Roma se daban coronas de laurel a los poetas y generales victoriosos.\",",
        "  \"La palabra griega 'marathon' significa 'lugar donde crece el hinojo': la batalla de Maratón se libró en un campo de hinojos. Los gladiadores romanos lo incluían en su dieta creyendo que les daba fuerza y agudeza visual.\",",
        'P2_CURIOSITIES[3]'
    ),
]

for old, new, label in changes:
    if old not in html:
        print(f'ERROR: {label} not found')
        print(f'  Looking for: {repr(old[:80])}')
    else:
        html = html.replace(old, new)
        print(f'OK: {label}')

with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done - file saved')
