from os.path import join as pjoin
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def getDirectory():
    from inspect import getsourcefile
    from os.path import abspath

    return abspath(getsourcefile(lambda:0))

class StoreHandler(BaseHTTPRequestHandler):
    directory = pjoin(getDirectory(), 'Data')

    def do_GET(self):
        self.path = self.path.lower()
        params = parse_qs(urlparse(self.path).query)
        if(self.path.startswith('/gait/')):
            uuid = params.get('uuid', None)
            if(uuid == None):
                self.send_response(400, 'No UUID specified')
                self.end_headers()
                self.wfile.write(b'No UUID specified')
                return

            sub = self.path[6:].split('?')[0]
            if(sub == 'download'):
                self.get_download(uuid)
                return
            if(sub == 'status'):
                self.get_status(uuid)
                return
            if(sub == 'results'):
                self.get_results(uuid);
                return
            
            self.send_response(404, 'Nothing here.')
            self.end_headers()
            self.wfile.write(b'Not Found.')
            

        if(self.path == '' or self.path == None or self.path == 'status'):
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
        if(self.path.startswith('/gait/')):
            uuid = params.get('uuid', None)
            if(uuid == None):
                self.send_response(400, 'No UUID')
                self.end_headers()
                self.wfile.write(b'No UUID specified')
                return
        
            sub = self.path[6:].split('?')[0]
            if(sub == 'upload'):
                self.post_upload(uuid)
                return

        self.send_response(404, 'Nothing here.')
        self.end_headers()
        self.wfile.write(b'Not Found.')
        return

    def post_upload(self, uuid):
        length = self.headers['content-length']
        data = self.rfile.read(int(length))

        with open(pjoin(self.directory, 'raw', uuid), 'w') as fh:
            fh.write(data.decode())

        self.send_response(200)
        self.end_headers()
        
        #TODO, Queue for processing
        return;

    def get_download(self, uuid):
        self.send_response(200)
        self.send_header('content-type', 'video/mp4')
        self.end_headers()

        with open(pjoin(self.directory, 'raw', uuid), 'r') as fh:
            self.wfile.write(fh.read().encode())
    
    def get_status(self, uuid):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()

        #TODO: Check if results exist?
        self.wfile.write(b'{"status": "Pending"}')

    def get_results(self, uuid):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()

        #TODO: Check if results exist first.
        #TODO: Actual results (file? or DB?).
        self.wfile.write(b'{"results": "TODO"}')

def start():
    server = ThreadingHTTPServer(('0.0.0.0', 1234), StoreHandler)
    server.serve_forever()
