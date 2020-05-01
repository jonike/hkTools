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

        self.bake_reparentToWorld_btn = QtWidgets.QPushButton("BAKE CAMERA")
        self.bake_reparentToWorld_btn.setStyleSheet("QPushButton {background-color: #EC5f67;}")

    def create_layouts(self):
        options_groupbox = QtWidgets.QGroupBox("Options")
        options_layout = QtWidgets.QGridLayout()
        options_layout.addWidget(self.options_resetScale_cb, 0, 0)
        options_groupbox.setLayout(options_layout)

        bake_groupbox = QtWidgets.QGroupBox()
        bake_layout = QtWidgets.QGridLayout()
        bake_layout.addWidget(self.bake_reparentToWorld_btn, 0, 0)
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

    def loadSettings(self):
        if mc.optionVar(exists="bakeCam_options_resetScale_cb"):
            self.options_resetScale_cb.setChecked(True) if mc.optionVar(q="bakeCam_options_resetScale_cb") else self.options_resetScale_cb.setChecked(False)

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


        selCamTrans = sel[0]
        selCamShape = mc.listRelatives(selCamTrans, shapes=True, fullPath=True)[0]

        minTime = mc.playbackOptions(q=True, minTime=True)
        maxTime = mc.playbackOptions(q=True, maxTime=True)

        #if method == "duplicate":
        #    dupCamTrans, dupCamShape = mc.camera(name=selCamTrans)
        #    print "WIP"

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
