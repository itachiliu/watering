from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 发送响应状态码
        self.send_response(200)
        # 发送响应头
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # 发送响应内容
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting http server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()