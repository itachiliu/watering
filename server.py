from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
from urllib.parse import parse_qs
from deepseek import analyze_watering

# 日志配置
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# 用于保存最近一次上传的信息
latest_data = {}

import datetime
import pytz  # 需要安装 pytz 库
def get_season(month):
    if month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    elif month in [9, 10, 11]:
        return "秋季"
    else:
        return "冬季"
    
# 增加地理位置和植物种类
LOCATION = "南京"
PLANTS = ["薄荷", "花生", "大豆", "生菜", "小葱"]

# 每种植物的最新湿度数据
plant_data = {plant: {} for plant in PLANTS}
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"收到GET请求: {self.path}")
        if self.path == "/hello.txt":
            try:
                with open("hello.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                logging.info("成功返回hello.txt内容")
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"hello.txt not found")
                logging.warning("hello.txt未找到")
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"""
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
            <div class="mb-4"><strong>地理位置：</strong>{LOCATION}</div>
        """
        tz = pytz.timezone("Asia/Shanghai")
        now = datetime.datetime.now(tz)
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        season = get_season(now.month)
        if "humidity" in latest_data:
            for plant in PLANTS:
                analysis = analyze_watering(plant, latest_data['humidity'], time_str, season)
                html += f"""
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-info text-white">
                        {plant} 的最新湿度数据
                    </div>
                    <div class="card-body">
                        <table class="table table-bordered table-striped">
                            <tr><th>湿度</th><td>{latest_data['humidity']}</td></tr>
                            <tr><th>上传时间</th><td>{time_str}</td></tr>
                            <tr><th>季节</th><td>{season}</td></tr>
                        </table>
                        <div class="alert alert-secondary mt-3"><strong>AI分析：</strong>{analysis}</div>
                    </div>
                </div>
                """
        else:
            for plant in PLANTS:
                html += f"""
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-info text-white">
                        {plant} 的最新湿度数据
                    </div>
                    <div class="card-body">
                        <div class="alert alert-warning">暂无上传数据。</div>
                    </div>
                </div>
                """
        html += """
        </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
        logging.info("返回主页HTML页面")
    def do_POST(self):
        global latest_data
        logging.info(f"收到POST请求: {self.path}")
        if self.path == "/humidity":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            logging.info(f"POST数据: {post_data}")
            try:
                params = parse_qs(post_data)
                logging.info(f"post_data: {post_data}")
                logging.info(f"解析后的参数: {params}")
                if "humidity" not in params or not params["humidity"]:
                    raise ValueError("Missing field: humidity")
                humidity = params["humidity"][0]
                latest_data = {"humidity": humidity}
                logging.info(f"接收到湿度数据: {humidity}")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "success",
                    "received_humidity": humidity
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