import requests
import json
import time

# -------- CONFIG (CHANGE THESE) --------
TOMTOM_API_KEY = "YOUR_API_KEY_HERE"

LAT = "12.9756"
LON = "77.6050"

SPLUNK_HEC_URL = "https://YOUR_URL_.splunkcloud.com/services/collector"
SPLUNK_HEC_TOKEN = "YOUR_TOKEN_HERE"

INDEX = "traffic_blr"
SOURCETYPE = "traffic:tomtom"
# --------------------------------------

headers = {
    "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
    "Content-Type": "application/json"
}

tomtom_url = (
    "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    f"?key={TOMTOM_API_KEY}&point={LAT},{LON}"
)
response = requests.get(tomtom_url, timeout=100)
response.raise_for_status()

data = response.json()

flow = data.get("flowSegmentData", {})

event = {
    "event": {
        "city": "Bangalore",
        "latitude": LAT,
        "longitude": LON,
        "currentSpeed": flow.get("currentSpeed"),
        "freeFlowSpeed": flow.get("freeFlowSpeed"),
        "confidence": flow.get("confidence"),
        "roadClosure": flow.get("roadClosure")
    },
    "index": INDEX,
    "sourcetype": SOURCETYPE
}

splunk_response = requests.post(
    SPLUNK_HEC_URL,
    headers=headers,
    data=json.dumps(event),
    timeout=30
)

splunk_response.raise_for_status()

print("✔ TomTom event successfully sent to Splunk")
