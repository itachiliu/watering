from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

AI_SERVICE_URL = "http://ai-service:5000/irrigate"

# 用于保存最近一次上传的信息
latest_data = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')  # 指定utf-8编码
        self.end_headers()
        html = "<html><body><h1>欢迎来到张康硕的基于AI的自动灌溉系统!</h1>"
        if latest_data:
            html += "<h2>最近上传的信息：</h2>"
            html += "<table border='1' style='border-collapse:collapse;'>"
            html += "<tr><th>字段</th><th>值</th></tr>"
            for k, v in latest_data.items():
                html += f"<tr><td>{k}</td><td>{v}</td></tr>"
            html += "</table>"
        else:
            html += "<p>暂无上传数据。</p>"
        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))  # 用utf-8编码

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