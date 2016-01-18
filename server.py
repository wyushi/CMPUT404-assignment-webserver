#  coding: utf-8 
import SocketServer, os
from http_header_parser import parse
from router import routing

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def setup(self):
        self.connection = self.request
        self.wfile = self.connection.makefile('wb', 0)


    def finish(self):
        self.wfile.flush()
        self.wfile.close()

    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        header = parse(self.data)
        if header == None:
            return
        if header['method'] == 'GET':
            self.handle_GET(header)
        else:
            self.send_error_page(405)

        
    def handle_GET(self, header):
        path = routing(header['route'])
        if path == None:
            self.send_error_page(404)
            return
        if os.path.exists(path):
            self.send_header_start(200)
            self.send_header_field("Content-type", self.mimetype(path))
            self.send_header_field("Content-length", self.content_length(path))
            self.send_header_end()
            self.send_static_page(path)
        else:
            self.send_error_page(404)


    def mimetype(self, path):
        name, ext = os.path.splitext(path)
        ext = ext.lower()
        if self.mimetypes.has_key(ext):
            return self.mimetypes[ext]
        else:
            return self.mimetypes['']


    def content_length(self, path):
        try:
            size = os.path.getsize(path)
        except os.error as error:
            print error
        return size


    def send_header_start(self, code):
        short, long_message = self.responses[code]
        self.wfile.write('%s %s %s \r\n' % 
            (self.protocol_version, str(code), short))


    def send_header_field(self, key, value):
        self.wfile.write("%s: %s\r\n" % (key, value))


    def send_header_end(self):
        self.wfile.write('\r\n')


    def send_static_page(self, path):
        file = open(path)
        self.wfile.write(file.read())
        file.close()


    def send_error_page(self, code):
        self.send_header_start(code)
        self.send_header_field("Content-type", self.error_page_template)
        self.send_header_end()
        f = open(self.error_page_template)
        template = f.read()
        f.close()
        self.wfile.write(template % {
                'code': code,
                'short_msg': self.responses[code][0],
                'long_msg': self.responses[code][1]
            })


    # Essentially static class variables
    
    error_page_template = './www/error.html'

    mimetypes = {
        '': 'application/octet-stream',
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.png': 'image/png',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpg'
    }

    # The version of the HTTP protocol we support.
    # Don't override unless you know what you're doing (hint: incoming
    # requests are required to have exactly this version string).
    protocol_version = "HTTP/1.0"
    # Table mapping response codes to messages; entries have the

    # form {code: (shortmessage, longmessage)}.
    # See http://www.w3.org/hypertext/WWW/Protocols/HTTP/HTRESP.html
    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        404: ('Not found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed', 'A request was made of a resource using a request method not supported by that resource; for example, using GET on a form which requires data to be presented via POST, or using PUT on a read-only resource.')
    }



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print  'Server starts listening on port %d\n' % PORT
    server.serve_forever()
