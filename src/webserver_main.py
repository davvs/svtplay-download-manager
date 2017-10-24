#!/usr/bin/env python

import textwrap
import WebShow
import WebUpdateFeeds

from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class HelloRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print self.path
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response_text = textwrap.dedent('''\
                <html>
                <head>
                    <title>Greetings to the world</title>
                </head>
                <body>
                    <h1>Greetings to the world</h1>
                    <p>Hello, world!</p>
                </body>
                </html>
            ''')
            self.wfile.write(response_text.encode('utf-8'))
        elif self.path == "/show":
            WebShow.show(self)
            return
        else:
            self.send_error(404, "Object not found")
            return

    def do_POST(self):
        if self.path == "/updateFeeds":
            WebUpdateFeeds.updateFeeds(self)
            return
        else:
            self.send_error(404, "Object not found")
            return
        # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        # if ctype == 'multipart/form-data':
        #     postvars = cgi.parse_multipart(self.rfile, pdict)
        # elif ctype == 'application/x-www-form-urlencoded':
        #     length = int(self.headers.getheader('content-length'))
        #     postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        # else:
        #     postvars = {}
        # ...


server_address = ('', 8080)
httpd = HTTPServer(server_address, HelloRequestHandler)
print "Serving forever"
httpd.serve_forever()

