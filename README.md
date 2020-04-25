# Maya Matchmove Tools

## Tool List
### Matchmove
1. Center3D
    > ![doc/center3d_compare_120f.gif](doc/center3d_compare_120f.gif)<br>
    - [scripts/runTimeCommand/center3d.py](scripts/runTimeCommand/center3d.py)
    - [https://github.com/kohyuk91/center3d](https://github.com/kohyuk91/center3d)
1. Cycle Through Visible Cameras Forward & Backward
    - If there is **only one** visible camera in the scene, jump between **persp camera** and the **one visible camera**.
        > ![doc/cycleThroughVisibleCameras_onlyOneVisibleCamera.gif](doc/cycleThroughVisibleCameras_onlyOneVisibleCamera.gif)<br>
    - If there are **more than two** visible cameras in the scene, cycle through **all visible cameras**.
      > ![doc/cycleThroughVisibleCameras_twoOrMoreVisibleCameras.gif](doc/cycleThroughVisibleCameras_twoOrMoreVisibleCameras.gif)<br>
    - [scripts/runTimeCommand/cycleThroughVisibleCamerasForward.py](scripts/runTimeCommand/cycleThroughVisibleCamerasForward.py)
    - [scripts/runTimeCommand/cycleThroughVisibleCamerasBackward.py](scripts/runTimeCommand/cycleThroughVisibleCamerasBackward.py)
1. Dual Image Plane
    - [scripts/runTimeCommand/dualImagePlane.py](scripts/runTimeCommand/dualImagePlane.py)
1. Horizon Line
    - [scripts/runTimeCommand/horizonLine.py](scripts/runTimeCommand/horizonLine.py)
1. Reset Pan Zoom
    - [scripts/runTimeCommand/resetPanZoom.py](scripts/runTimeCommand/resetPanZoom.py)
1. TLOC
    - [scripts/runTimeCommand/tloc.py](scripts/runTimeCommand/tloc.py)
    - [https://github.com/kohyuk91/tloc](https://github.com/kohyuk91/tloc)
1. ZLOC
    - [scripts/shelf/zloc_maya.py](scripts/shelf/zloc_maya.py)
    - [https://github.com/kohyuk91/zloc](https://github.com/kohyuk91/zloc)

### Miscellaneous
1. Smart Save
    - Similar to "Save New Comp Version" in Foundry Nuke.
    - [scripts/runTimeCommand/smartSave.py](scripts/runTimeCommand/smartSave.py)
1. Toggle Holdout
    - [scripts/runTimeCommand/toggleHoldout.py](scripts/runTimeCommand/toggleHoldout.py)
1. Toggle Show
1. Toggle Docked Window
    > ![doc/toggleDockedWindow.gif](doc/toggleDockedWindow.gif)<br>
    - [scripts/runTimeCommand/toggleDockedGraphEditor.py](scripts/runTimeCommand/toggleDockedGraphEditor.py)
1. Toggle Pickmask
    > ![doc/togglePickmask.gif](doc/togglePickmask.gif)<br>
    - [scripts/runTimeCommand/togglePickmaskHandle.py](scripts/runTimeCommand/togglePickmaskHandle.py)
    - [scripts/runTimeCommand/togglePickmaskJoint.py](scripts/runTimeCommand/togglePickmaskJoint.py)
    - [scripts/runTimeCommand/togglePickmaskCurve.py](scripts/runTimeCommand/togglePickmaskCurve.py)
    - [scripts/runTimeCommand/togglePickmaskSurface.py](scripts/runTimeCommand/togglePickmaskSurface.py)
    - [scripts/runTimeCommand/togglePickmaskDeformation.py](scripts/runTimeCommand/togglePickmaskDeformation.py)
    - [scripts/runTimeCommand/togglePickmaskDynamic.py](scripts/runTimeCommand/togglePickmaskDynamic.py)
    - [scripts/runTimeCommand/togglePickmaskRendering.py](scripts/runTimeCommand/togglePickmaskRendering.py)
    - [scripts/runTimeCommand/togglePickmaskMisc.py](scripts/runTimeCommand/togglePickmaskMisc.py)
    - [scripts/runTimeCommand/togglePickmaskAll.py](scripts/runTimeCommand/togglePickmaskAll.py)
1. Toggle Pivot
    - [scripts/runTimeCommand/toggleDisplayRotatePivot.py](scripts/runTimeCommand/toggleDisplayRotatePivot.py)

## Installation
1. Download and unzip the mayaMatchmoveTools.zip file from [GitHub releases](https://github.com/kohyuk91/mayaMatchmoveTools/releases).

1. Drag and drop the `drag_and_drop_install.mel` file onto the Maya viewport.
    > ![doc/drag_and_drop_install.gif](doc/drag_and_drop_install.gif)<br>
1. Open `Hotkey Editor`
    1. Edit Hotkeys For: `Custom Scripts`
    1. Assign a Hotkey for each command
