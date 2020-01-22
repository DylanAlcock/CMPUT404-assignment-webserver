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
        #print ("Got a request of: %s\n" % self.data)

        header = self.data.decode().split('\n')
        
        req = header[0].split(" ")
        if req[0] == "GET":
            
            #Get the path of the request
            url = "./www" + req[1]
            #print("URL", url)
         
            #if the path leads to a file, set the the FILE_TYPE and send 200 OK 
            # if the path doesnt try to move up directories
            if os.path.isfile(url):
                file_type = url.split(".")[-1]
                
                #Check if url tries to move up directories if so return 404 error
                if "/../" not in url:
                    page = open(url, 'rb').read()
                    content_length = str(len(page))
                    send = bytearray(req[2][:-1] + " 200 OK\r\nContent-Type:text/" + file_type + "\r\n" + "Content-length:"+ content_length + "\r\n\r\n","utf-8")
                    
                else:
                    page  = "<!DOCTYPE html>\n<html><body>HTTP/1.1 404 Path Not Found</body></html>"
                    content_length = str(len(page))
                    send = bytearray(req[2][:-1] + " 404 Not Found\r\nContent-Type: text/html\r\nContent-Length:" + content_length + "\r\n\r\n", "utf-8")
                    page = page.encode()
                       
            #if the path is a directory and has / at the end, open index.html at that directory           
            elif req[1].endswith("/") and os.path.isdir(url):
                url = url + "index.html"
                page = open(url, 'rb').read()
                content_length = str(len(page))
                send = bytearray(req[2][:-1] + " 200 OK\r\nLocation: http://127.0.0.1:8080/\r\nContent-Type:text/html\r\nContent-Length:" + content_length + "\r\n\r\n","utf-8")
                
            #If the path is a directory and doesn't have a / at the end 
            # add a / to the path and open index.html at that directory    
            elif req[1][-1].isalpha() and os.path.isdir(url):
                url = url + "/index.html"
                page = open(url, 'rb').read()
                #print(page)
                content_length = str(len(page))                 
                send = bytearray(req[2][:-1] + " 301 Moved Permanently\r\nLocation: http://127.0.0.1:8080" + req[1] + "/\r\n\r\n", "utf-8")               
                
            #If path is not a file or directory return 404 error
            else:
                page  = "<!DOCTYPE html>\n<html><body>HTTP/1.1 404 Path Not Found "+ url+ "</body></html>"
                content_length = str(len(page)) 
                send = bytearray(req[2][:-1] + " 404 Not Found\r\nContent-Type: text/html\r\nContent-Length:" + content_length + "\r\n\r\n", "utf-8")
                page = page.encode()

        #If request is not a GET return a 405 error
        else:
            page  = "<!DOCTYPE html>\n<html><body>HTTP/1.1 405 Method Not Allowed "+ req[0] + "</body></html>"
            content_length = str(len(page)) 
            send = bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\nContent-Length:" + content_length + "\r\n\r\n<", "utf-8")
            page = page.encode()

        #Send the response and the page
        self.request.send(send)
        self.request.send(page)
        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    
