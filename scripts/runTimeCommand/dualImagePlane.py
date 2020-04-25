# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91

import maya.cmds as mc
import maya.mel as mm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui


def getActive3dViewCam():
    active3dView = omui.M3dView.active3dView()
    active3dViewCamDagPath = om.MDagPath()
    active3dView.getCamera(active3dViewCamDagPath)
    active3dViewCamShape = active3dViewCamDagPath.fullPathName()
    active3dViewCamTrans = mc.listRelatives(active3dViewCamShape, parent=True, fullPath=True)[0]

    return active3dViewCamShape, active3dViewCamTrans


def main():
    if mc.objExists("*dualImagePlane*"):
        mc.delete("*dualImagePlane*") # Delete existing "dualImagePlane"
        return

    active3dViewCamShape, active3dViewCamTrans = getActive3dViewCam()

    try:
        active3dViewCamImagePlaneShape = mc.listRelatives(active3dViewCamShape, allDescendents=True, type='imagePlane', fullPath=True)[0]
        active3dViewCamImagePlaneShapeImageName = mc.getAttr(active3dViewCamImagePlaneShape+'.imageName')
    except:
        mc.warning("No image plane found in current view.")
        return

    dualImagePlaneTrans = mc.imagePlane(name="dualImagePlane", sia=False, fileName=active3dViewCamImagePlaneShapeImageName, camera=active3dViewCamTrans)[0]
    dualImagePlaneShape = mc.listRelatives(dualImagePlaneTrans, shapes=True, fullPath=True)[0]

    mc.setAttr(dualImagePlaneShape+'.useFrameExtension', 1)
    mc.setAttr(dualImagePlaneShape+'.frameCache', mc.getAttr(active3dViewCamImagePlaneShape+'.frameCache'))
    mc.setAttr(dualImagePlaneShape+'.alphaGain', 0.5)

    # Depth Expression
    mc.expression(s="{0}.depth = {1}.nearClipPlane + 1".format(dualImagePlaneShape, active3dViewCamShape), object=dualImagePlaneTrans)


    mm.eval("AttributeEditor;")

if __name__ == "__main__":
    main()
