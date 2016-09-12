#!/usr/bin/python

# curl -T filename.txt http://www.example.com/dir/

import signal
from threading import Thread
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import time
import json
import orb_process_store

class MyHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        print "----- SOMETHING WAS PUT!! ------"
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)

        orb_process_store.processDescriptorsFromImage(content, self.path)
        self.send_response(200)

    def do_GET(self):
        print "---- GET!! ----"

    def do_POST(self):
        print "-- GOT POST--"
        ms = time.time() * 1000.0

        orb_result = orb_process_store.search(self.rfile.read(int(self.headers.getheader('Content-Length'))))
        mse = time.time() * 1000.0

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(str(json.dumps({'time': mse - ms, 'results': orb_result})))
        self.wfile.close()

def run_on(port):
    print("Starting a server on port %i" % port)
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    server = Thread(target=run_on, args=[8080])
    server.daemon = True # Do not make us wait for you to exit
    server.start()

    signal.pause() # Wait for interrupt signal, e.g. KeyboardInterrupt
