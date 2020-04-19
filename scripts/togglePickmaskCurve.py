from maya import cmds

def main():
    toggleState = cmds.selectType(q=True, nurbsCurve=True) or cmds.selectType(q=True, cos=True) or cmds.selectType(q=True, stroke=True)
    cmds.selectType(nurbsCurve=(not toggleState))
    cmds.selectType(cos=(not toggleState))
    cmds.selectType(stroke=(not toggleState))

if __name__ == "__main__":
    main()
