import re
import socket
import os

SERVER_ROOT = os.path.abspath("./public")

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
            file_path = convert_to_file_path(start_line[1])
            if file_path.startsWith(SERVER_ROOT):
                content = get_file_content(start_line[1])
        headers = parse_request_and_get_headers(request)
        print(headers)
        response = construct_response(content)
        new_socket.sendall(response.encode("ISO-8859-1"))
        new_socket.close()

def parse_request_and_get_headers(request):
    headers = {}
    pattern = re.compile(r'(.+?): (.+?)\r\n')
    matches = re.findall(pattern, request)
    for match in matches:
        headers[match[0]] = match[1]
    return headers

def convert_to_file_path(request_path):
    file_path = os.path.abspath(os.path.sep.join(SERVER_ROOT, request_path))
    return file_path

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except:
        return construct_404_response()

def construct_404_response():
    return ("HTTP/1.1 404 Not Found\r\n" +
            "Content-Type: text/plain\r\n" +
            "Content-Length: 13\r\n" +
            "Connection: close\r\n" +
            "\r\n\r\n" +
            "404 not found\r\n")


def construct_response(content):
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n{content}\r\n\r\n";

try:
    main()
except KeyboardInterrupt:
        print("Server shutting down! Bye bye!")