from http.server import BaseHTTPRequestHandler, HTTPServer
import json

AI_SERVICE_URL = "http://ai-service:5000/irrigate"

# 用于保存最近一次上传的信息
latest_data = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
        if latest_data:
            html += """
            <div class="card shadow-sm">
                <div class="card-header bg-success text-white">
                    最近上传的信息
                </div>
                <div class="card-body">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr><th>字段</th><th>值</th></tr>
                        </thead>
                        <tbody>
            """
            for k, v in latest_data.items():
                html += f"<tr><td>{k}</td><td>{v}</td></tr>"
            html += """
                        </tbody>
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
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                required_fields = ["humidity", "temperature", "light_intensity", "soil_type", "timestamp", "device_id"]
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Missing field: {field}")

                latest_data = data  # 保存最新上传数据

                # 转发给AI服务
                # ai_response = requests.post(AI_SERVICE_URL, json=data, timeout=5)
                # ai_result = ai_response.json()
                ai_result = {"should_irrigate": True, "amount": 100}  # 测试用假数据

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "success",
                    "ai_decision": ai_result
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