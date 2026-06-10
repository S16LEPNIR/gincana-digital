#!/usr/bin/env python3
"""
Servidor local para fijar posiciones en ginkana_standalone.html.
Ejecuta este script UNA VEZ antes de usar el botón "Fijar posiciones".
Mantén la ventana abierta mientras editas el mapa.
"""
import http.server
import json
import re
from pathlib import Path

HTML_FILE = Path(__file__).parent / 'ginkana_standalone.html'
PORT = 7891

class Handler(http.server.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path != '/fix-positions':
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            positions = json.loads(body)
            html = HTML_FILE.read_text(encoding='utf-8')
            pos_json = json.dumps(positions, ensure_ascii=False, separators=(',', ':'))
            updated = re.sub(
                r'<script id="default-positions-data" type="application/json">.*?</script>',
                f'<script id="default-positions-data" type="application/json">{pos_json}</script>',
                html,
                flags=re.DOTALL
            )
            HTML_FILE.write_text(updated, encoding='utf-8')
            self._respond(200, {'ok': True})
            print(f'✅  Posiciones guardadas en {HTML_FILE.name}')
        except Exception as e:
            self._respond(500, {'ok': False, 'error': str(e)})
            print(f'❌  Error: {e}')

    def _respond(self, code, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        origin = self.headers.get('Origin', '*')
        self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Vary', 'Origin')

    def log_message(self, *args):
        pass  # silencia el log de cada request

if __name__ == '__main__':
    print(f'🗺️  Servidor de posiciones iniciado — puerto {PORT}')
    print(f'📄  Archivo: {HTML_FILE}')
    print('ℹ️  Deja esta ventana abierta mientras usas el mapa.')
    print('    Pulsa Ctrl+C para detener.\n')
    with http.server.HTTPServer(('localhost', PORT), Handler) as srv:
        srv.serve_forever()
