from flask import Flask, render_template_string
import joblib
import os
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

# ---------------- MODEL ---------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "model", "model.pkl")
model = joblib.load(model_path)

# ---------------- THINGSPEAK CONFIG ---------------- #
CHANNEL_ID = "3328334"
READ_API_KEY = "XPWN1DY9G7PWL0VV"

def get_sensor_data():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}&results=1"
    response = requests.get(url)
    data = pd.read_csv(StringIO(response.text))

    latest = data.iloc[-1]

    return {
        "temperature": latest.get("field1", 0),
        "humidity": latest.get("field2", 0),
        "voltage": latest.get("field3", 0)
    }

# ---------------- HOME PAGE ---------------- #
@app.route('/')
def home():

    sensor = get_sensor_data()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
    <title>IoT Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            color: white;
        }

        .container {
            text-align: center;
            padding: 30px;
        }

        .cards {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }

        .card {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 15px;
            width: 150px;
        }

        .value {
            font-size: 24px;
            font-weight: bold;
        }

        .btn {
            margin-top: 30px;
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            background: white;
            color: #333;
            cursor: pointer;
        }
    </style>
    </head>

    <body>

    <div class="container">
        <h1>⚡ IoT Smart Energy Dashboard</h1>

        <div class="cards">
            <div class="card">
                <h3>🌡 Temp</h3>
                <div class="value">{{ temp }}</div>
            </div>

            <div class="card">
                <h3>💧 Humidity</h3>
                <div class="value">{{ hum }}</div>
            </div>

            <div class="card">
                <h3>⚡ Voltage</h3>
                <div class="value">{{ volt }}</div>
            </div>
        </div>

        <a href="/predict">
            <button class="btn">Predict Energy</button>
        </a>
    </div>

    </body>
    </html>
    """, temp=sensor["temperature"], hum=sensor["humidity"], volt=sensor["voltage"])


# ---------------- PREDICTION PAGE ---------------- #
@app.route('/predict')
def predict():

    sensor = get_sensor_data()

    input_data = [[sensor["temperature"], sensor["humidity"], sensor["voltage"]]]
    prediction = model.predict(input_data)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Prediction</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
        }

        .card {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
        }

        .result {
            font-size: 30px;
            color: #00ffcc;
            margin: 20px;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            background: #00ffcc;
            cursor: pointer;
        }
    </style>
    </head>

    <body>

    <div class="card">
        <h1>⚡ Energy Prediction</h1>

        <p>Temp: {{ temp }} | Humidity: {{ hum }} | Voltage: {{ volt }}</p>

        <div class="result">{{ result }}</div>

        <a href="/"><button class="btn">Back</button></a>
    </div>

    </body>
    </html>
    """,
    result=prediction[0],
    temp=sensor["temperature"],
    hum=sensor["humidity"],
    volt=sensor["voltage"]
    )


if __name__ == "__main__":
    app.run(debug=True)