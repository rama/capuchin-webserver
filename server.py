import re
import socket
import os

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

# x create a Server class
# x it can hold above constants
# x add a run method
# x not needed yet - add a setup method to choose port etc?
# x not needed yet - should i track state?
# maybe move to create_socket etc
# x method for now - parse request in separate class or method?
# TODO construct response - should response be a dataclass?
# TODO add pylint and mypy type annotations?


class Server:
    def __init__(self, port=25600, server_root="./public"):
        self.PORT = port
        self.self.SERVER_ROOT = os.path.abspath(server_root)
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = ("", self.PORT)
        self.socket.bind(address)

    def run(self):
        self.socket.listen()
        print("Server running...")

        while True:
            self._handle_request()

    def _handle_request(self):
        new_connection = self.socket.accept()
        new_socket = new_connection[0]
        req = new_socket.recv(1024)
        request = req.decode("ISO-8859-1")
        while "\r\n\r\n" not in req.decode():
            req = new_socket.recv(1024)
            request += req.decode("ISO-8859-1")
        print(request)
        start_line = request.split("\r\n")[0].split(" ")
        print(start_line)
        if start_line[0] == "GET":
            response = self._handle_get(start_line[1])

        # headers = parse_request_and_get_headers(request)
        new_socket.sendall(response.encode("ISO-8859-1"))
        new_socket.close()

    def _handle_get(self, target):
        file_path = os.path.abspath(os.path.sep.join([self.SERVER_ROOT, target]))
        # Make sure requested file is inside server_root
        if not file_path.startswith(self.SERVER_ROOT):
            print("403 Forbidden")
            content = "forbidden"
            return construct_response("403", content)

        file_path = add_index_to_filepath(file_path)
        extension = os.path.splitext(file_path)[-1]
        content_type = MIME_TYPES[extension]
        try:
            with open(file_path, "r") as f:
                content = f.read()
                return construct_response("200", content, content_type)
        except:
            print("404 Not Found")
            content = "not found"
            return construct_response("404", content)

    def stop(self):
        pass


def parse_request_and_get_headers(request):
    headers = {}
    pattern = re.compile(r"(.+?): (.+?)\r\n")
    matches = re.findall(pattern, request)
    for match in matches:
        headers[match[0]] = match[1]
    return headers


def add_index_to_filepath(path):
    # check if the file_path ends with .html or a trailing slash?
    if not path.endswith(".html"):
        if path.endswith("/"):
            path += "index.html"
        else:
            path += "/index.html"
    return path


def construct_response(status_code, content, content_type="text/plain"):
    return (
        f"HTTP/1.1 {status_code} {STATUSES[status_code]}\r\n"
        + f"Content-Type: {content_type}\r\n"
        + f"Content-Length: {len(content)}\r\n"
        + f"Connection: close\r\n\r\n{content}\r\n\r\n"
    )


def main():
    server = Server()
    server.run()


try:
    main()
except KeyboardInterrupt:
    print("Server shutting down! Bye bye!")
