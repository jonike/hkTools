import os

try:
    from maya import mel
    from maya import cmds
    isMaya = True
except ImportError:
    isMaya = False

def onMayaDroppedPythonFile(*args, **kwargs):
    pass


def _onMayaDropped():
    if isMaya:
        main()


def getRunTimeCommandNamePathLang():
    runTimeCommandDir = getRunTimeCommandDir()
    dirItemList = os.listdir(runTimeCommandDir)

    runTimeCommandNamePathLang = []
    for dirItem in dirItemList:
        if dirItem.endswith(".py"):
            runTimeCommandNamePathLang.append([dirItem.split(".")[0], os.path.join(runTimeCommandDir, dirItem), "python"])
        if dirItem.endswith(".mel"):
            runTimeCommandNamePathLang.append([dirItem.split(".")[0], os.path.join(runTimeCommandDir, dirItem), "mel"])

    return runTimeCommandNamePathLang


def getCommand(scriptPath):
    with open(scriptPath, "r") as f:
        data = f.read()
    return data


def getRunTimeCommandDir():
    currentDir = os.path.dirname(__file__)
    runTimeCommandDir = os.path.join(currentDir, "scripts", "runTimeCommand")
    return runTimeCommandDir


def registerRunTimeCommand():
    runTimeCommandNamePathLangs = getRunTimeCommandNamePathLang()
    updatedMsg = "\nUpdated...\n\n"
    createdMsg = "\nCreated...\n\n"
    for runTimeCommandNamePathLang in runTimeCommandNamePathLangs:
        name, path, commandLanguage = runTimeCommandNamePathLang
        if cmds.runTimeCommand(name, q=True, exists=True):
            cmds.runTimeCommand(name, e=True, delete=True)
            cmds.runTimeCommand(name, category="Custom Scripts", commandLanguage=commandLanguage, command=getCommand(path))
            updatedMsg += "'{}' runtime command\n".format(name)
        else:
            cmds.runTimeCommand(name, category="Custom Scripts", commandLanguage=commandLanguage, command=getCommand(path))
            createdMsg += "'{}' runtime command.\n".format(name)

    cmds.confirmDialog(title="Results",message="{0}\n-----------------------\n{1}".format(updatedMsg, createdMsg))


def main():
    registerRunTimeCommand()
