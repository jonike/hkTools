import maya.cmds as mc
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
    if mc.objExists("*horizonLine*"):
        mc.delete("*horizonLine*") # Delete existing "horizonLine"
        return

    active3dViewCamShape, active3dViewCamTrans = getActive3dViewCam()

    horizonLineTrans = mc.circle(name='horizonLine', radius=2, normal=(0,1,0), sections=32)[0]
    horizonLineShape = mc.listRelatives(horizonLineTrans, shapes=True, fullPath=True)[0]

    mc.expression(s="""
                    {0}.sx = {1}.nearClipPlane;
                    {0}.sy = {1}.nearClipPlane;
                    {0}.sz = {1}.nearClipPlane;
                    """.format(horizonLineTrans, active3dViewCamShape), object=horizonLineTrans)

    mc.setAttr(horizonLineShape + '.overrideEnabled', 1)
    mc.setAttr(horizonLineShape + '.overrideColor', 14)

    mc.pointConstraint(active3dViewCamTrans, horizonLineTrans, maintainOffset=False)


if __name__ == "__main__":
    main()
