from maya import cmds

def main():
    toggleState = cmds.selectType(q=True, joint=True)
    cmds.selectType(joint=(not toggleState))
    
if __name__ == "__main__":
    main()
