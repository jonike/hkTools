from maya import cmds

def main():
    toggleState = cmds.selectType(q=True, handle=True) or cmds.selectType(q=True, ikHandle=True)
    cmds.selectType(handle=(not toggleState))
    cmds.selectType(ikHandle=(not toggleState))

if __name__ == "__main__":
    main()
