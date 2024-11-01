import os
### check if conf has WLAN detains
if "config.json" in os.listdir():
    import json
    conf = json.load(open("config.json"))   
 
