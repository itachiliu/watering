from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# 用于保存最近一次上传的信息
latest_data = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/hello.txt":
            try:
                with open("hello.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"hello.txt not found")
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html lang="zh-cn">
        <head>
            <meta charset="utf-8">
            <title>AI自动灌溉系统数据展示</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
        <div class="container mt-5">
            <h1 class="mb-4 text-primary">欢迎来到张康硕的基于AI的自动灌溉系统!</h1>
        """
        if "humidity" in latest_data:
            html += f"""
            <div class="card shadow-sm">
                <div class="card-header bg-success text-white">
                    最近上传的湿度
                </div>
                <div class="card-body">
                    <table class="table table-bordered table-striped">
                        <tr><th>湿度</th><td>{latest_data['humidity']}</td></tr>
                    </table>
                </div>
            </div>
            """
        else:
            html += '<div class="alert alert-warning mt-4">暂无上传数据。</div>'
        html += """
        </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        global latest_data
        if self.path == "/humidity":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                params = parse_qs(post_data)
                if "humidity" not in params or not params["humidity"]:
                    raise ValueError("Missing field: humidity")
                humidity = params["humidity"][0]
                latest_data = {"humidity": humidity}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "success",
                    "received_humidity": humidity
                }
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting http server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()