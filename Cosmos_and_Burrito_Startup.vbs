Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\HP\.gemini\antigravity\scratch\pixel_desktop_pet"
WshShell.Run "python desktop_pet_app.py", 0, False
