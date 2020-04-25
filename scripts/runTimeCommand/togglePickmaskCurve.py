import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelCurveBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Curve" false;') if toggleState else mm.eval('setObjectPickMask "Curve" true;')

if __name__ == "__main__":
    main()
