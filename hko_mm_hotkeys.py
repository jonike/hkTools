import os

from maya import cmds


def getScripts():
    scriptsDir = getScriptsDir()
    dirItemList = os.listdir(scriptsDir)

    scripts = []
    for dirItem in dirItemList:
        if dirItem.endswith(".py"):
            scripts.append([dirItem.split(".")[0], os.path.join(scriptsDir, dirItem), "python"])
        if dirItem.endswith(".mel"):
            scripts.append([dirItem.split(".")[0], os.path.join(scriptsDir, dirItem), "mel"])
    
    return scripts


def getCommand(scriptPath):
    with open(scriptPath, "r") as f:
        data = f.read()
    
    return data


def getScriptsDir():
    currentDir = os.path.dirname(__file__)
    scriptsDir = os.path.join(currentDir, "scripts")
    return scriptsDir


def main():
    scripts = getScripts()
    for script in scripts:
        name, scriptPath, commandLanguage = script
        if cmds.runTimeCommand(name, q=True, exists=True):
            cmds.runTimeCommand(name, e=True, delete=True)
        
        cmds.runTimeCommand(
                            name,
                            category="Custom Scripts",
                            hotkeyCtx="",
                            commandLanguage=commandLanguage,
                            command=getCommand(scriptPath)
                            )


main()