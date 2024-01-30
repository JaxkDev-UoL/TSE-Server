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
        params = parse_qs(urlparse(self.path).query)
        print(self.path)
        print(params)
        if(self.path.startswith('/gait/')):
            if(params.get('uuid', None) == None):
                self.send_response(400, 'No UUID specified')
                self.end_headers()

            sub = self.path[6:].split('?')[0]
            if(sub == 'download'):
                self.get_download()
            if(sub == 'status'):
                self.get_status()
            if(sub == 'results'):
                self.get_results();

            with open(pjoin(self.directory, 'ID')) as fh:
                self.send_response(200)
                self.send_header('content-type', 'image/png')
                self.end_headers()
                self.wfile.write(fh.read().encode())

    def do_POST(self):
        params = parse_qs(urlparse(self.path).query)
        if(self.path == '/gait/upload'):
            if(params.get('uuid', None) == None):
                self.send_response(400, 'No UUID specified')
                return
            
            length = self.headers['content-length']
            data = self.rfile.read(int(length))

            with open(pjoin(self.directory, 'ID'), 'w') as fh:
                fh.write(data.decode())

            self.send_response(200)

def start():
    server = ThreadingHTTPServer(('0.0.0.0', 1234), StoreHandler)
    server.serve_forever()
