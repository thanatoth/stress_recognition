import json
from soracom import soracom

data = json.loads(soracom.getSoracom())

print(data)
print(data['lightSener'])
print(data['heartRate'])