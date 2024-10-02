import re
import socket

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
            path = "./public/" + start_line[1] + "/index.html"
            with open(path, 'r') as f:
                content = f.read()
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

def construct_response(content):
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n{content}\r\n\r\n";

try:
    main()
except KeyboardInterrupt:
        print("Server shutting down! Bye bye!")