import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelSurfaceBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Surface" false;') if toggleState else mm.eval('setObjectPickMask "Surface" true;')

if __name__ == "__main__":
    main()
