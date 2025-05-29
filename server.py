from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

AI_SERVICE_URL = "http://ai-service:5000/irrigate"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")

    def do_POST(self):
        if self.path == "/humidity":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                # 检查必需字段
                required_fields = ["humidity", "temperature", "light_intensity", "soil_type", "timestamp", "device_id"]
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Missing field: {field}")

                # 转发给AI服务
                ai_response = requests.post(AI_SERVICE_URL, json=data, timeout=5)
                ai_result = ai_response.json()

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