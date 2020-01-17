#!/usr/bin/env python3
#  coding: utf-8 
import socketserver
import os

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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        header = self.data.decode().split('\n')
        print("HEADER: " , header)
        
        req = header[0].split(" ")
        if req[0] == "GET":
            
            url = os.getcwd() + "/www" + req[1]
            print("URL", url)            
         
            if os.path.isfile(url):
                file_type = url.split(".")[-1]
                print("FILE TYPE =" + file_type)
                if file_type == "css" or file_type == "html":
                    send = bytearray(req[2][:-1] + " 200 OK\r\nContent-Type:text/" + file_type + "\r\n\r\n" + url,"utf-8")
                else:
                    send = bytearray(req[2][:-1] + " 404 Not Found\r\n\r\n", "utf-8")
                       
            elif req[1].endswith("/") and os.path.isdir(url):
                url = url + "index.html"
                send = bytearray(req[2][:-1] + " 200 OK\r\nLocation: http://127.0.0.1:8080/\r\nContent-Type:text/html\r\n\r\n" + url,"utf-8")
                
            elif req[1][-1].isalpha() and os.path.isdir(url):
                url = url + "/index.html"
                send = bytearray(req[2][:-1] + " 301 Moved Permanently\r\nLocation: http://127.0.0.1:8080/deep/" + "\r\n\r\n" ,"utf-8")
                
            else:
                send = bytearray(req[2][:-1] + " 404 Not Found\r\n\r\n", "utf-8")

        else:
            send = bytearray(req[2][:-1] + " 405 Method Not Allowed\r\n\r\n", "utf-8")


        self.request.sendall(send)
        
        

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    
    
