# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91


import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui


def main(mode):
    selVisCamShapeList = mc.ls(cameras=True, visible=True, long=True)
    selVisCamShapeListSize = len(selVisCamShapeList)

    panelWithFocus = mc.getPanel(withFocus=True)

    activeView = omui.M3dView.active3dView()
    camDagPath = om.MDagPath()
    activeView.getCamera(camDagPath)
    currentCam = camDagPath.fullPathName()

    if selVisCamShapeListSize == 1:
        if currentCam == '|persp|perspShape':
            mc.lookThru(panelWithFocus, selVisCamShapeList[0])
        else:
            mc.lookThru(panelWithFocus, '|persp|perspShape')
    elif mode == "forward":
        if currentCam not in selVisCamShapeList:
            mc.lookThru(panelWithFocus, selVisCamShapeList[0])
        else:
            if selVisCamShapeList.index(currentCam) == selVisCamShapeListSize - 1:
                mc.lookThru(panelWithFocus, selVisCamShapeList[0])
            else:
                mc.lookThru(panelWithFocus, selVisCamShapeList[selVisCamShapeList.index(currentCam) + 1])
    elif mode == "backward":
        if currentCam not in selVisCamShapeList:
            mc.lookThru(panelWithFocus, selVisCamShapeList[0])
        else:
            if selVisCamShapeList.index(currentCam) == 0:
                mc.lookThru(panelWithFocus, selVisCamShapeList[selVisCamShapeListSize - 1])
            else:
                mc.lookThru(panelWithFocus, selVisCamShapeList[selVisCamShapeList.index(currentCam) - 1])


if __name__ == "__main__":
    main("backward")
