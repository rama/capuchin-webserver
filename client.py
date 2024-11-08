import socket
import sys


def main(host, port=80):
    s = socket.socket()
    port = int(port)
    server_address = (host, port)
    s.connect(server_address)
    request = (
        f"GET / HTTP/1.1\r\nHost: {host}"
        + (f":{port}" if port else "")
        + "\r\nConnection: close\r\n\r\n"
    )
    s.sendall(request.encode("utf-8"))
    r = s.recv(4096)
    response = r
    while len(r := s.recv(4096)) != 0:
        r = s.recv(4096)
        response += r
    print(response.decode("utf-8"))
    s.close()


if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
else:
    main(sys.argv[1])
