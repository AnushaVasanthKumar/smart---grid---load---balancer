from flask import Flask, request
import requests

app = Flask(__name__)

LOAD_BALANCER_URL = "http://load_balancer:5000/request_charge"

@app.route('/charge', methods=['POST'])
def handle_request():
    try:
        res = requests.post(LOAD_BALANCER_URL)
        return res.text, res.status_code
    except:
        return "Failed to reach load balancer", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

