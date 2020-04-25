import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelHandleBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Marker" false;') if toggleState else mm.eval('setObjectPickMask "Marker" true;')

if __name__ == "__main__":
    main()
