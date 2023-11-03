from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = 'xxx'

@app.route('/')
def mapview():
    return render_template('map.html', GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY)

@app.route('/send-location', methods=['POST'])
def send_location():
    data = request.json
    print("Location to send:", data.get('location'))
    print("Email to send to:", data.get('email'))
    return jsonify({"status": "success", "message": "Location sent to the recipient."})

@app.route('/calculate-eta', methods=['POST'])
def calculate_eta():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{origin['lat']},{origin['lng']}",
        "destinations": f"{destination['lat']},{destination['lng']}",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    eta_info = response.json()
    
    eta = eta_info['rows'][0]['elements'][0]['duration']['text']
    return jsonify({"status": "success", "eta": eta})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

