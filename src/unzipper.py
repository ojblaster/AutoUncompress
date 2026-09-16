import os
import zipfile
def renamePath(a):
  originalDir = a
  count = 1
  while os.path.exists(a):
    a = f"{originalDir} ({count})"
    count += 1
  return a

def unzip(zipPath: str, targetDir: str) -> tuple[bool, str]:
  if not os.path.exists(zipPath) or not zipfile.is_zipfile(zipPath):
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

def renameMovingFilePath(filePath: str) -> str:
    base, ext = os.path.splitext(filePath)
    count = 1
    newPath = filePath
    while os.path.exists(newPath):
        newPath = f"{base} ({count}){ext}"
        count += 1
    return newPath

def move(filePath: str, targetDir: str) -> tuple[bool, str]:
    if not os.path.isfile(filePath) or not os.path.isdir(targetDir):
        return False, ""

    try:
        targetPath = os.path.join(targetDir, os.path.basename(filePath))
        targetPath = renameMovingFilePath(targetPath)

        os.rename(filePath, targetPath)
        return True, targetPath
    except Exception:
        return False, ""