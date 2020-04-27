# Shout out to Vasil Shotarov for the great article about creating custom shelf with python.
# https://bindpose.com/scripting-custom-shelf-in-maya-python/
# https://gist.github.com/vshotarov/1c3176fe9e38dcaadd1e56c2f15c95d9


import os
import re

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


def getShelfNamePathLang():
    shelfDir = getShelfDir()
    dirItemList = os.listdir(shelfDir)

    shelfNamePathLang = []
    for dirItem in dirItemList:
        if dirItem.endswith(".py"):
            shelfNamePathLang.append([dirItem.split(".")[0], os.path.join(shelfDir, dirItem), "python"])
        if dirItem.endswith(".mel"):
            shelfNamePathLang.append([dirItem.split(".")[0], os.path.join(shelfDir, dirItem), "mel"])

    return shelfNamePathLang


def getCommand(scriptPath):
    with open(scriptPath, "r") as f:
        data = f.read()
    return data


def getRunTimeCommandDir():
    currentDir = os.path.dirname(__file__)
    runTimeCommandDir = os.path.join(currentDir, "scripts", "runTimeCommand")
    return runTimeCommandDir


def getShelfDir():
    currentDir = os.path.dirname(__file__)
    shelfDir = os.path.join(currentDir, "scripts", "shelf")
    return shelfDir


def createUpdateRunTimeCommand():
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

    cmds.confirmDialog(title="Run Time Command Results",message="{0}\n-----------------------\n{1}".format(updatedMsg, createdMsg))


def camel_case_split(str):
    """
    e.g. str = "mayaMatchmoveTools" >> ['maya', 'Matchmove', 'Tools']
    e.g. str = "MayaMatchmoveTools" >> ['Maya', 'Matchmove', 'Tools']
    """
    return re.findall(r'[a-zA-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)


def labelfy(name):
    strings = camel_case_split(name)
    labelName = '\n\n' + '\n'.join(strings)
    return labelName


def _null(*args):
    pass


class _shelf():
    '''A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf".'''

    def __init__(self, name="hkTools", iconPath=""):
        self.name = name

        self.iconPath = iconPath

        self.labelBackground = (0, 0, 0, 1)
        self.labelColour = (.9, .9, .9)

        self._cleanOldShelf()
        cmds.setParent(self.name)
        self.build()

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def addButon(self, label, icon="commandButton.png", command=_null, doubleCommand=_null, sourceType=_null):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        cmds.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        cmds.shelfButton(image=icon, l=label, command=command, dcc=doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColour, stp=sourceType, noDefaultPopup=True)

    def addSeparator(self):
        cmds.separator(enable=True, width=24, height=31, manage=True, visible=True, style="shelf", horizontal=False)

    def addMenuItem(self, parent, label, command=_null, icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, l=label, c=command, i="")

    def addSubMenu(self, parent, label, icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, l=label, i=icon, subMenu=1)


    def _cleanOldShelf(self):
        '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
        if cmds.shelfLayout(self.name, ex=1):
            if cmds.shelfLayout(self.name, q=1, ca=1):
                for each in cmds.shelfLayout(self.name, q=1, ca=1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p="ShelfLayout")


class customShelf(_shelf):
    def build(self):
        self.shelfNamePathLangs = getShelfNamePathLang()
        for shelfNamePathLang in self.shelfNamePathLangs:
            name, path, commandLanguage = shelfNamePathLang
            labelName = labelfy(name).upper()
            self.addButon(label=labelName, sourceType=commandLanguage, command=getCommand(path))

        # Add shelf buttons manually from this point...

        self.addSeparator() # Add separator

        self.addButon(label="", icon="parentConstraint.png", sourceType="mel", command="ParentConstraintOptions")
        self.addButon(label="", icon="posConstraint.png", sourceType="mel", command="PointConstraintOptions")
        self.addButon(label="", icon="orientConstraint.png", sourceType="mel", command="OrientConstraintOptions")

        self.addSeparator()

        self.addButon(label="", icon="motionTrail.png", sourceType="mel", command="CreateMotionTrailOptions")
        self.addButon(label="", icon="bakeAnimation.png", sourceType="mel", command="BakeSimulationOptions")

        self.addSeparator()

        self.addButon(label="", icon="locator.png", sourceType="mel", command="CreateLocator")
        self.addButon(label="", icon="cluster.png", sourceType="mel", command="CreateClusterOptions")


def createUpdateShelf():
    customShelf()
    return


def main():
    createUpdateRunTimeCommand()
    createUpdateShelf()
