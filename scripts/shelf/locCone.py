# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91


import maya.cmds as mc


def createCone(locName):
    cone = mc.polyCone(name=locName+'_cone', r=1, h=2, sx=4, sy=1, sz=0, ax=[0,-1,0], rcp=0, cuv=3, ch=True)[0]
    mc.move(1, y=True)
    mc.rotate(45, y=True)
    mc.move(0, 0, 0, cone+".scalePivot", cone+".rotatePivot", absolute=True)
    mc.makeIdentity(apply=True, translate=True, rotate=True)
    return cone

def main():
    selList = []
    selList = mc.ls(selection=True)

    for sel in selList:
        cone = createCone(sel)
        mc.select(cone, sel, replace=True)
        mc.MatchTranslation()
        mc.select(clear=True)


if __name__ == "__main__":
    main()
