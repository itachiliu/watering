from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from urllib.parse import parse_qs

from datetime import datetime

# 用于保存所有上传的信息
latest_data_list = []

def get_season(month):
    # 简单判断季节
    if month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    elif month in [9, 10, 11]:
        return "秋季"
    else:
        return "冬季"
# 日志配置
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# 用于保存最近一次上传的信息
latest_data = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"收到GET请求: {self.path}")
        if self.path == "/hello.txt":
            # ...existing code...
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

        if latest_data_list:
            html += """
            <div class="card shadow-sm">
                <div class="card-header bg-success text-white">
                    所有上传的湿度记录
                </div>
                <div class="card-body">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                <th>湿度</th>
                                <th>上传时间</th>
                                <th>季节</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            for item in reversed(latest_data_list):
                html += f"<tr><td>{item['humidity']}</td><td>{item['time']}</td><td>{item['season']}</td></tr>"
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
        logging.info("返回主页HTML页面")

    def do_POST(self):
        global latest_data_list
        logging.info(f"收到POST请求: {self.path}")
        if self.path == "/humidity":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            logging.info(f"POST数据: {post_data}")
            try:
                params = parse_qs(post_data)
                if "humidity" not in params or not params["humidity"]:
                    raise ValueError("Missing field: humidity")
                humidity = params["humidity"][0]
                now = datetime.now()
                time_str = now.strftime("%Y-%m-%d %H:%M:%S")
                season = get_season(now.month)
                record = {
                    "humidity": humidity,
                    "time": time_str,
                    "season": season
                }
                latest_data_list.append(record)
                logging.info(f"接收到湿度数据: {humidity}, 时间: {time_str}, 季节: {season}")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "success",
                    "received_humidity": humidity,
                    "time": time_str,
                    "season": season
                }
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                logging.error(f"处理POST请求出错: {e}")
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            logging.warning(f"未知POST路径: {self.path}")
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"启动HTTP服务器，端口: {port}")
    print(f"Starting http server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()