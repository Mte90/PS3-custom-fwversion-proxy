#!/usr/bin/python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib import request, error
import sys
PORT = 8080
FW_VERSION = "4.8600"


class PS3Proxy(SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        print("URL requested: " + url)
        self.server_version = ""
        self.sys_version = "AkamaiNetStorage"
        if "ps3-updatelist.txt" in url:
            with open('ps3-updatelist.txt', 'r') as reader:
                content = reader.read().replace('FW_VERSION', FW_VERSION).replace("\n","\r\n")
            if url[0] == "/":
                url = url[1:]
            # Do real requests to get the headers
            response = request.urlopen(url)
            self.send_response(200)
            for name, value in response.headers.items():
                if name != "Date" and name != "Server":
                    self.send_header(name, value)
            self.end_headers()
            print("Serving custom ps3-updatelist.txt")
            self.wfile.write(bytes(content, "utf8"))
        else:
            if "http" not in url:
                url = url[1:]

            if "favicon" in url:
                return

            if len(url) >= 2:
                try:
                    response = request.urlopen(url)
                except error.HTTPError as e:
                    self.send_response_only(e.code)
                    self.end_headers()
                    return

                self.send_response_only(response.status)
                for name, value in response.headers.items():
                    self.send_header(name, value)
                self.end_headers()
                self.copyfile(response, self.wfile)
            else:
                print("You are accessing locally and is not working in that way")


httpd = HTTPServer(('', PORT), PS3Proxy)
host, port = httpd.socket.getsockname()
print(f'Listening on {host}:{port}')
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    sys.exit(0)
