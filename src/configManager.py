import json
import os
from urllib.parse import urlparse

defaultConfig = {
    "version": "1.0",
    "default_destination": None,
    "rules": {
        "cad.onshape.com": {
            "unzip": True,
            "destination": None
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

def evalDownload(url, originFilePath) -> tuple[bool, str, str, bool]:
    config = loadConfig()
    domain = urlparse(url).netloc
    rules = config.get("rules", {}).get(domain)

    if not rules:
        return False, "Rules do not exist for domain", None, False
    
    unzip = rules.get("unzip", {}) or False
 
    destination = (rules.get("destination") or config.get("default_destination")) or None
    if destination == "origin file location" or not destination or not os.path.exists(destination):
        destination = os.path.dirname(originFilePath)

    return True, "Evaluated Successfully.", destination, unzip