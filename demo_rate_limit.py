from flask import Flask, request, jsonify
from collections import defaultdict
import threading
import requests
import random
import time

app = Flask(__name__)

RATE_LIMIT = 8
WINDOW = 5

requests_log = defaultdict(list)
blocked_ips = set()


@app.route("/")
def home():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    now = time.time()

    if ip in blocked_ips:
        print(f"[BLOCKED] {ip}")
        return jsonify({"status": "blocked", "ip": ip})

    requests_log[ip] = [
        t for t in requests_log[ip]
        if now - t < WINDOW
    ]

    requests_log[ip].append(now)

    if len(requests_log[ip]) > RATE_LIMIT:
        blocked_ips.add(ip)
        print(f"[ALERT] Blocking IP: {ip}")
        return jsonify({"status": "blocked_due_to_rate_limit", "ip": ip})

    print(f"[OK] {ip} -> {len(requests_log[ip])} requests")
    return jsonify({"status": "allowed", "ip": ip})


def run_server():
    app.run(debug=False, use_reloader=False)


def run_simulator():
    time.sleep(1)

    url = "http://127.0.0.1:5000/"

    ips = [
        "192.168.1.10",
        "192.168.1.20",
        "10.0.0.5",
        "203.0.113.99"   # simulated abusive IP
    ]

    for i in range(40):
        if random.random() < 0.7:
            ip = "203.0.113.99"
        else:
            ip = random.choice(ips)

        headers = {"X-Forwarded-For": ip}

        try:
            response = requests.get(url, headers=headers)
            print(f"Client request from {ip}: {response.json()}")
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

        time.sleep(0.2)

    print("\nDemo finished.")
    print("Blocked IPs:", blocked_ips)


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    run_simulator()