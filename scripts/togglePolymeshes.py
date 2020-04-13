from maya import cmds

def main():
    panel = cmds.getPanel( withFocus = True )
    if cmds.getPanel( typeOf = panel ) == 'modelPanel':
    
        toggleState = cmds.modelEditor( panel, query = True, polymeshes = True )
        cmds.modelEditor( panel, edit = True, polymeshes = ( not toggleState ) )

if __name__ == "__main__":
    main()
