# Maya Matchmove Tools

## Tool List
### Matchmove
1. Center3D
    > ![doc/center3d_compare_120f.gif](doc/center3d_compare_120f.gif)<br>
    - [scripts/center3d.py](scripts/center3d.py)
    - [https://github.com/kohyuk91/center3d](https://github.com/kohyuk91/center3d)
1. Cycle Through Visible Cameras Forward & Backward
    - If there is **only one** visible camera in the scene, jump between **persp camera** and the **one visible camera**.
        > ![doc/cycleThroughVisibleCameras_onlyOneVisibleCamera.gif](doc/cycleThroughVisibleCameras_onlyOneVisibleCamera.gif)<br>
    - If there are **more than two** visible cameras in the scene, cycle through all **visible cameras**.
      > ![doc/cycleThroughVisibleCameras_twoOrMoreVisibleCameras.gif](doc/cycleThroughVisibleCameras_twoOrMoreVisibleCameras.gif)<br>
    - [scripts/cycleThroughVisibleCamerasForward.py](scripts/cycleThroughVisibleCamerasForward.py)
    - [scripts/cycleThroughVisibleCamerasBackward.py](scripts/cycleThroughVisibleCamerasBackward.py)
1. Dual Image Plane
    - [scripts/dualImagePlane.py](scripts/dualImagePlane.py)
1. Horizon Line
    - [scripts/horizonLine.py](scripts/horizonLine.py)
1. Reset Pan Zoom
    - [scripts/resetPanZoom.py](scripts/resetPanZoom.py)
1. TLOC
    - [scripts/tloc.py](scripts/tloc.py)
    - [https://github.com/kohyuk91/tloc](https://github.com/kohyuk91/tloc)
1. ZLOC
    - [scripts/zloc_maya.py](scripts/zloc_maya.py)
    - [https://github.com/kohyuk91/zloc](https://github.com/kohyuk91/zloc)

### Miscellaneous
1. Toggle Show
1. Toggle Docked Window
    > ![doc/toggleDockedWindow.gif](doc/toggleDockedWindow.gif)<br>
    - [scripts/toggleDockedGraphEditor.py](scripts/toggleDockedGraphEditor.py)
1. Toggle Pickmask
    > ![doc/togglePickmask.gif](doc/togglePickmask.gif)<br>
    - [scripts/togglePickmaskHandle.py](scripts/togglePickmaskHandle.py)
    - [scripts/togglePickmaskJoint.py](scripts/togglePickmaskJoint.py)
    - [scripts/togglePickmaskCurve.py](scripts/togglePickmaskCurve.py)
    - [scripts/toggleShowPolymeshes.py](scripts/toggleShowPolymeshes.py)
1. Toggle Pivot
    - [scripts/toggleDisplayRotatePivot.py](scripts/toggleDisplayRotatePivot.py)

## Installation
1. Download and unzip the mayaMatchmoveTools.zip file from [GitHub releases](https://github.com/kohyuk91/mayaMatchmoveTools/releases).

1. Drag and drop the `drag_and_drop_install.mel` file onto the Maya viewport.

1. Open `Hotkey Editor`
    1. Edit Hotkeys For: `Custom Scripts`
    1. Assign a Hotkey for each command
