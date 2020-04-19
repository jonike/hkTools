from maya import cmds

def main():
    toggleState = cmds.selectType(q=True, nurbsSurface=True) or cmds.selectType(q=True, polymesh=True) or cmds.selectType(q=True, plane=True) or cmds.selectType(queryByName="gpuCache")
    cmds.selectType(nurbsSurface=(not toggleState))
    cmds.selectType(polymesh=(not toggleState))
    cmds.selectType(plane=(not toggleState))
    cmds.selectType(byName=("gpuCache", (not toggleState)))

if __name__ == "__main__":
    main()
