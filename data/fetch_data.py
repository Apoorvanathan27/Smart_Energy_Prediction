import pandas as pd
import requests
from io import StringIO

CHANNEL_ID = "3328334"
READ_API_KEY = "XPWN1DY9G7PWL0VV"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}&results=1000"

response = requests.get(url)

data = pd.read_csv(StringIO(response.text))

data.to_csv("data/energy_data.csv", index=False)

print("Data Saved Successfully")