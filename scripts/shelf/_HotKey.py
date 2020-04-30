import maya.cmds as mc

def main():
    # Returns all available hotkey sets in Maya
    hotkeySetList = cmds.hotkeySet( q=True, hotkeySetArray=True )
    hotkeySetListSize = len(hotkeySetList)

    if hotkeySetListSize == 1:
        return

    currentHotkeySet = cmds.hotkeySet( q=True, current=True )
    if hotkeySetList.index(currentHotkeySet) == hotkeySetListSize - 1:
        hotkeySet = cmds.hotkeySet( hotkeySetList[0], e=True, current=True )
        mc.warning("Switched to '{}' hotkey set.".format(hotkeySetList[0]))
    else:
        cmds.hotkeySet( hotkeySetList[hotkeySetList.index(currentHotkeySet) + 1], e=True, current=True )
        mc.warning("Switched to '{}' hotkey set.".format(hotkeySetList[hotkeySetList.index(currentHotkeySet) + 1]))

if __name__ == "__main__":
    main()
