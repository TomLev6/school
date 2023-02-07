import logging
from collections import defaultdict
from flask import request, Flask


def log_blocked_request(ip_address):
    logging.warning(f"Blocked request from IP address: {ip_address}")


app = Flask(__name__)


@app.route("/")
def serve_request():
    return "Hello, World!"


def get_request_ip_address(request):
    return request.remote_addr


ip_counts = defaultdict(int)


def handle_request(ip_address):
    ip_counts[ip_address] += 1
    if ip_counts[ip_address] > 100:
        return False
    else:
        return True


def test_request(url):
    with app.test_request_context(url):
        ip_address = get_request_ip_address(request)
        if handle_request(ip_address):
            result = serve_request()
            print(f"Allowed request: {result}")
        else:
            log_blocked_request(ip_address)
            print(f"Blocked request from IP address: {ip_address}")


if __name__ == "__main__":
    for i in range(1, 150):
        test_request("http://localhost")
