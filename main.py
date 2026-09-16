# This main script gets called when the chrome extension sends a message.

import os
import sys
import json
from src.notifier import sendNotification
from src.unzipper import unzip, move
from src.communicator import read, write
from src.configManager import evalDownload

# Communicating with chrome extension.
try:
  incomingMessage = sys.stdin.buffer.read(4)

  if incomingMessage:
    incomingMessage = read(incomingMessage)

    # Chrome extension has pinged native to test for a connection.
    if incomingMessage.get("action") == "ping":
      write(json.dumps({"status": "connected"}))

    # Chrome extension needs to evaluate a file. (Standard)
    elif incomingMessage.get("action") == "evaluate":
      filePath = incomingMessage.get("filePath")
      url = incomingMessage.get("url")
      fileType = incomingMessage.get("fileType")
      fileName = os.path.splitext(os.path.basename(filePath))[0]

      readSuccess, readError, fileDestination, unzipRule = evalDownload(url, filePath)
      if readSuccess:
        if unzipRule and fileType == ".zip":
          success, realPath = unzip(filePath, fileDestination)
          if success:
            realName = os.path.splitext(os.path.basename(realPath))[0]
            realDir = os.path.splitext(os.path.basename(os.path.dirname(realPath)))[0]
            sendNotification("Evaluation Complete", f'File "{realName}" from "{url}" successfully moved and unzipped to {realDir}".')
            write(json.dumps({"status": "Evaluation complete"}))
          else:
            sendNotification("Evaluation Failed", f'File "{fileName}" from "{url}" has encountered an error!')
            write(json.dumps({"status": "Evaluation failed"}))

        else:
          success, realPath = move(filePath, fileDestination)
          if success:
            realName = os.path.splitext(os.path.basename(realPath))[0]
            realDir = os.path.splitext(os.path.basename(os.path.dirname(realPath)))[0]
            sendNotification("Evaluation Complete", f'File "{realName}" from "{url}" successfully moved to {realDir}".')
            write(json.dumps({"status": "Evaluation complete"}))
          else:
            sendNotification("Evaluation Failed", f'File "{fileName}" from "{url}" has encountered an error!')
            write(json.dumps({"status": "Evaluation failed"}))
              
      else:
          write(json.dumps({"status": f"{readError}"}))
    else:
        write(json.dumps({"status": "URL mismatch"}))
  else:
      write(json.dumps("unhandeled action recieved, skipping."))

except Exception:
  sys.exit(1)