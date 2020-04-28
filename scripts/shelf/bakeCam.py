# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91

"""
import bakeCam
try:
    bc.close()
    bc.deleteLater()
except:
    pass
bc = bakeCam.BakeCam()
bc.show()
"""

import maya.cmds as mc
import maya.mel as mm
import maya.OpenMayaUI as omui

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    import shiboken
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken

import os
import re
from functools import wraps


# Decorator for undo support.
def openCloseChunk(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        action = None
        try:
            mc.undoInfo(openChunk=True)
            action = func(*args, **kargs)
        except:
            print(traceback.format_exc())
            pass
        finally:
            mc.undoInfo(closeChunk=True)
            return action

    return wrapper

""" Smart Save """
DEFAULT_PADDING = 3

def paddingExistsInBasename(baseName):
    result = re.search(r"_v\d*.", baseName)
    if result == None:
        return False
    return True

def paddingExistsInFiles(matchList):
    matchListString = " ".join(matchList)

    result = re.search(r"_v\d*.", matchListString)
    if result == None:
        return False
    return True

def getPadding( matchList):
    pattern = re.compile(r"_v\d*.")
    for match in matchList:
        version = pattern.findall(match)
        versionStripped = version[0][2:-1]
        padding = len(versionStripped)
    return padding

def newSceneVersion(currentScenePath):
    currentSceneDir, currentSceneFile = os.path.split(currentScenePath)
    currentSceneBasename, currentSceneExt = os.path.splitext(currentSceneFile)

    fileList = os.listdir(currentSceneDir)
    fileListString = " ".join(fileList)

    # If current scene name has no "_v#"
    # e.g. currentSceneFile >> "blasterWalk.ma"
    # e.g. currentSceneBasename >> "blasterWalk"
    if not paddingExistsInBasename(currentSceneBasename):

        # We have to check the extention because files might have same basename but different extention(e.g. ".ma", ".mb")
        pattern = re.compile(r"{baseName}_v\d*{ext}".format(baseName=currentSceneBasename, ext=currentSceneExt))
        matchList = pattern.findall(fileListString)

        padding = getPadding(matchList) if paddingExistsInFiles(matchList) else DEFAULT_PADDING

        # Get list of all "blasterWalk_v#.ma" in same directory.
        # The current scene does not have "_v#",
        # but there might be a file in the same directory that already follows the naming convention "blasterWalk_v###.ma"
        versionList = []
        for match in matchList:
            try:
                versionPattern = re.compile(r"_v\d{{{padding}}}.".format(padding=padding))
                version = int(versionPattern.findall(match)[0][2:padding+2])
                versionList.append(version)
            except:
                pass

        # If there is no file that follows the naming convention "blasterWalk_v#.ma", save v001.
        # e.g. blasterWalk_v001.ma
        if len(versionList) == 0:
            newSceneVersionFile = "{baseName}_v{nextVer:0{padding}d}{ext}".format(baseName=currentSceneBasename, nextVer=1, padding=padding, ext=currentSceneExt)
            newSceneVersionPath = os.path.join(currentSceneDir, newSceneVersionFile)
            return newSceneVersionPath

        # If there is a file that follows the naming convention "blasterWalk_v#.ma", find the next available version and save.
        # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v002.ma] >> Result: blasterWalk_v003.ma
        # e.g. Files with same naming convention in directory: [blasterWalk_v0001.ma, blasterWalk_v0002.ma] >> Result: blasterWalk_v0003.ma
        # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v003.ma] >> Result: blasterWalk_v004.ma | Skips "blasterWalk_v002.ma"
        # e.g. Files with same naming convention in directory: [blasterWalk_v0001.ma, blasterWalk_v0003.ma] >> Result: blasterWalk_v0004.ma | Skips "blasterWalk_v002.ma"
        maxVersion = max(versionList)
        nextVersion = maxVersion + 1

        newSceneVersionFile = "{baseName}_v{nextVer:0{padding}d}{ext}".format(baseName=currentSceneBasename, nextVer=nextVersion, padding=padding, ext=currentSceneExt)
        newSceneVersionPath = os.path.join(currentSceneDir, newSceneVersionFile)
        return newSceneVersionPath

    # If current scene name has "_v#"
    # e.g. currentSceneFile >> "blasterWalk_v001.ma"
    # e.g. currentSceneBasename >> "blasterWalk_v001"
    # Get list of all "blasterWalk_v#.ma" in same directory.

    # Remove "_v#" from basename
    currentSceneBasenameVersionStripped = re.sub(r"_v\d*", "", currentSceneBasename)

    # We have to check the extention because files might have same basename but different extention(e.g. ".ma", ".mb")
    pattern = re.compile(r"{baseName}_v\d*{ext}".format(baseName=currentSceneBasenameVersionStripped, ext=currentSceneExt))
    matchList = pattern.findall(fileListString)

    padding = getPadding(matchList)

    versionList = []
    for match in matchList:
        try:
            versionPattern = re.compile(r"_v\d{{{padding}}}.".format(padding=padding))
            version = int(versionPattern.findall(match)[0][2:padding+2])
            versionList.append(version)
        except:
            pass

    # If there is a file that follows the naming convention "blasterWalk_v###.ma", find the next available version and save.
    # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v002.ma] >> Result: blasterWalk_v003.ma
    # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v003.ma] >> Result: blasterWalk_v004.ma | Skips "blasterWalk_v002.ma"
    maxVersion = max(versionList)
    nextVersion = maxVersion + 1

    newSceneVersionFile = "{baseName}_v{nextVer:0{padding}d}{ext}".format(baseName=currentSceneBasenameVersionStripped, nextVer=nextVersion, padding=padding, ext=currentSceneExt)
    newSceneVersionPath = os.path.join(currentSceneDir, newSceneVersionFile)
    return newSceneVersionPath

def smartSave():
    currentScenePath = mc.file(q=1, sn=1)
    if currentScenePath == "":
        mc.warning("You must save a scene first.")
        return "Failed"

    currentSceneDir, currentSceneFile = os.path.split(currentScenePath)
    currentSceneBasename, currentSceneExt = os.path.splitext(currentSceneFile)

    newSceneVersionPath = newSceneVersion(currentScenePath)

    if currentSceneExt == ".ma": fileType = "mayaAscii"
    if currentSceneExt == ".mb": fileType = "mayaBinary"

    # Rename and Save
    mc.file(rename=newSceneVersionPath)
    mc.file(save=True, type=fileType)

""" Smart Save """


class BakeCam(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(BakeCam, self).__init__(self.maya_main_window())

        self.setWindowTitle("Bake Cam")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.loadSettings()

    def create_widgets(self):
        self.options_resetScale_cb = QtWidgets.QCheckBox("Reset Scale")
        self.options_resetScale_cb.setChecked(True)
        self.options_smartSave_cb = QtWidgets.QCheckBox("Smart Save")
        self.options_smartSave_cb.setChecked(True)

        self.bake_duplicate_btn = QtWidgets.QPushButton("\nDuplicate\n")
        self.bake_reparentToWorld_btn = QtWidgets.QPushButton("Reparent\nto\nWorld")

    def create_layouts(self):
        options_groupbox = QtWidgets.QGroupBox("Options")
        options_layout = QtWidgets.QGridLayout()
        options_layout.addWidget(self.options_resetScale_cb, 0, 0)
        options_layout.addWidget(self.options_smartSave_cb, 0, 1)
        options_groupbox.setLayout(options_layout)

        bake_groupbox = QtWidgets.QGroupBox("Method")
        bake_layout = QtWidgets.QGridLayout()
        bake_layout.addWidget(self.bake_duplicate_btn, 0, 0)
        bake_layout.addWidget(self.bake_reparentToWorld_btn, 0, 1)
        bake_groupbox.setLayout(bake_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(options_groupbox)
        main_layout.addWidget(bake_groupbox)

    def create_connections(self):
        #self.bake_duplicate_btn.clicked.connect(lambda: self.bake("duplicate"))
        self.bake_reparentToWorld_btn.clicked.connect(lambda: self.bake("reparentToWorld"))

    def getObjectType(self, sel):
        selShape = mc.listRelatives(sel, fullPath=True, shapes=True) # Get selected object's shape node.
        objectType = mc.objectType(selShape) # Get object type.
        return objectType

    def saveSettings(self):
        mc.optionVar(intValue=("bakeCam_options_resetScale_cb", self.options_resetScale_cb.isChecked()))
        mc.optionVar(intValue=("bakeCam_options_smartSave_cb", self.options_smartSave_cb.isChecked()))

    def loadSettings(self):
        if mc.optionVar(exists="bakeCam_options_resetScale_cb"):
            self.options_resetScale_cb.setChecked(True) if mc.optionVar(q="bakeCam_options_resetScale_cb") else self.options_resetScale_cb.setChecked(False)
        if mc.optionVar(exists="bakeCam_options_smartSave_cb"):
            self.options_smartSave_cb.setChecked(True) if mc.optionVar(q="bakeCam_options_smartSave_cb") else self.options_smartSave_cb.setChecked(False)

    @openCloseChunk
    def bake(self, method):
        """
        Bake Method
        Duplicate:
        Reparent to World: If the camera you want to bake has custom attributes or connections you do not want to break, click this.
        """

        sel = mc.ls(selection=True, long=True)
        if len(sel) != 1: # Check if only one object is selected.
            mc.warning("You must select a single camera.")
            return

        if self.getObjectType(sel) != "camera": # Check if selected object's type is camera.
            mc.warning("You must select a single camera.")
            return

        if mc.listRelatives(sel, parent=True) == None: # Check if selected camera's parent is 'world'.
            mc.warning("Selected camera is already a child of the parent, 'world'.")
            return

        if self.options_smartSave_cb.isChecked():
            # e.g. current scene: blasterWalk_v001.ma
            # Save once...
            # e.g. blasterWalk_v002.ma
            if smartSave() == "Failed":
                return
            # Save twice...
            # e.g. blasterWalk_v003.ma << It is safe to overwrite this file because you have "blasterWalk_v002.ma"!
            smartSave()

        selCamTrans = sel[0]
        selCamShape = mc.listRelatives(selCamTrans, shapes=True, fullPath=True)[0]

        minTime = mc.playbackOptions(q=True, minTime=True)
        maxTime = mc.playbackOptions(q=True, maxTime=True)

        if method == "duplicate":
            dupCamTrans, dupCamShape = mc.camera(name=selCamTrans)
            print "WIP"

        if method == "reparentToWorld":
            worldLoc = mc.spaceLocator(name="worldLoc")[0]
            selCamRotateOrder = mc.getAttr(selCamTrans+".rotateOrder")
            mc.setAttr(worldLoc+".rotateOrder", selCamRotateOrder)

            pc = mc.parentConstraint(selCamTrans, worldLoc, maintainOffset=False)

            mc.ogs(pause=True)
            mc.bakeResults(worldLoc, simulation=True, attribute=["tx","ty","tz","rx","ry","rz"], time=(minTime, maxTime))
            mc.ogs(pause=True)

            mc.delete(pc) # Delete parent constraint.

            # Delete selected camera's translation and rotation attributes.
            mm.eval('cutKey -time ":" -hierarchy none  -at "tx" -at "ty" -at "tz" -at "rx" -at "ry" -at "rz" {cam};'.format(cam=selCamTrans))
            # Unparent selected camera to world
            unparentedSelCamTrans = mc.parent(selCamTrans, world=True)[0]

            # Cut worldLoc transform keys.
            mm.eval('cutKey -time ":" -hierarchy none  -at "tx" -at "ty" -at "tz" -at "rx" -at "ry" -at "rz" {loc};'.format(loc=worldLoc))
            # Paste worldLoc transform keys to unparentedSelCamTrans
            mm.eval('pasteKey -option replaceCompletely -copies 1 -connect 0 -timeOffset 0 -floatOffset 0 -valueOffset 0 "{cam}";'.format(cam=unparentedSelCamTrans))
            mc.delete(worldLoc)

            # If Reset Scale is checked, set unparentedSelCamTrans scaleXYZ value to 1.
            if self.options_resetScale_cb.isChecked():
                mc.setAttr(unparentedSelCamTrans+".sx", 1)
                mc.setAttr(unparentedSelCamTrans+".sy", 1)
                mc.setAttr(unparentedSelCamTrans+".sz", 1)

        # Close window
        self.close()
        self.deleteLater()

        # Save checkbox toggle state
        self.saveSettings()


if __name__ == "__main__":
    try:
        bc.close()
        bc.deleteLater()
    except:
        pass
    bc = BakeCam()
    bc.show()
