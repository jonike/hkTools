import os
import imp


try:
    import maya.mel
    import maya.cmds
    isMaya = True
except ImportError:
    isMaya = False


def onMayaDroppedPythonFile(*args, **kwargs):
    pass


def _onMayaDropped():
    currentPath = os.path.dirname(__file__)
    hko_mm_hotkeys_Path = os.path.join(currentPath, "hko_mm_hotkeys.py")

    #imp.load_source("", hko_mm_hotkeys_Path)
    __import__("hko_mm_hotkeys")


if isMaya:
    _onMayaDropped()