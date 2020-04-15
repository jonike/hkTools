import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

def main():
    active3dView = omui.M3dView.active3dView()
    active3dViewCamDagPath = om.MDagPath()
    active3dView.getCamera(active3dViewCamDagPath)
    active3dViewCamShape = active3dViewCamDagPath.fullPathName()

    try:
        mc.setAttr(active3dViewCamShape+'.horizontalPan', lock=False)
        mc.setAttr(active3dViewCamShape+'.horizontalPan', 0)
        mc.setAttr(active3dViewCamShape+'.verticalPan', lock=False)
        mc.setAttr(active3dViewCamShape+'.verticalPan', 0)
        mc.setAttr(active3dViewCamShape+'.zoom', lock=False)
        mc.setAttr(active3dViewCamShape+'.zoom', 1)
        mc.setAttr(active3dViewCamShape+'.renderPanZoom', lock=False)
        mc.setAttr(active3dViewCamShape+'.renderPanZoom', 0)
        mc.setAttr(active3dViewCamShape+'.panZoomEnabled', lock=False)
        mc.setAttr(active3dViewCamShape+'.panZoomEnabled', 0)
    except:
        mc.warning("Something went wrong.")

if __name__ == "__main__":
    main()
