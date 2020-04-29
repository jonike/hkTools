# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91

"""
import childSpace
try:
    cs.close()
    cs.deleteLater()
except:
    pass
cs = childSpace.ChildSpace()
cs.show()
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


class ChildSpace(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(ChildSpace, self).__init__(self.maya_main_window())

        self.setWindowTitle("Child Space")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_icons()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_icons(self):
        self.add_icon = QtGui.QIcon(":addCreateGeneric.png")
        self.delete_icon = QtGui.QIcon(":deleteGeneric.png")

    def create_widgets(self):
        self.camera_lb = QtWidgets.QLabel()
        self.camera_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_lb.setStyleSheet("QLabel {background-color: #252525;}")
        self.camera_get_btn = QtWidgets.QPushButton("GET")

        self.objectPointGroupList_lw = QtWidgets.QListWidget()
        self.objectPointGroupList_add_btn = QtWidgets.QPushButton()
        self.objectPointGroupList_add_btn.setStyleSheet("QPushButton {background-color: #99C794;}")
        self.objectPointGroupList_add_btn.setIcon(self.add_icon)
        self.objectPointGroupList_remove_btn = QtWidgets.QPushButton()
        self.objectPointGroupList_remove_btn.setStyleSheet("QPushButton {background-color: #EC5f67;}")
        self.objectPointGroupList_remove_btn.setIcon(self.delete_icon)

        self.childSpace_btn = QtWidgets.QPushButton("RUN")

    def create_layouts(self):
        camera_groupbox = QtWidgets.QGroupBox("1. Get Camera")
        camera_layout = QtWidgets.QGridLayout()
        camera_layout.addWidget(self.camera_lb, 0, 0, 1, 2)
        camera_layout.addWidget(self.camera_get_btn, 0, 2)
        camera_groupbox.setLayout(camera_layout)

        objectPointGroupList_groupbox = QtWidgets.QGroupBox("2. Get Object Point Group List")
        objectPointGroupList_layout = QtWidgets.QGridLayout()
        objectPointGroupList_layout.addWidget(self.objectPointGroupList_lw, 0, 0, 1, 2)
        objectPointGroupList_layout.addWidget(self.objectPointGroupList_add_btn, 1, 0)
        objectPointGroupList_layout.addWidget(self.objectPointGroupList_remove_btn, 1, 1)
        objectPointGroupList_groupbox.setLayout(objectPointGroupList_layout)

        childSpace_groupbox = QtWidgets.QGroupBox("3. Switch to Child space")
        childSpace_layout = QtWidgets.QGridLayout()
        childSpace_layout.addWidget(self.childSpace_btn, 0, 0)
        childSpace_groupbox.setLayout(childSpace_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(camera_groupbox)
        main_layout.addWidget(objectPointGroupList_groupbox)
        main_layout.addWidget(childSpace_groupbox)

    def create_connections(self):
        self.objectPointGroupList_add_btn.clicked.connect(lambda: self.addItem(self.objectPointGroupList_lw, self.getPointGroup()))
        self.objectPointGroupList_remove_btn.clicked.connect(lambda: self.removeCurrentItem(self.objectPointGroupList_lw))
        self.camera_get_btn.clicked.connect(self.setCameraLabel)
        self.childSpace_btn.clicked.connect(self.childSpace)

    def getPointGroup(self):
        sel = mc.ls(selection=True, long=True)

        if len(sel) != 1: # Check if only one object is selected.
            mc.warning("Add one item at a time.")
            return

        pointGroup = sel[0]
        return pointGroup

    def getItems(self, listWidget):
        items = [listWidget.item(index).text() for index in xrange(listWidget.count())]
        return items

    def checkDuplicate(self, listWidget, itemName):
        items = self.getItems(listWidget)

        if itemName in items:
            return True

        return False

    def addItem(self, listWidget, itemName):
        if self.checkDuplicate(listWidget, itemName):
            mc.warning("Already in list.")
            return
        item = itemName
        listWidget.addItem(item)

    def removeCurrentItem(self, listWidget):
        removeItemRow = listWidget.currentRow()
        listWidget.takeItem(removeItemRow)

    def getObjectType(self, sel):
        selShape = mc.listRelatives(sel, fullPath=True, shapes=True) # Get selected object's shape node.
        objectType = mc.objectType(selShape) # Get object type.
        return objectType

    def setCameraLabel(self):
        sel = mc.ls(selection=True, long=True)
        if len(sel) != 1: # Check if only one object is selected.
            mc.warning("You must select a single camera.")
            return

        if self.getObjectType(sel) != "camera": # Check if selected object's type is camera.
            mc.warning("You must select a single camera.")
            return

        camera = sel[0]
        self.camera_lb.setText(camera)

    @openCloseChunk
    def childSpace(self):
        camera = self.camera_lb.text()
        if camera == "":
            mc.warning("1. Get Camera")
            return

        objectPointGroupList = self.getItems(self.objectPointGroupList_lw)
        if objectPointGroupList == []:
            mc.warning("2. Get Object Point Group List")
            return

        for objectPointGroup in objectPointGroupList:
            parentGrpTrans = mc.group(name=objectPointGroup+"_ctrl", empty=True)
            childGrpTrans = mc.duplicate(objectPointGroup, name=objectPointGroup+"_dup")[0]
            mc.parent(childGrpTrans, parentGrpTrans)

            ### Add Constraints ###
            parentGrpPC = mc.parentConstraint(camera, parentGrpTrans, maintainOffset=False)
            childGrpPC = mc.parentConstraint(objectPointGroup, childGrpTrans, maintainOffset=False)

            ### Bake ###
            minTime = mc.playbackOptions(q=True, minTime=True)
            maxTime = mc.playbackOptions(q=True, maxTime=True)
            mc.bakeResults(childGrpTrans, attribute=["tx","ty","tz","rx","ry","rz"], time=(minTime, maxTime))
            mc.delete(childGrpPC)

            ### Hide Original ###
            mc.hide(objectPointGroup)

        # Close window
        self.close()
        self.deleteLater()


if __name__ == "__main__":
    try:
        cs.close()
        cs.deleteLater()
    except:
        pass
    cs = ChildSpace()
    cs.show()
