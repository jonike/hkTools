import maya.cmds as mc
import maya.mel as mm

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


class BakeCam(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


    def __init__(self):
        super(BakeCam, self).__init__(self.maya_main_window())

        self.setWindowTitle("Bake Cam")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.camShapeAttr = ['.hfa','.vfa','.fl','.nearClipPlane','.farClipPlane','.horizontalFilmOffset','.verticalFilmOffset']

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.bake_keepOriginal_btn = QtWidgets.QPushButton("Keep\nOriginal")
        self.bake_reparentToWorld_btn = QtWidgets.QPushButton("Reparent\nto\nWorld")

    def create_layouts(self):
        bake_groupbox = QtWidgets.QGroupBox()
        bake_layout = QtWidgets.QGridLayout()
        bake_layout.addWidget(self.bake_keepOriginal_btn, 0, 0)
        bake_layout.addWidget(self.bake_reparentToWorld_btn, 0, 1)
        bake_groupbox.setLayout(bake_layout)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(bake_groupbox)

    def create_connections(self):
        self.bake_keepOriginal_btn.clicked.connect(lambda: self.bake("keepOriginal"))
        self.bake_reparentToWorld_btn.clicked.connect(lambda: self.bake("reparentToWorld"))

    def getObjectType(self, sel):
        selShape = mc.listRelatives(sel, fullPath=True, shapes=True) # Get selected object's shape node.
        objectType = mc.objectType(selShape) # Get object type.
        return objectType

    @openCloseChunk
    def bake(self, mode):
        """
        Bake Options
        Keep Original
        Reparent to World: If the camera you want to bake has custom attributes or connections you do not want to break, click this.
        """

        sel = mc.ls(selection=True, long=True)
        if len(sel) != 1:
            mc.warning("You must select a single camera.")
            return

        if self.getObjectType(sel) != "camera":
            mc.warning("You must select a single camera.")
            return

        selCamTrans = sel[0]
        selCamShape = mc.listRelatives(selCamTrans, shapes=True, fullPath=True)[0]

        minTime = mc.playbackOptions(q=True, minTime=True)
        maxTime = mc.playbackOptions(q=True, maxTime=True)

        if mode == "keepOriginal":
            print "keepOriginal"

        if mode == "reparentToWorld":
            worldLoc = mc.spaceLocator(name="worldLoc")[0]
            selCamRotateOrder = mc.getAttr(selCamTrans+".rotateOrder")
            mc.setAttr(worldLoc+".rotateOrder", selCamRotateOrder)

            pc = mc.parentConstraint(selCamTrans, worldLoc, maintainOffset=False)

            mc.ogs(pause=True)
            mc.bakeResults(worldLoc, simulation=True, attribute=["tx","ty","tz","rx","ry","rz"], time=(minTime, maxTime))
            mc.ogs(pause=True)

            mc.delete(pc)

            # Delete selected camera's translation and rotation attributes.
            mm.eval('cutKey -time ":" -hierarchy none  -at "tx" -at "ty" -at "tz" -at "rx" -at "ry" -at "rz" {cam};'.format(cam=selCamTrans))
            # Unparent selected camera to world
            unparentedSelCamTrans = mc.parent(selCamTrans, world=True)[0]

            # Cut worldLoc transform keys.
            mm.eval('cutKey -time ":" -hierarchy none  -at "tx" -at "ty" -at "tz" -at "rx" -at "ry" -at "rz" {loc};'.format(loc=worldLoc))
            # Paste worldLoc transform keys to unparentedSelCamTrans
            mm.eval('pasteKey -option replaceCompletely -copies 1 -connect 0 -timeOffset 0 -floatOffset 0 -valueOffset 0 "{cam}";'.format(cam=unparentedSelCamTrans))

            mc.delete(worldLoc)

            self.close()
            self.deleteLater()



if __name__ == "__main__":
    try:
        bc.close()
        bc.deleteLater()
    except:
        pass
    bc = BakeCam()
    bc.show()
