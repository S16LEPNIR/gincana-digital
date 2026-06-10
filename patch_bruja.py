import sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\Sergio\Desktop\Mapa interactivo assets'
with open(base + '\\ginkana_standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

OLD = '''function bruCalcCompat() {
  var a = document.getElementById('bru-name1').value.trim();
  var b = document.getElementById('bru-name2').value.trim();
  if (!a || !b) { alert('Introduce los dos nombres para calcular la compatibilidad.'); return; }
  if (!localStorage.getItem('witchVisited')) { localStorage.setItem('witchVisited', '1'); checkAchievements(['credulo']); }
  var seed = 0, combined = (a + b).toLowerCase();
  for (var i = 0; i < combined.length; i++) seed += combined.charCodeAt(i);
  var pct = 60 + (seed % 40);
  var phrasesAmist = [
    "Una amistad verdadera, de esas que duran toda la vida.",
    "Vuestra conexión es como las raíces de un árbol: profunda y firme.",
    "Hay una complicidad especial entre vosotros. El jardín lo confirma.",
    "Una chispa de amistad que puede convertirse en algo inquebrantable."
  ];
  var phrasesRom = [
    "Una conexión cósmica extraordinaria. Las estrellas os unieron.",
    "Vuestra armonía es como la de las flores y las abejas. Perfectos.",
    "Un lazo muy especial os une. El jardín lo puede sentir.",
    "Hay chispa entre vosotros. La magia ya ha comenzado a actuar."
  ];
  var phrases = _bruCompatType === 'amistad' ? phrasesAmist : phrasesRom;
  var phraseIdx = pct >= 90 ? 0 : pct >= 80 ? 1 : pct >= 70 ? 2 : 3;
  document.getElementById('bru-compat-form').style.display = 'none';
  var resultEl = document.getElementById('bru-compat-result');
  resultEl.style.display = 'flex';
  var pctEl = document.getElementById('bru-compat-pct');
  pctEl.textContent = '0%';
  document.getElementById('bru-compat-phrase').textContent = phrases[phraseIdx];
  var current = 0;
  var timer = setInterval(function() {
    if (current < pct) { current++; pctEl.textContent = current + '%'; }
    else clearInterval(timer);
  }, 25);
}'''

NEW = '''function bruCalcCompat() {
  var a = document.getElementById('bru-name1').value.trim();
  var b = document.getElementById('bru-name2').value.trim();
  if (!a || !b) { alert('Introduce los dos nombres para calcular la compatibilidad.'); return; }
  if (!localStorage.getItem('witchVisited')) { localStorage.setItem('witchVisited', '1'); checkAchievements(['credulo']); }

  // Hash FNV-1a sobre ambos nombres + tipo para máxima dispersión
  function fnv32(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = (Math.imul(h, 16777619)) >>> 0; }
    return h;
  }
  var type  = _bruCompatType || 'x';
  var h1    = fnv32((a + '\x01' + b + '\x01' + type).toLowerCase());
  var h2    = fnv32((b + '\x01' + a + '\x01' + type).toLowerCase());
  var mixed = ((h1 ^ (h2 << 11) ^ (h2 >>> 5)) >>> 0) % 1000;

  // Distribución no uniforme: cubre todo el rango 1-99 con variedad real
  var pct;
  if      (mixed <  60) pct =  1 + (mixed % 12);          //  1-12  (6 %)
  else if (mixed < 150) pct = 13 + (mixed % 15);          // 13-27  (9 %)
  else if (mixed < 280) pct = 28 + (mixed % 18);          // 28-45 (13 %)
  else if (mixed < 460) pct = 46 + (mixed % 18);          // 46-63 (18 %)
  else if (mixed < 670) pct = 64 + (mixed % 16);          // 64-79 (21 %)
  else if (mixed < 870) pct = 80 + (mixed % 13);          // 80-92 (20 %)
  else                  pct = 93 + (mixed %  7);          // 93-99 (13 %)

  // Frases por tramo — amistad
  var amistTiers = [
    // 1-27
    ["Las estrellas os ven pasar por caminos muy distintos... por ahora.",
     "La conexión existe, pero es tenue. Como dos plantas en macetas separadas.",
     "El jardín percibe que aún os estáis conociendo. Todo a su tiempo.",
     "Vuestra energía choca un poco. Quizá necesitáis más tiempo juntos."],
    // 28-45
    ["Hay potencial, pero también roces. La amistad requiere riego constante.",
     "El vínculo existe, aunque aún es frágil. Como un brote recién plantado.",
     "El jardín ve algo en vosotros, pero todavía debe crecer. Cultívalo.",
     "Una amistad en construcción. Con paciencia puede florecer."],
    // 46-63
    ["Una amistad sólida y equilibrada. Como el ciclo de las estaciones.",
     "Hay buena sintonía. El jardín siente que os entendéis bien.",
     "Compenetración notable. Sois como dos ramas del mismo árbol.",
     "El lazo es real y estable. Podéis contar el uno con el otro."],
    // 64-79
    ["Una amistad genuina y profunda. El jardín lo siente con fuerza.",
     "Vuestra conexión tiene raíces fuertes. Difícil de romper.",
     "Gran complicidad. Como el romero y el sol, os hacéis bien mutuamente.",
     "El jardín os ve como aliados naturales. Una amistad para recordar."],
    // 80-99
    ["¡Amistad extraordinaria! Las flores del jardín se inclinan ante vosotros.",
     "Una complicidad única. Como si vuestras almas se conocieran de otra vida.",
     "El jardín nunca ha visto tanta armonía. Sois inseparables.",
     "¡Rara vez el jardín ve tanto destello! Una amistad verdaderamente especial."]
  ];

  // Frases por tramo — romance
  var romTiers = [
    // 1-27
    ["Las flores se giran... en dirección opuesta. Las estrellas guardan silencio.",
     "El jardín percibe chispas, pero muy tímidas. La magia necesita más tiempo.",
     "Una atracción leve, como el rocío que se evapora al amanecer.",
     "El cosmos no os ve juntos aún. Quizá en otro momento del jardín."],
    // 28-45
    ["Hay algo... pero todavía sin florecer. El amor es un proceso lento.",
     "Una semilla de algo especial. Aún necesita tierra fértil y paciencia.",
     "El jardín percibe algo entre vosotros, aunque aún no sabe qué.",
     "Chispa tenue. Como una vela al viento. Puede apagarse... o encenderse."],
    // 46-63
    ["Una conexión romántica interesante. El jardín la observa con curiosidad.",
     "Hay armonía. No es un fuego, pero sí una brasa cálida y real.",
     "El corazón late un poco más fuerte. Algo aquí merece atención.",
     "Compatible, sí. El jardín siente que podríais construir algo juntos."],
    // 64-79
    ["Una atracción notable. Como las lianas que se enredan con naturalidad.",
     "El jardín ve una llama entre vosotros. Hay potencial romántico real.",
     "Buena compatibilidad. Las estrellas sonríen cuando pronuncia vuestros nombres.",
     "Hay algo especial aquí. El jardín lo siente en cada hoja que tiembla."],
    // 80-99
    ["¡Conexión cósmica extraordinaria! Las estrellas llevan tiempo esperando esto.",
     "El jardín nunca miente: vuestros corazones laten al mismo ritmo.",
     "¡Amor de los que perduran! Como el olivo milenario: eterno y resistente.",
     "¡Raro y precioso! El jardín ha visto pocas parejas con tanta magia."]
  ];

  var tierIdx = pct <= 27 ? 0 : pct <= 45 ? 1 : pct <= 63 ? 2 : pct <= 79 ? 3 : 4;
  var tiers   = _bruCompatType === 'amistad' ? amistTiers : romTiers;
  var pool    = tiers[tierIdx];
  var phrase  = pool[fnv32((a + b + type + pct).toLowerCase()) % pool.length];

  document.getElementById('bru-compat-form').style.display = 'none';
  var resultEl = document.getElementById('bru-compat-result');
  resultEl.style.display = 'flex';
  var pctEl = document.getElementById('bru-compat-pct');
  pctEl.textContent = '0%';
  document.getElementById('bru-compat-phrase').textContent = phrase;
  var current = 0, speed = pct > 70 ? 18 : pct > 40 ? 22 : 30;
  var timer = setInterval(function() {
    if (current < pct) { current++; pctEl.textContent = current + '%'; }
    else clearInterval(timer);
  }, speed);
}'''

assert OLD in html, 'bruCalcCompat not found'
html = html.replace(OLD, NEW)
print('bruCalcCompat replaced')

with open(base + '\\ginkana_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done - file saved')
