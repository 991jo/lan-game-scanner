import json 

def export(data, path):
    with open(path,"w+") as f:
        json.dump(data,f, indent=2, sort_keys=True)



