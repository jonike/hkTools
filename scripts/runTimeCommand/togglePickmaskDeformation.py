import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelDeformBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Deformer" false;') if toggleState else mm.eval('setObjectPickMask "Deformer" true;')

if __name__ == "__main__":
    main()
