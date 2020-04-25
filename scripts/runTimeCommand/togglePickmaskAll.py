import maya.cmds as mc
import maya.mel as mm

def main():
    toggleState = mc.iconTextCheckBox("objSelHandleBtn", q=True, v=True) or mc.iconTextCheckBox("objSelJointBtn", q=True, v=True) or mc.iconTextCheckBox("objSelCurveBtn", q=True, v=True) or mc.iconTextCheckBox("objSelSurfaceBtn", q=True, v=True) or mc.iconTextCheckBox("objSelDeformBtn", q=True, v=True) or mc.iconTextCheckBox("objSelDynamicBtn", q=True, v=True) or mc.iconTextCheckBox("objSelRenderBtn", q=True, v=True) or mc.iconTextCheckBox("objSelMiscBtn", q=True, v=True)
    mm.eval('setObjectPickMask "All" false;') if toggleState else mm.eval('setObjectPickMask "All" true;')

if __name__ == "__main__":
    main()
