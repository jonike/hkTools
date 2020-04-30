import maya.cmds as mc

def movePivotToYmin(sel):
    bbox = mc.exactWorldBoundingBox(sel)

    xpiv = (bbox[0] + bbox[3]) / 2
    zpiv = (bbox[2] + bbox[5]) / 2

    ypiv = bbox[1]

    mc.move(xpiv, ypiv, zpiv, sel+".scalePivot", sel+".rotatePivot", worldSpace=True)

def main():
    selList = mc.ls(selection=True)
    for sel in selList:
        movePivotToYmin(sel)


if __name__ == "__main__":
    main()
