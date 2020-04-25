from maya import cmds

def main():
    panel = cmds.getPanel( withFocus = True )
    if cmds.getPanel( typeOf = panel ) == 'modelPanel':

        toggleState = cmds.modelEditor( panel, query = True, imagePlane = True )
        cmds.modelEditor( panel, edit = True, imagePlane = ( not toggleState ) )

if __name__ == "__main__":
    main()
