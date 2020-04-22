from maya import cmds

def main():
    window = "graphEditor1Window"

    try:
        if cmds.workspaceControl(window, q=True, floating=True):
            cmds.warning("There is no docked '{0}'.".format(window))
            return
    except:
        cmds.warning("'{0}' does not exist.".format(window))
        return

    # If collapsed, raise. If raised, collapse.
    cmds.workspaceControl(window, e=True, collapse=True) if cmds.workspaceControl(window, q=True, r=True) else cmds.workspaceControl(window, e=True, restore=True)

if __name__ == "__main__":
    main()