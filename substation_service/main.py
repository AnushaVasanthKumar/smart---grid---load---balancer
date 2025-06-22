from flask import Flask, request
from prometheus_client import Gauge, generate_latest, start_http_server
import threading
import time

app = Flask(__name__)

# Global variables
current_load = 0
load_metric = Gauge('substation_current_load', 'Current load on the substation')

def update_metrics():
    load_metric.set(current_load)

@app.route('/charge', methods=['POST'])
def handle_charge():
    global current_load
    current_load += 1
    update_metrics()
    print("Charging started, load =", current_load)
    threading.Thread(target=simulate_charging).start()
    return 'Charging started', 200

def simulate_charging():
    global current_load
    time.sleep(5)  # Simulate a 5-second charge session
    current_load -= 1
    update_metrics()
    print("Charging complete, load =", current_load)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    update_metrics()
    start_http_server(9100)               # Prometheus will scrape here
    app.run(host='0.0.0.0', port=8000)    # Flask runs here
