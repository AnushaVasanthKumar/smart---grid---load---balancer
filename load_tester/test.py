import requests
import threading
import time
import random

CHARGE_ENDPOINT = "http://localhost:8080/charge"  # charge_request_service

def simulate_ev(i):
    try:
        res = requests.post(CHARGE_ENDPOINT)
        print(f"EV {i} → {res.status_code}: {res.text}")
    except Exception as e:
        print(f"EV {i} → Failed: {e}")

if __name__ == "__main__":
    num_requests = 30  # simulate 30 cars
    threads = []
    for i in range(num_requests):
        t = threading.Thread(target=simulate_ev, args=(i,))
        t.start()
        threads.append(t)
        time.sleep(random.uniform(0.2, 1.0))  # simulate burst pattern

    for t in threads:
        t.join()

