import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelDynamicBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Dynamic" false;') if toggleState else mm.eval('setObjectPickMask "Dynamic" true;')

if __name__ == "__main__":
    main()
