from maya import cmds

def main():
    toggleState = cmds.selectType(q=True, polymesh=True)
    cmds.selectType(nurbsSurface=(not toggleState))
    cmds.selectType(polymesh=(not toggleState))
    cmds.selectType(plane=(not toggleState))
    cmds.selectType(byName=("gpuCache", (not toggleState)))

if __name__ == "__main__":
    main()
