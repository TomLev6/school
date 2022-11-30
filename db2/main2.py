import win32event
m2 = win32event.OpenMutex(win32event.SYNCHRONIZE, False, "MyMutex")
r2 = win32event.WaitForSingleObject(m2, -1)
