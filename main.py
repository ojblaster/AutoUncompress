# This main script gets called when the chrome extension sends a message.

import os
import sys
import json
from src.notifier import sendNotification
from src.unzipper import unzip, move
from src.communicator import read, write
from src.configManager import readData

def writeChrome(status, fileType=None, filePath=None):
  workingTable = {}
  if status: workingTable["status"] = status
  if fileType: workingTable["fileType"] = fileType
  if filePath: workingTable["filePath"] = filePath

  write(json.dumps(workingTable))

def getPretty(path):
  realName = os.path.splitext(os.path.basename(path))[0]
  realDir = os.path.splitext(os.path.basename(os.path.dirname(path)))[0]
  return realName, realDir

class CleanExit(Exception):
  pass

# Communicating with chrome extension.
try:
  incomingMessage = sys.stdin.buffer.read(4)

  if incomingMessage:
    incomingMessage = read(incomingMessage)

    # Chrome extension has pinged native to test for a connection.
    if incomingMessage.get("action") == "ping":
      writeChrome("connected")
      raise CleanExit

    # Chrome extension needs to evaluate a file. (Standard)
    elif incomingMessage.get("action") == "evaluate":
      filePath:str = incomingMessage.get("filePath")
      url:str = incomingMessage.get("url")
      fileType:str = incomingMessage.get("fileType")

      readSuccess, unzipRule, fileDestination = readData(url, filePath, fileType)
      if not readSuccess:
        writeChrome("read fail")
        raise CleanExit
      #Zip file and we want to unzip
      if unzipRule and fileType == ".zip":
        success, realPath = unzip(filePath, fileDestination)
        if success:
          realName, realDir = getPretty(realPath)
          writeChrome("complete", fileType, realPath)
        else:
          writeChrome("failed")

      #Not a zip file or we just dont want to unzip it
      else:
        success, realPath = move(filePath, fileDestination)
        if success:
          realName, realDir = getPretty(realPath)
          writeChrome("complete", fileType, realPath)
        else:
          writeChrome("failed")
    else:
      writeChrome("unhandled action")
  else:
    raise Exception

except CleanExit:
  pass

except Exception:
  sys.exit(1)