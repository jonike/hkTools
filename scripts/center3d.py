# BSD 3-Clause License
#
# Copyright (c) 2020, Hyuk Ko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#
# Shout out to Frank Illing for the "World Space to Image Space" formula.
#

# Documentation
"""
https://github.com/kohyuk91/center3d
"""

# Usage
# Execute the code below via Hotkey.
# e.g) Alt + Shift + C
"""
import center3d
center3d.main()
"""

# Versions
# 0.1.1 - Added 'if __name__ == "__main__":' statement.
# 0.1.0 - Initial Release (2020.04.11)
# 0.0.1 - Project start (2018)


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

def getObjectType(sel):
    try:
        selShape = mc.listRelatives(sel, fullPath=True, shapes=True) # Get selected object's shape node.
        objectType = mc.objectType(selShape) # Get object type.
    except:
        objectType = "transform" # If there is no shape node pass "transform".
    return objectType


def center3d():
    """
    Centers the viewport to TLOC.
    This may not work properly if the Image Plane's Aspect Ratio and Device Aspect Ratio(in Render Setting) does not match.
    Image Plane Size: 1920 X 1080 (1.778)  and  Image Size: 1920 X 1080 (1.778) --> O
    Image Plane Size: 1920 X 1080 (1.778)  and  Image Size: 960 X 540 (1.778) --> O
    Image Plane Size: 1920 X 1080 (1.778) and  Image Size: 3000 X 1500 (1.5) --> X
    """
    # Get selected transform list
    selTransformList = mc.ls(selection=True, long=True)
    if len(selTransformList) == 0:
        mc.warning("Select one or more Transform Nodes")
        return

    # Check if imagePlane is in selection list
    for selTransform in selTransformList:
        objectType = getObjectType(selTransform)
        if objectType == "imagePlane":
            mc.warning("Can't Center3D an image plane")
            return

    # Get Active 3D View Camera
    active3dViewCamShape, active3dViewCamTrans = getActive3dViewCam()

    active3dViewCamTrans = mc.listRelatives(active3dViewCamShape, parent=True, fullPath=True)[0]
    try:
        active3dViewCamImgPlaneShape = mc.listRelatives(active3dViewCamShape, allDescendents=True, type='imagePlane')[0]
    except:
        active3dViewCamImgPlaneShape = None

    # Set Imageplane to show in "All Views"
    if active3dViewCamImgPlaneShape is not None:
        mc.imagePlane(active3dViewCamImgPlaneShape, e=True, showInAllViews=True)

    # Create Center3D Locator
    center3dLoc = mc.spaceLocator(name='center3d_#')[0]
    mc.setAttr(center3dLoc+'.v', 0)

    for selTransform in selTransformList:
        mc.pointConstraint(selTransform, center3dLoc, maintainOffset=False)


    # Create Center3D Camera
    center3dCam = mc.camera(name=active3dViewCamTrans + center3dLoc)[0]
    center3DcamTrans = mc.ls(mc.parent(center3dCam, active3dViewCamTrans, relative=True), long=True)[0]
    center3DcamShape = mc.listRelatives(center3DcamTrans, shapes=True, fullPath=True)[0]


    # LookThru Center3D Camera
    panelWithFocus = mc.getPanel(withFocus=True)
    mc.lookThru(panelWithFocus, center3DcamShape)


    # Sync Shape Attributes. Active 3D View Cam & Center 3D Cam
    mc.connectAttr(active3dViewCamShape+'.hfa' , center3DcamShape+'.hfa')
    mc.connectAttr(active3dViewCamShape+'.vfa' , center3DcamShape+'.vfa')
    mc.connectAttr(active3dViewCamShape+'.fl' , center3DcamShape+'.fl')
    mc.connectAttr(active3dViewCamShape+'.nearClipPlane' , center3DcamShape+'.nearClipPlane')
    mc.connectAttr(active3dViewCamShape+'.farClipPlane' , center3DcamShape+'.farClipPlane')


    # Center3D Expression
    exp =  'global proc float[] cTtransformPoint(float $mtx[], float $pt[]) // multiply 4x4 matrix with 4x vector\n'
    exp += '{\n'
    exp += '    float $res[] = {};\n'
    exp += '    if(`size $pt` == 3)\n'
    exp += '    $pt[3] = 1.0;\n'
    exp += '    for($i=0;$i<4;$i++){\n'
    exp += '    float $tmp = 0;\n'
    exp += '    for($k=0;$k<4;$k++){\n'
    exp += '        $tmp += $pt[$k] * $mtx[$k * 4 + $i];\n'
    exp += '    };\n'
    exp += '    $res[$i] = $tmp;\n'
    exp += '    };\n'
    exp += '    return $res;\n'
    exp += '};\n'

    exp += 'global proc float[] cGetProjectionMatrix(string $shape) //get camera projection matrix\n'
    exp += '{\n'
    exp += '    float $res[] = {};\n'
    exp += '    if(`objExists $shape` && `nodeType $shape` == "camera"){\n'
    exp += '    python "import maya.OpenMaya as om";\n'
    exp += '    python "list = om.MSelectionList()";\n'
    exp += '    python (' + '"' + 'list.add(' + "'"+ '"' + '+ $shape + ' + '"' + "')" + '");\n'
    exp += '    python "depNode = om.MObject()";\n'
    exp += '    python "list.getDependNode(0, depNode)";\n'
    exp += '    python "camFn = om.MFnCamera(depNode)";\n'
    exp += '    python "pMtx = om.MFloatMatrix()";\n'
    exp += '    python "pMtx = camFn.projectionMatrix()";\n'
    exp += '    for($i=0;$i<=3;$i++){\n'
    exp += '        for($k=0;$k<=3;$k++)\n'
    exp += '        $res[`size $res`] = `python ("pMtx(" + $i + ", " + $k + ")")`;\n'
    exp += '    };\n'
    exp += '    };\n'
    exp += '    return $res;\n'
    exp += '};\n'

    exp += 'global proc float[] cWorldSpaceToImageSpace(string $camera, float $worldPt[])\n'
    exp += '{\n'
    exp += '    string $camShape[] = `ls -dag -type "camera" $camera`;\n'
    exp += '    if(! `size $camShape`)\n'
    exp += '    return {};\n'
    exp += '    string $cam[] = `listRelatives -p -f $camShape`;\n'
    exp += '    float $cam_inverseMatrix[] = `getAttr ($cam[0] + ".worldInverseMatrix")`;\n'
    exp += '    float $cam_projectionMatrix[] = `cGetProjectionMatrix $camShape[0]`;\n'
    exp += '    float $ptInCamSpace[] = `cTtransformPoint $cam_inverseMatrix $worldPt`;\n'
    exp += '    float $projectedPoint[] = `cTtransformPoint $cam_projectionMatrix $ptInCamSpace`;\n'
    exp += '    float $resultX = (($projectedPoint[0] / $projectedPoint[3]));\n'
    exp += '    float $resultY = (($projectedPoint[1] / $projectedPoint[3]));\n'
    exp += '    return {$resultX, $resultY};\n'
    exp += '};\n'

    exp += 'float $xy[] = cWorldSpaceToImageSpace("' + active3dViewCamTrans +'", {'+ center3dLoc +'.translateX,'+center3dLoc+'.translateY,'+center3dLoc+'.translateZ});\n'
    exp += center3DcamShape + '.horizontalFilmOffset = ($xy[0] *' + active3dViewCamShape + '.hfa)/2 ;\n'
    exp += center3DcamShape + '.verticalFilmOffset = ($xy[1] *'+ active3dViewCamShape + '.vfa)/2 ;\n'

    mc.expression(s=exp ,object=center3DcamShape)

    # Select Center3D Loc ##
    mc.select(center3dLoc, replace=True)


def main():

    if mc.objExists("*center3d*") == True:
        mc.delete("*center3d*") # Delete all Center3D nodes
        return

    center3d()


if __name__ == "__main__":
    main()
