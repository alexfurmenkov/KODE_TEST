import argparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from subscriber import Subscriber


class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = f"{message}"
        return content.encode("utf8")

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("GET!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_encoded_data = post_data.decode('utf-8')
        decoded_data = json.loads(json_encoded_data)
        Subscriber.addSubscriber(decoded_data)

        self._set_headers()
        self.wfile.write(self._html(post_data))

    def do_DELETE(self):
        content_length = int(self.headers['Content-Length'])
        delete_data = self.rfile.read(content_length)
        json_encoded_data = delete_data.decode('utf-8')
        decoded_data_delete = json.loads(json_encoded_data)
        self._set_headers()
        self.wfile.write(self._html(decoded_data_delete))
        Subscriber.delSubcriber(decoded_data_delete)


def run(server_class=HTTPServer, handler_class=Server, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Запуск сервера по адресу {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск HTTP сервера")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Уточните IP адрес",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Уточните порт",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
