# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91


import os
import re

import maya.cmds as mc


DEFAULT_PADDING = 3


def paddingExistsInBasename(baseName):
    result = re.search(r"_v\d*.", baseName)
    if result == None:
        return False
    return True


def paddingExistsInFiles(matchList):
    matchListString = " ".join(matchList)
    
    result = re.search(r"_v\d*.", matchListString)
    if result == None:
        return False
    return True


def getPadding( matchList):
    pattern = re.compile(r"_v\d*.")
    for match in matchList:
        version = pattern.findall(match)
        versionStripped = version[0][2:-1]
        padding = len(versionStripped)
    return padding


def newSceneVersion(currentScenePath):
    
    currentSceneDir, currentSceneFile = os.path.split(currentScenePath)
    currentSceneBasename, currentSceneExt = os.path.splitext(currentSceneFile)

    fileList = os.listdir(currentSceneDir)
    fileListString = " ".join(fileList)

    # If current scene name has no "_v#"
    # e.g. currentSceneFile >> "blasterWalk.ma"
    # e.g. currentSceneBasename >> "blasterWalk"
    if not paddingExistsInBasename(currentSceneBasename):

        # We have to check the extention because files might have same basename but different extention(e.g. ".ma", ".mb")
        pattern = re.compile(r"{baseName}_v\d*{ext}".format(baseName=currentSceneBasename, ext=currentSceneExt))
        matchList = pattern.findall(fileListString)
        
        padding = getPadding(matchList) if paddingExistsInFiles(matchList) else DEFAULT_PADDING
        
        # Get list of all "blasterWalk_v#.ma" in same directory.
        # The current scene does not have "_v#",
        # but there might be a file in the same directory that already follows the naming convention "blasterWalk_v###.ma"
        versionList = []
        for match in matchList:
            try:
                versionPattern = re.compile(r"_v\d{{{padding}}}.".format(padding=padding))
                version = int(versionPattern.findall(match)[0][2:padding+2])
                versionList.append(version)
            except:
                pass

        # If there is no file that follows the naming convention "blasterWalk_v#.ma", save v001.
        # e.g. blasterWalk_v001.ma
        if len(versionList) == 0:
            newSceneVersionFile = "{baseName}_v{nextVer:0{padding}d}{ext}".format(baseName=currentSceneBasename, nextVer=1, padding=padding, ext=currentSceneExt)
            newSceneVersionPath = os.path.join(currentSceneDir, newSceneVersionFile)
            return newSceneVersionPath

        # If there is a file that follows the naming convention "blasterWalk_v#.ma", find the next available version and save.
        # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v002.ma] >> Result: blasterWalk_v003.ma
        # e.g. Files with same naming convention in directory: [blasterWalk_v0001.ma, blasterWalk_v0002.ma] >> Result: blasterWalk_v0003.ma
        # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v003.ma] >> Result: blasterWalk_v004.ma | Skips "blasterWalk_v002.ma"
        # e.g. Files with same naming convention in directory: [blasterWalk_v0001.ma, blasterWalk_v0003.ma] >> Result: blasterWalk_v0004.ma | Skips "blasterWalk_v002.ma"
        maxVersion = max(versionList)
        nextVersion = maxVersion + 1

        newSceneVersionFile = "{baseName}_v{nextVer:0{padding}d}{ext}".format(baseName=currentSceneBasename, nextVer=nextVersion, padding=padding, ext=currentSceneExt)
        newSceneVersionPath = os.path.join(currentSceneDir, newSceneVersionFile)
        return newSceneVersionPath


    # If current scene name has "_v#"
    # e.g. currentSceneFile >> "blasterWalk_v001.ma"
    # e.g. currentSceneBasename >> "blasterWalk_v001"
    # Get list of all "blasterWalk_v#.ma" in same directory.
    
    # Remove "_v#" from basename
    currentSceneBasenameVersionStripped = re.sub(r"_v\d*", "", currentSceneBasename)

    # We have to check the extention because files might have same basename but different extention(e.g. ".ma", ".mb")
    pattern = re.compile(r"{baseName}_v\d*{ext}".format(baseName=currentSceneBasenameVersionStripped, ext=currentSceneExt))
    matchList = pattern.findall(fileListString)
    
    padding = getPadding(matchList)

    versionList = []
    for match in matchList:
        try:
            versionPattern = re.compile(r"_v\d{{{padding}}}.".format(padding=padding))
            version = int(versionPattern.findall(match)[0][2:padding+2])
            versionList.append(version)
        except:
            pass


    # If there is a file that follows the naming convention "blasterWalk_v###.ma", find the next available version and save.
    # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v002.ma] >> Result: blasterWalk_v003.ma
    # e.g. Files with same naming convention in directory: [blasterWalk_v001.ma, blasterWalk_v003.ma] >> Result: blasterWalk_v004.ma | Skips "blasterWalk_v002.ma"
    maxVersion = max(versionList)
    nextVersion = maxVersion + 1

    newSceneVersionFile = "{baseName}_v{nextVer:0{padding}d}{ext}".format(baseName=currentSceneBasenameVersionStripped, nextVer=nextVersion, padding=padding, ext=currentSceneExt)
    newSceneVersionPath = os.path.join(currentSceneDir, newSceneVersionFile)
    return newSceneVersionPath


def main():
    currentScenePath = mc.file(q=1, sn=1)
    if currentScenePath == "":
        mc.warning("You must save a scene first.")
        return

    currentSceneDir, currentSceneFile = os.path.split(currentScenePath)
    currentSceneBasename, currentSceneExt = os.path.splitext(currentSceneFile)

    newSceneVersionPath = newSceneVersion(currentScenePath)

    if currentSceneExt == ".ma": fileType = "mayaAscii"
    if currentSceneExt == ".mb": fileType = "mayaBinary"

    # Rename and Save
    mc.file(rename=newSceneVersionPath)
    mc.file(save=True, type=fileType)

    print newSceneVersionPath


if __name__ == "__main__":
    main()
