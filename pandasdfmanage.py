import pandas as pd  # read csv, df manipulation
import datetime

import requests

telemetry = requests.get('http://192.168.4.1')
print(telemetry.text)
#print(telemetry.json())

telemetryjson=telemetry.json()
telemetryjson.update({"time":datetime.datetime.utcnow().isoformat()})
print(telemetryjson)

#debug use
#telemetryjson={'Current Lat': 0.0, 'Current Long': 0.0, 'Home Lat': 0.0, 'Home Long': 0.0, 'Current Hdg': 237.674438, 'Target Hdg': 0.0, 'Current vel': 0.0, 'Target vel': 0.0, 'Current Motor Setting': 0.0, 'Rudder Config Var': -72.325562}

telemdf = pd.DataFrame(telemetryjson, index=[datetime.datetime.now().isoformat()])
#print(telemdf.to_string())

while True:
    telemetry = requests.get('http://192.168.4.1')
    print(telemetry.text)
    # print(telemetry.json())

    telemetryjson = telemetry.json()
    telemetryjson.update({"time": datetime.datetime.utcnow().isoformat()})

    tobeappended=pd.DataFrame(telemetryjson, index=[datetime.datetime.now().isoformat()])
    telemdf=pd.concat([telemdf,tobeappended],ignore_index=True)
    print(telemdf.to_string())
    .time.sleep(0.3)
