import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from db.connection import Connection

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    db_connection: Connection = None

    def _write_response(self, response):
        json_data = json.dumps(response)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

    # pylint: disable=invalid-name
    def do_GET(self):
        if self.path == '/list':
            data = self.db_connection.list()
            self._write_response(data)

        elif self.path.startswith('/search'):
            query_components = parse_qs(urlparse(self.path).query)
            lastname = query_components.get('lastname', [''])[0]
            data = self.db_connection.search(lastname)
            self._write_response(data)

        elif self.path == '/info':
            data = {
                "git_commit_hash": os.environ.get('GIT_COMMIT_HASH', 'hash_not_set'),
            }
            self._write_response(data)

        else:
            self.send_response(404)
            self.end_headers()


def run(connection, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    if connection:
        handler_class.db_connection = connection

    httpd = None
    server_address = ('', port)

    try:
        httpd = server_class(server_address, handler_class)
        sys.stdout.write(f"Starting server on port {port}...\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("Server keyboard interrupted.\n")
    except OSError as e:
        sys.stderr.write(f"Server error: {e}\n")
    finally:
        if httpd:
            sys.stdout.write("Shutting down server...\n")
            httpd.shutdown()
