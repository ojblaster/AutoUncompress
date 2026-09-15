from plyer import notification

def sendNotification(title: str, message: str):
  notification.notify(
      title=title,
      message=message,
      app_name="Auto-Uncompress",
      timeout=5,
  )