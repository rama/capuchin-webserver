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
            #path = start_line[1].replace('/', '.', 1) 
            #print(path)
            path = "./index.html"
            with open(path, 'r') as f:
                content = f.read()
                print(len(content)) #is len in bytes???
        headers = parse_request_and_get_headers(request)
        print(headers)
        response = construct_response()
        new_socket.sendall(response.encode("ISO-8859-1"))
        new_socket.close()

def parse_request_and_get_headers(request):
    headers = {}
    pattern = re.compile(r'(.+?): (.+?)\r\n')
    matches = re.findall(pattern, request)
    for match in matches:
        headers[match[0]] = match[1]
    return headers

def construct_response():
    return "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 10\r\nConnection: close\r\n\r\nHi, there!\r\n\r\n";

try:
    main()
except KeyboardInterrupt:
        print("Server shutting down! Bye bye!")