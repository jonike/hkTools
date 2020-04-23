# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91


import maya.cmds as mc


def getObjectType(sel):
    try:
        objectType = mc.objectType(sel) # Get object type.
    except:
        objectType = "transform" # If there is no shape node pass "transform".
    return objectType


def isOneImageplaneSelected(shapeList):
    shapeListSize = len(shapeList)
    if not 0 < shapeListSize < 2:
        return False

    objectType = getObjectType(shapeList[0])
    if objectType == "imagePlane":
        return True
    else:
        return False


def getShapeList(transformList):
    shapeList = []
    for transform in transformList:
        shape = mc.listRelatives(transform, shapes=True, fullPath=True)[0]
        shapeList.append(shape)
    return shapeList


def main():
    selGeoTransList = mc.ls(selection=True, long=True)
    selGeoShapeList = getShapeList(selGeoTransList)
    selGeoShapeListSize = len(selGeoShapeList)

    if selGeoShapeListSize == 0 or isOneImageplaneSelected(selGeoShapeList): # If nothing is selected toggle all geometry in scene.
        holdoutGeoExists = False
        geoList = mc.ls(geometry=True, long=True) # Get list of geometric Dag objects in scene.
        for geo in geoList:
            try:
                holdoutGeoExists = mc.getAttr(geo + '.holdOut')
            except:
                pass

        if holdoutGeoExists: # If Holdout Geometry exists in scene...
            for geo in geoList:
                try:
                    mc.setAttr(geo + '.holdOut', 0) # Turn off holdout for all geometry in scene
                except:
                    pass
            return

        if not holdoutGeoExists: # If there is no Holdout Geometry in scene...
            for geo in geoList:
                try:
                    mc.setAttr(geo + '.holdOut', 1) # Turn on holdout for all geometry in scene
                except:
                    pass
            return

    elif selGeoShapeListSize >= 0:
        for selGeoShape in selGeoShapeList:
            try:
                toggleState = mc.getAttr(selGeoShape + '.holdOut')
                mc.setAttr(selGeoShape + '.holdOut', (not toggleState))
            except:
                pass


if __name__ == "__main__":
    main()
