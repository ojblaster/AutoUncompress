import json
import os
import winreg

projectRoot = os.path.dirname(os.path.abspath(__file__))
programPath = os.path.join(projectRoot, "programStart.bat")
manifestPath = os.path.join(projectRoot, "hostManifest.json")

extensionID = "cidlolodppkneidgbijpblmnjnobmfjj"
hostName = "com.auto_uncompress.host"

# 1. Generate host_manifest.json
manifestData = {
    "name": hostName,
    "description": "Auto Unzipper Native Messaging Host",
    "path": programPath,
    "type": "stdio",
    "allowed_origins": [f"chrome-extension://{extensionID}/"],
}

with open(manifestPath, "w", encoding="utf-8") as f:
  json.dump(manifestData, f, indent=2)

print(f"Generated manifest at: {manifestPath}")

# 2. Register into Windows Registry
registryPath = rf"Software\Google\Chrome\NativeMessagingHosts\{hostName}"
try:
  key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registryPath)
  winreg.SetValue(key, "", winreg.REG_SZ, manifestPath)
  winreg.CloseKey(key)
  print("Successfully registered host in Windows Registry! Registered at " + registryPath)
except Exception as e:
  print(f"Failed to write registry entry: {e}")