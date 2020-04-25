from maya import cmds

def main():
    sels = cmds.ls(selection=True, long=True)

    if len(sels) == 0:
        return

    for sel in sels:
        toggleState = cmds.getAttr(sel+".displayRotatePivot")
        cmds.setAttr(sel+".displayRotatePivot", (not toggleState))


if __name__ == "__main__":
    main()
