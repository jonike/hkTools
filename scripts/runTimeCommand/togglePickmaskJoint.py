import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelJointBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Joint" false;') if toggleState else mm.eval('setObjectPickMask "Joint" true;')

if __name__ == "__main__":
    main()
    
