from flask import Flask, request
import requests
import threading
import time

app = Flask(__name__)

# List of substation service URLs (Docker service names)
SUBSTATIONS = [
    "http://substation1:8000/metrics",
    "http://substation2:8000/metrics",
    "http://substation3:8000/metrics"
]

# Map of substation name to current load
load_map = {}

def update_loads():
    while True:
        for url in SUBSTATIONS:
            try:
                res = requests.get(url)
                for line in res.text.splitlines():
                    if "substation_current_load" in line:
                        load = float(line.split()[-1])
                        load_map[url] = load
            except:
                load_map[url] = float('inf')
        time.sleep(2)

@app.route('/request_charge', methods=['POST'])
def route_charge():
    if not load_map:
        return "Load data unavailable", 503
    best = min(load_map.items(), key=lambda x: x[1])[0]
    target = best.replace("/metrics", "/charge")
    try:
        res = requests.post(target)
        return f"Routed to: {target} | {res.text}", res.status_code
    except:
        return "Failed to route charge request", 500
    print("Load map:", load_map)

if __name__ == '__main__':
    threading.Thread(target=update_loads, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
