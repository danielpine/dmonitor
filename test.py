import psutil
import json

for p in psutil.process_iter():
        j=p.as_dict()
        print(json.dumps(j,indent=2))