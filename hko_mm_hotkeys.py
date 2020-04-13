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
    main()


def getScriptNamePathLang():
    scriptsDir = getScriptsDir()
    dirItemList = os.listdir(scriptsDir)

    scriptNamePathLang = []
    for dirItem in dirItemList:
        if dirItem.endswith(".py"):
            scriptNamePathLang.append([dirItem.split(".")[0], os.path.join(scriptsDir, dirItem), "python"])
        if dirItem.endswith(".mel"):
            scriptNamePathLang.append([dirItem.split(".")[0], os.path.join(scriptsDir, dirItem), "mel"])

    return scriptNamePathLang


def getCommand(scriptPath):
    with open(scriptPath, "r") as f:
        data = f.read()
    return data


def getScriptsDir():
    currentDir = os.path.dirname(__file__)
    scriptsDir = os.path.join(currentDir, "scripts")
    return scriptsDir


def main():
    scriptNamePathLangs = getScriptNamePathLang()
    for scriptNamePathLang in scriptNamePathLangs:
        name, path, commandLanguage = scriptNamePathLang
        if cmds.runTimeCommand(name, q=True, exists=True):
            continue

        cmds.runTimeCommand(
                            name,
                            category="Custom Scripts",
                            commandLanguage=commandLanguage,
                            command=getCommand(path)
                            )
        print "Created '{}' runtime command.".format(name)


if isMaya:
    _onMayaDropped()
