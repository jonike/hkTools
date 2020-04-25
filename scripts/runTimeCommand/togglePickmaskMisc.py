import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelMiscBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Other" false;') if toggleState else mm.eval('setObjectPickMask "Other" true;')

if __name__ == "__main__":
    main()
