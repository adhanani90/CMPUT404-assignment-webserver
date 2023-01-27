#  coding: utf-8 
import socketserver
import pickle

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Alim Dhanani (January 2023)
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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        header = self.data.decode('utf-8').split('\n')
        list_of_filename = header[0].split()
        method = list_of_filename[0]
        if method != "GET":
            self.request.sendall(bytearray("HTTP/1.0 405 Method Not Allowed\r\n", 'utf-8'))
            return
        filename = list_of_filename[1]
        filepath = "Not Found"
        if filename[0] == "/": 
            filename = filename[1:]
            if not filename:
                filepath = "www/index.html"
            elif filename == "index.html":
                filepath = "www/index.html"
            elif filename == "base.css":
                filepath = "www/base.css"
            
            elif filename[:4] == "deep":
                filename = filename[5:]
                if not filename:
                    filepath = "www/deep/index.html"
                elif filename == "index.html":
                    filepath = "www/deep/index.html"
                elif filename == "deep.css":
                    filepath = "www/deep/deep.css"
                
   

        file_data = ""
        try:
            file = open(filepath, 'rb')
            file_data = file.read().decode('utf-8')
            file.close()
            content_type = "text/html"
            if filename.endswith(".css"):
                content_type = "text/css"
            response = 'HTTP/1.0 200 OK\r\n' +content_type + file_data
            response = f"HTTP/1.0 200 OK\r\nContent-Type:{content_type}; charset=utf-8\r\nContent-Length:{len(file_data)}\r\n\r\n{file_data}"
            
            
            self.request.sendall(bytearray(response,'utf-8', ))
            return
        except FileNotFoundError:
            self.request.sendall(bytearray('HTTP/1.0 404 Not Found\r\n','utf-8'))
            return
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    with socketserver.TCPServer((HOST, PORT), MyWebServer) as server:
        
        print("Listening on port 8080")
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    
