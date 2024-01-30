from json import dumps
from os.path import join as pjoin
from tempfile import TemporaryFile
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.path = self.path.lower()
        if(self.path == '/' or self.path == None or self.path == '/status' or self.path == '/status/'):
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        
        self.send_response(404, 'Nothing here.')
        self.end_headers()
        self.wfile.write(b'Not Found.')
        return

    def do_POST(self):
        self.path = self.path.lower()
        params = parse_qs(urlparse(self.path).query)
        if(self.path.startswith('/gait_analysis')):
            uuid = params.get('uuid', None)
            if(uuid == None):
                self.send_response(400, 'No UUID')
                self.end_headers()
                self.wfile.write(b'No UUID specified')
                return
            uuid = uuid[0]
        
            self.post_upload(uuid)
            return

        self.send_response(404, 'Nothing here.')
        self.end_headers()
        self.wfile.write(b'Not Found.')
        return

    def post_upload(self, uuid):
        length = self.headers['Content-length']
        data = self.rfile.read(int(length))
        f = TemporaryFile() # Creates temp file in OS temp folder.
        f.write(data)
        f.flush()

        self.send_response(200)
        self.end_headers()
        
        print("New analysis video uploaded: " + uuid + ".mp4  >  " + f.name)
        
        #TODO Gait analysis here. (Processing)

        f.close() # Deletes temp file.

        data = {'status': 'Successful', 'results': ['todo?']}
        self.wfile.write(dumps(data).encode())
        return;

def start():
    server = ThreadingHTTPServer(('0.0.0.0', 1234), StoreHandler)
    server.serve_forever()
