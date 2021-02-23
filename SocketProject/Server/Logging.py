from os import system
from datetime import datetime

def startlog():
    system("touch log.log")
    system("echo Date Time FlagNum Flag % Comment > log.log")
    now = datetime.now()
    system("echo %s 8 [Info] %% Logging Start >> log.log"%now)

def log(flag, comment):
    system("touch log.log")

    now = datetime.now()
    flagList = ["[Err]","[Auth]","[FileIO]","","","","","","[Info]","[Test]"]

    system("echo %s %i %s %% %s >> log.log"%(now,flag,flagList[flag],comment))
