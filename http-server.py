#!/usr/bin/python

# curl -T filename.txt http://www.example.com/dir/

import signal
from threading import Thread
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import urlparse
import orb_process_store

class MyHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        print "----- SOMETHING WAS PUT!! ------"

        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)


        #@todo get arg "?index=a...1" and pass to this function
        orb_process_store.processDescriptorsFromImage(content, self.path)
        self.send_response(200)

    def do_GET(self):
        print "---- GET!! ----"

    def do_POST(self):
        print "-- GOT POST--"
        orb_process_store.search(self.rfile.read(int(self.headers.getheader('Content-Length'))))

#        print postvars
        #@todo get arg "?index=a...1" and pass to this function
        # so that multiple separate indexes can be contained in the case of band name etc

        #length = int(self.headers['Content-Length'])
#        orb_process_store.search(postvars[''][0])

        # Get descriptors, load existing index, begin brute force matching


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