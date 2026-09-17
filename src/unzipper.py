import os
import zipfile
def renamePath(filePath:str):
  count = 1
  if os.path.isdir(filePath):
    originalPath = filePath
    while os.path.exists(filePath):
      filePath = f"{originalPath} ({count})"
      count += 1
    return filePath
  
  else:
    base, ext = os.path.splitext(filePath)
    newPath = filePath
    while os.path.exists(newPath):
      newPath = f"{base} ({count}){ext}"
      count += 1
    return newPath

def unzip(zipPath: str, targetDir: str) -> tuple[bool, str]:
  if not os.path.exists(zipPath) or not zipfile.is_zipfile(zipPath) or not os.path.isdir(targetDir):
    return False, ""

  try:
    zipName = os.path.splitext(os.path.basename(zipPath))[0]
    targetDir = os.path.join(targetDir, zipName)

    targetDir = renamePath(targetDir)

    os.makedirs(targetDir)

    with zipfile.ZipFile(zipPath, "r") as zipRef:
      zipRef.extractall(targetDir)

    os.remove(zipPath)
    return True, targetDir
  except Exception:
    return False, ""

def move(filePath: str, targetDir: str) -> tuple[bool, str]:
    if not os.path.exists(filePath) or not os.path.isdir(targetDir):
        return False, ""

    try:
        targetPath = os.path.join(targetDir, os.path.basename(filePath))
        targetPath = renamePath(targetPath)

        os.rename(filePath, targetPath)
        return True, targetPath
    except Exception:
        return False, ""