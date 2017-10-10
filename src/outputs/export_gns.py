import json 
from collections import defaultdict

def export(data, path):
    
    data_format = defaultdict(list)

    for server in data:
        game = server["game"]
        data_format[game].append(server)
    

    with open(path,"w+") as f:
        json.dump(data_format,f, indent=2, sort_keys=True)



