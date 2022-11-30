import win32event
m = win32event.CreateMutex(None, False, 'MyMutex')
r = win32event.WaitForSingleObject(m, 100)
win32event.ReleaseMutex(m)
