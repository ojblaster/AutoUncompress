import json
import os
from urllib.parse import urlparse

defaultConfig = {
    "version": "1.0",
    "default_destination": None,
    "rules": {
        "cad.onshape.com": {
            "unzip": True,
            "destination": None,
            "fileDests": {
                ".stl": "ofl"
            }
        }
    }
}

src = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(src)
configPath = os.path.join(root, "config.json")

def loadConfig():
    if not os.path.exists(configPath):
        with open(configPath, "w", encoding="utf-8") as f:
            json.dump(defaultConfig, f, indent=2)
        return defaultConfig
    else:
        with open(configPath, "r", encoding="utf-8") as f:
            return json.load(f)

def getDestination(file, rules:dict, fileType):
    dest = rules.get("destination")
    orginDir = os.path.dirname(file)
    fileTypes:dict = rules.get("fileTypes", {})
    destForType = fileTypes.get(fileType)

    if destForType: dest = destForType

    if not dest or dest == "ofl" or not os.path.exists(dest):
        return orginDir
    else: return dest

def readData(url, originFilePath, fileType) -> tuple[bool, bool, str]:
    config = loadConfig()
    domain:str = urlparse(url).netloc
    rules:dict = config.get("rules", {}).get(domain)

    if not rules:
        return False, False, None
    try:
        unzip = rules.get("unzip", False)

        destination = rules.get("destination")
    
        destination = getDestination(originFilePath, rules, fileType)
        return True, unzip, destination
    except:
        return False, False, None