#This main script gets called when the chrome extension sends a message.

import os
import sys
import json
from src.notifier import sendNotification
from src.unzipper import unzip
from src.communicator import read, write
targetURL = "https://cad.onshape.com"
targetFolder = os.path.join(os.path.expanduser("~"), "3D Objects")

#Communicating with chrome extension.
try:
  incomingMessage = sys.stdin.buffer.read(4)

  if incomingMessage:
    incomingMessage = read(incomingMessage)

    #Chrome extension has pinged native to test for a connection
    if incomingMessage.get("action") == "ping":
      write(json.dumps({"status": "connected"}))

    #Chrome extension has pinged native to 
    elif incomingMessage.get("action") == "unzip":
      filePath = incomingMessage.get("filePath")
      url = incomingMessage.get("url")
      zipName = os.path.splitext(os.path.basename(filePath))[0]

      if url == targetURL:
        success, realPath = unzip(filePath, targetFolder)

        if success:
          realName = os.path.splitext(os.path.basename(realPath))[0]
          sendNotification("Extraction Complete", f'Zip file "{zipName}" from "{url}" has been extracted into "{targetFolder}".')
          write(json.dumps({"status": "extraction complete", "new path": realPath, "target folder": targetFolder}))
        else:
          sendNotification("Extraction Failed", f'Zip file "{zipName}" from "{url}" has encountered an error!')
          write(json.dumps({"status": "extraction failed", "zip path": filePath}))
      else:
        write(json.dumps({"status": "URL mismatch"}))
    else:
      write(json.dumps("unhandeled action recieved, skipping."))

except Exception:
  sys.exit(1)