import re
import socket
import os

SERVER_ROOT = os.path.abspath("./public")
STATUSES = {
    "200": "OK",
    "404": "Not Found",
    "403": "Forbidden",
    "500": "Server Error",
}
MIME_TYPES = {
    ".txt": "text/plain",
    ".html": "text/html",
    ".pdf": "application/pdf",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
}

def main(port=25600):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('', port)
    s.bind(address)
    s.listen()
    # Needs to run forever!!
    while (True):
        new_connection = s.accept()
        new_socket = new_connection[0]
        req = new_socket.recv(1024)
        request = req.decode("ISO-8859-1")
        while ("\r\n\r\n" not in req.decode()):
            req = new_socket.recv(1024)
            request += req.decode("ISO-8859-1")
        print(request)
        start_line = request.split('\r\n')[0].split(' ')
        print(start_line)
        if start_line[0] == "GET":
            file_path = os.path.abspath(os.path.sep.join([SERVER_ROOT, start_line[1]]))
            if file_path.startswith(SERVER_ROOT):
                file_path = add_index_to_filepath(file_path)
                extension = os.path.splitext(file_path)[-1]
                content_type = MIME_TYPES[extension]
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        response = construct_response("200", content, content_type)
                except:
                    # send 404
                    print("404 Not Found")
                    content = "not found"
                    response = construct_response("404", content)
            else:
                # send 403
                print("403 Forbidden")
                content = "forbidden"
                response = construct_response("403", content)
        
        headers = parse_request_and_get_headers(request)
        # print(content)
        new_socket.sendall(response.encode("ISO-8859-1"))
        new_socket.close()

def parse_request_and_get_headers(request):
    headers = {}
    pattern = re.compile(r'(.+?): (.+?)\r\n')
    matches = re.findall(pattern, request)
    for match in matches:
        headers[match[0]] = match[1]
    return headers

def add_index_to_filepath(path):
    # check if the file_path ends with .html or a trailing slash?
    if not path.endswith('.html'):
        if path.endswith('/'): 
            path += 'index.html'
        else:
            path += '/index.html'
    return path

def construct_404_response():
    return ("HTTP/1.1 404 Not Found\r\n" +
            "Content-Type: text/plain\r\n" +
            "Content-Length: 13\r\n" +
            "Connection: close\r\n" +
            "\r\n\r\n" +
            "404 not found\r\n")

def construct_response(status_code, content, content_type="text/plain"):
    return (f"HTTP/1.1 {status_code} {STATUSES[status_code]}\r\n" + 
            f"Content-Type: {content_type}\r\n" + 
            f"Content-Length: {len(content)}\r\n" + 
            f"Connection: close\r\n\r\n{content}\r\n\r\n");

try:
    main()
except KeyboardInterrupt:
        print("Server shutting down! Bye bye!")