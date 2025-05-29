import http.client

def fetch_homepage(server='localhost', port=8080):
    conn = http.client.HTTPConnection(server, port)
    conn.request("GET", "/")
    response = conn.getresponse()
    print("Status:", response.status)
    print("Reason:", response.reason)
    data = response.read()
    print("Response body:", data.decode())
    conn.close()

if __name__ == "__main__":
    fetch_homepage()