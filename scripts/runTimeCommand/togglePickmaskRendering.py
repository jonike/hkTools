import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelRenderBtn", q=True, v=True)
    mm.eval('setObjectPickMask "Rendering" false;') if toggleState else mm.eval('setObjectPickMask "Rendering" true;')

if __name__ == "__main__":
    main()
