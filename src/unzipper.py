import os
import zipfile


def unzip(zipPath: str, targetDir: str) -> tuple[bool, str]:
  if not os.path.exists(zipPath) or not zipfile.is_zipfile(zipPath):
    return False, ""

  try:
    zipName = os.path.splitext(os.path.basename(zipPath))[0]
    targetDir = os.path.join(targetDir, zipName)

    originalDir = targetDir
    count = 1
    while os.path.exists(targetDir):
      targetDir = f"{originalDir} ({count})"
      count += 1

    os.makedirs(targetDir)

    with zipfile.ZipFile(zipPath, "r") as zipRef:
      zipRef.extractall(targetDir)

    os.remove(zipPath)
    return True, targetDir
  except Exception:
    return False, ""