# BSD 3-Clause License
#
# Copyright (c) 2020, Hyuk Ko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Documentaion:
# ZLOC is a 2.5D tracker system built for Science-D-Visions 3DEqualizer and Autodesk Maya. (Based on SynthPipe by Martin Kulig)
# Find out more at https://github.com/kohyuk91/zloc
#
# Versions:
# 0.1.3 - All versions does not require "Qt.py" anymore. Added 'if __name__ == "__main__": statement'.
# 0.1.2 - Maya 2017 and above does not require "Qt.py" anymore.
# 0.1.1 - Naming correction. "Epipolar Line" to "Projection Ray".
# 0.1.0 - Initial release
#
# Usage:
"""
import zloc_maya
try:
    zm.close()
    zm.deleteLater()
except:
    pass
zm = zloc_maya.ZLOC()
zm.show()
"""

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    import shiboken
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken


import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

import os
import random
import tempfile
import traceback
from functools import wraps


TEMPDIR = tempfile.gettempdir() # Get the path of the system's temp directory
# print(TEMPDIR):
# Windows >> c:\users\<USER>\appdata\local\temp
# Mac >> /var/folders/<...>
# Linux(CentOS) >> /usr/tmp

# Decorator for undo support.
def openCloseChunk(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        action = None
        try:
            mc.undoInfo(openChunk=True)
            action = func(*args, **kargs)
        except:
            print(traceback.format_exc())
            pass
        finally:
            mc.undoInfo(closeChunk=True)
            return action
    return wrapper


class ZLOC(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(ZLOC, self).__init__(self.maya_main_window())

        self.setWindowTitle("ZLOC")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setMaximumSize(0,0)

        self.MainTab = MainTab()
        self.AboutTab = AboutTab()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.main_tabWidget = QtWidgets.QTabWidget()
        self.main_tabWidget.addTab(self.MainTab, "Main")
        self.main_tabWidget.addTab(self.AboutTab, "About")

    def create_layouts(self):
        main_Layout = QtWidgets.QVBoxLayout(self)
        main_Layout.setContentsMargins(2, 2, 2, 2)
        main_Layout.addWidget(self.main_tabWidget)

    def create_connections(self):
        pass

class MainTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MainTab, self).__init__(parent)

        self.colorIndexList = [13,14,6,17,1,16,2,9,18,20,19,30]
        """
        13 # Red
        14 # Green
        6 # Blue
        17 # Yellow
        1 # Black
        16 # White
        2 # Gray
        9 # Purple
        18 # Cyan
        20 # Light Red
        19 # Light Green
        30 # Light Blue
        """

        self.int_validator = QtGui.QIntValidator()
        self.alphabet_whitespace_validator = QtGui.QRegExpValidator(QtCore.QRegExp("[a-z-A-Z\s_]+"))

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        #### Options ####
        self.frame_offset_le = QtWidgets.QLineEdit()
        self.frame_offset_le.setValidator(self.int_validator) # Frame Offset Line Edit will only allow "Integer".
        self.frame_offset_le.setText("0")
        self.flip_u_cb = QtWidgets.QCheckBox("U")
        self.flip_v_cb = QtWidgets.QCheckBox("V")
        self.random_color_cb = QtWidgets.QCheckBox()
        self.projection_ray_cb = QtWidgets.QCheckBox()
        self.projection_ray_cb.toggle() # Default is "ON".

        #### Rename ####
        self.prefix_lb = QtWidgets.QLabel("Prefix")
        self.prefix_le = QtWidgets.QLineEdit()
        self.prefix_le.setValidator(self.alphabet_whitespace_validator) # Prefix Line Edit will only allow "Alphabet" and "Whitespace".
        self.suffix_lb = QtWidgets.QLabel("Suffix")
        self.suffix_le = QtWidgets.QLineEdit()
        self.suffix_le.setValidator(self.alphabet_whitespace_validator) # Suffix Line Edit will only allow "Alphabet" and "Whitespace".

        #### Quick Import ####
        self.quick_import_btn = QtWidgets.QPushButton("Quick")
        self.quick_import_btn.setStyleSheet("QPushButton {background-color: #EC5f67;}")

        #### Manual Import ####
        self.manual_import_btn = QtWidgets.QPushButton("Manual")

        #### Create Null ####
        self.create_null_btn = QtWidgets.QPushButton("Null")

    def create_layouts(self):
        #### Options ####
        options_flip_Layout = QtWidgets.QHBoxLayout()
        options_flip_Layout.addWidget(self.flip_u_cb)
        options_flip_Layout.addWidget(self.flip_v_cb)

        options_GroupBox = QtWidgets.QGroupBox("Options")
        options_Layout = QtWidgets.QFormLayout()
        options_Layout.addRow("Frame Offset", self.frame_offset_le)
        options_Layout.addRow("Flip", options_flip_Layout)
        options_Layout.addRow("Random Color", self.random_color_cb)
        options_Layout.addRow("Projection Ray", self.projection_ray_cb)
        options_GroupBox.setLayout(options_Layout)

        #### Rename ####
        rename_GroupBox = QtWidgets.QGroupBox("Rename")
        rename_Layout = QtWidgets.QGridLayout()
        rename_Layout.addWidget(self.prefix_lb, 0, 0)
        rename_Layout.addWidget(self.prefix_le, 0, 1)
        rename_Layout.addWidget(self.suffix_lb, 1, 0)
        rename_Layout.addWidget(self.suffix_le, 1, 1)
        rename_GroupBox.setLayout(rename_Layout)

        #### Quick Import ####
        quick_import_GroupBox = QtWidgets.QGroupBox("")
        quick_import_Layout = QtWidgets.QHBoxLayout()
        quick_import_Layout.addWidget(self.quick_import_btn)
        quick_import_GroupBox.setLayout(quick_import_Layout)

        #### Manual Import ####
        manual_import_GroupBox = QtWidgets.QGroupBox("")
        manual_import_Layout = QtWidgets.QHBoxLayout()
        manual_import_Layout.addWidget(self.manual_import_btn)
        manual_import_GroupBox.setLayout(manual_import_Layout)

        #### Create Null ####
        create_null_GroupBox = QtWidgets.QGroupBox("")
        create_null_Layout = QtWidgets.QHBoxLayout()
        create_null_Layout.addWidget(self.create_null_btn)
        create_null_GroupBox.setLayout(create_null_Layout)

        main_Layout = QtWidgets.QVBoxLayout(self)
        main_Layout.addWidget(options_GroupBox)
        main_Layout.addWidget(rename_GroupBox)
        main_Layout.addWidget(quick_import_GroupBox)
        main_Layout.addWidget(manual_import_GroupBox)
        main_Layout.addWidget(create_null_GroupBox)

    def create_connections(self):
        self.quick_import_btn.clicked.connect(lambda: self.create_zloc("quick"))
        self.manual_import_btn.clicked.connect(lambda: self.create_zloc("manual"))
        self.create_null_btn.clicked.connect(lambda: self.create_zloc("null"))

    @openCloseChunk
    def create_zloc(self, mode):
        if self.one_camera_selected() == False: # Select "One" "Camera" type object.
            om.MGlobal.displayError("Please select a camera.")
            return

        selCamTrans = mc.ls(selection=True, long=True)[0]
        selCamShape = mc.listRelatives(selCamTrans, shapes=True, fullPath=True)[0]
        selCamHFA = mc.camera(selCamShape, q=True, hfa=True)
        selCamVFA = mc.camera(selCamShape, q=True, vfa=True)
        selCamUUID = mc.ls(selCamTrans, uuid=True)[0]
        selCamUUID_underscore = selCamUUID.replace("-", "_")
        selCamZLocGrp = "zloc_grp_{0}".format(selCamUUID_underscore)
        selCamZLocProjectionRayGrp = "zloc_projection_ray_grp_{0}".format(selCamUUID_underscore)

        ## Options ##
        frame_offset = int(self.frame_offset_le.text())
        flip_u = self.flip_checked("flip_u_cb") # If checked returns -1, else 1.
        flip_v = self.flip_checked("flip_v_cb") # If checked returns -1, else 1.
        random_color = self.random_color_cb.isChecked()
        projection_ray = self.projection_ray_cb.isChecked()

        ## Rename ##
        prefix = self.get_prefix()
        suffix = self.get_suffix()

        if mode == "quick":
            path = os.path.join(TEMPDIR, "quick.zloc")
            # print(path)
            # c:\users\<USER>\appdata\local\temp\zloc_quick.txt
        elif mode == "manual":
            try:
                path = mc.fileDialog2(fileFilter='*.zloc', dialogStyle=2, fileMode=1)[0]
            except:
                return None
        elif mode == "null":
            path = "null"

        if path == "":
            om.MGlobal.displayError("Something is wrong with the path.")
            return

        if mode == "null":
            word_list = ["null_zloc#", "1", "0.000000000000000", "0.000000000000000", "3"]
            # <name> + # to avoid name collision.
        else:
            with open(path,'r') as f:
                """
                print(f):
                zloc01 1 0.100000000000000 0.100000000000000 0
                zloc01 2 0.200000000000000 0.200000000000000 0
                zloc01 3 0.300000000000000 0.300000000000000 0
                zloc02 1 -0.100000000000000 -0.100000000000000 1
                zloc02 2 -0.200000000000000 -0.200000000000000 1
                zloc02 3 -0.300000000000000 -0.300000000000000 1
                """
                # About ZLOC Format
                # <name> <frame> <U> <V> <3DE4_color_index>

                word_list = [word for line in f for word in line.split()]
                """
                print(word_list):
                ["zloc01", "1", "0.100000000000000", "0.100000000000000", "0",
                 "zloc01", "2", "0.200000000000000", "0.200000000000000", "0",
                 "zloc01", "3", "0.300000000000000", "0.300000000000000", "0",
                 "zloc02", "1", "-0.100000000000000", "-0.100000000000000", "1",
                 "zloc02", "2", "-0.200000000000000", "-0.200000000000000", "1",
                 "zloc02", "3", "-0.300000000000000", "-0.300000000000000", "1"]
                """
        zloc_list = sorted(set(zip(word_list[0::5], word_list[4::5])))
        # Zip is for pairing every "0"th(Name) and "4"th(3DE4 Color Index) item.
        # Set is for removing dulplicates.
        # Sorted is for reordering items in alphabetical and numerical order.
        """
        print(zloc_list):
        [("zloc01","0"), ("zloc02","1")]
        """
        group_word_by_five_list = [word_list[i:i+5] for i in range(0, len(word_list), 5)]
        # "group_word_by_five_list" Result:
        """
        [["zloc01", "1", "0.100000000000000", "0.100000000000000", "0"],
         ["zloc01", "2", "0.200000000000000", "0.200000000000000", "0"],
         ["zloc01", "3", "0.300000000000000", "0.300000000000000", "0"],
         ["zloc02", "1", "-0.100000000000000", "-0.100000000000000", "1"],
         ["zloc02", "2", "-0.200000000000000", "-0.200000000000000", "1"],
         ["zloc02", "3", "-0.300000000000000", "-0.300000000000000", "1"]]
        """

        # Check for name collision
        for zloc, _ in zloc_list:
            if mc.objExists(prefix + zloc + suffix):
                om.MGlobal.displayError("Name collision detected. Please rename by using prefix and suffix.")
                return

        # Create ZLOC Group
        if mc.objExists(selCamZLocGrp): # ZLOC Group Exists
            pass
        else:
            mc.group(name=selCamZLocGrp, empty=True) # Create ZLOC Group
            mc.parentConstraint(selCamTrans, selCamZLocGrp, maintainOffset=False)
            mc.scaleConstraint(selCamTrans, selCamZLocGrp, maintainOffset=True)

        # Create ZLOC Projection Ray Group
        if projection_ray: # If Projection Ray checkbox is checked
            if mc.objExists(selCamZLocProjectionRayGrp): # ZLOC Projection Ray Group Exists
                pass
            else:
                mc.group(name=selCamZLocProjectionRayGrp, empty=True) # Create ZLOC Projection Ray Group
                mc.hide(selCamZLocProjectionRayGrp) # Hide ZLOC Projection Ray Group.
                mc.parentConstraint(selCamTrans, selCamZLocProjectionRayGrp, maintainOffset=False)
                mc.scaleConstraint(selCamTrans, selCamZLocProjectionRayGrp, maintainOffset=True)

        for zloc, tde4_color_index in zloc_list:
            # Create ZLOC
            zlocTrans = mc.spaceLocator(name=prefix + zloc + suffix)[0]
            zlocShape = mc.listRelatives(zlocTrans, shapes=True, fullPath=True)[0]

            # Set ZLOC Color
            if random_color: # If Random Color checkbox is checked
                zloc_color = random.choice(self.colorIndexList) # Pick a random index from "colorIndexList"
            else:
                zloc_color = self.get_color_from_index(tde4_color_index)
            mc.setAttr(zlocShape + '.overrideEnabled', 1) # Enable Color Override
            mc.setAttr(zlocShape + '.overrideColor', zloc_color) # Set Color

            # Add & Set Attributes
            mc.addAttr(zlocTrans, longName='U', attributeType='double', defaultValue=0)
            mc.addAttr(zlocTrans, longName='V', attributeType='double', defaultValue=0)
            mc.addAttr(zlocTrans, longName='OffsetU', attributeType='double', defaultValue=0) # Simillar to "Animation Layer".
            mc.addAttr(zlocTrans, longName='OffsetV', attributeType='double', defaultValue=0) # Simillar to "Animation Layer".
            mc.setAttr(zlocTrans + '.U', keyable=True)
            mc.setAttr(zlocTrans + '.V', keyable=True)
            mc.setAttr(zlocTrans + '.OffsetU', keyable=True)
            mc.setAttr(zlocTrans + '.OffsetV', keyable=True)
            mc.setAttr(zlocTrans + '.sx', 0.1)
            mc.setAttr(zlocTrans + '.sy', 0.1)
            mc.setAttr(zlocTrans + '.sz', 0.001)
            mc.setAttr(zlocTrans + '.tz', -10)

            # Expressions
            mc.expression(s="{0}.tx = {1}.hfa * 2.54 * {0}.tz / ({1}.fl / 10) * -1 * ({0}.U + {0}.OffsetU);".format(zlocTrans, selCamTrans), object=zlocTrans, alwaysEvaluate=True, unitConversion='all')
            mc.expression(s="{0}.ty = {1}.vfa * 2.54 * {0}.tz / ({1}.fl / 10) * -1 * ({0}.V + {0}.OffsetV);".format(zlocTrans, selCamTrans), object=zlocTrans, alwaysEvaluate=True, unitConversion='all')

            mc.parent(zlocTrans, selCamZLocGrp, relative=True) # Parent ZLOC to ZLOC Group

            # Projection Ray
            if projection_ray: # If Projection Ray checkbox is checked.
                projectionRayTrans = mc.curve(name= zlocTrans + "_projectionRay", degree=1, point=[(0,0,0),(0,0,-1000)]) # Create a Nurbs Curve. Length is 1000.
                projectionRayShape = mc.listRelatives(projectionRayTrans, shapes=True, fullPath=True)[0] # Get Shape Node's name.

                # Set Projection Ray Color
                mc.setAttr(projectionRayShape + '.overrideEnabled', 1) # Enable Color Override.
                mc.setAttr(projectionRayShape + '.overrideColor', zloc_color) # Set Color. Same Color as ZLOC.

                mc.aimConstraint(zlocTrans, projectionRayTrans, aimVector=[0.0, 0.0, -1.0], maintainOffset=False) # Aim Projection Ray to ZLOC.

                mc.parent(projectionRayTrans, selCamZLocProjectionRayGrp, relative=True)

        if mode != "null": # If mode is "null", skip this loop.
            # Set Keyframe for each ZLOC's "U" & "V" attributes.
            for i in range(len(group_word_by_five_list)):
                mc.setKeyframe(prefix + group_word_by_five_list[i][0] + suffix, t=int(group_word_by_five_list[i][1]) + frame_offset, v=float(group_word_by_five_list[i][2])/selCamHFA*flip_u, at='U')
                mc.setKeyframe(prefix + group_word_by_five_list[i][0] + suffix, t=int(group_word_by_five_list[i][1]) + frame_offset, v=float(group_word_by_five_list[i][3])/selCamVFA*flip_v, at='V')

        # Select Camera in the end
        mc.select(selCamTrans, replace=True)


    def one_camera_selected(self):
        selList = mc.ls(selection=True, long=True)
        if len(selList)==1 and mc.objectType(mc.listRelatives(selList, shapes=True, fullPath=True)[0]) == 'camera':
            return True
        else:
            return False

    def get_prefix(self):
        prefix = self.prefix_le.text().replace(" ", "_")
        if prefix == "":
            return ""
        else:
            return "{0}_".format(prefix)

    def get_suffix(self):
        suffix = self.suffix_le.text().replace(" ", "_")
        if suffix == "":
            return ""
        else:
            return "_{0}".format(suffix)

    def flip_checked(self, cb):
        exec("checked = self.{0}.isChecked()".format(cb))
        if checked:
            return -1
        else:
            return 1

    def get_color_from_index(self, tde4_color_index):
        color_dict = {
        # 3DE4 Color Index : Maya Color Index
        "0": 13, # Red
        "1": 14, # Green
        "2": 6, # Blue
        "3": 17, # Yellow
        "4": 1, # Black
        "5": 16, # White
        "6": 2, # Gray
        "7": 9, # Purple
        "8": 18, # Cyan
        "9": 20, # Light Red
        "10": 19, # Light Green
        "11": 30 # Light Blue
        }
        maya_color_index = color_dict[tde4_color_index]
        return maya_color_index

class AboutTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AboutTab, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        #### Author ####
        self.author_lb = QtWidgets.QLabel("<a href='https://www.linkedin.com/in/kohyuk91/' style='text-decoration:none'><font color=cyan>Hyuk Ko</font></a>")
        self.author_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.author_lb.setOpenExternalLinks(True)
        self.email_lb = QtWidgets.QLabel("kohyuk91@gmail.com")
        self.email_lb.setAlignment(QtCore.Qt.AlignCenter)

        #### Version ####
        self.version_lb = QtWidgets.QLabel("0.1.0")
        self.version_lb.setAlignment(QtCore.Qt.AlignCenter)

        #### Documentation ####
        self.github_lb = QtWidgets.QLabel("<a href='https://github.com/kohyuk91/zloc' style='text-decoration:none'><font color=cyan>GitHub</font></a>")
        self.github_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.github_lb.setOpenExternalLinks(True)

    def create_layouts(self):
        #### Author ####
        author_GroupBox = QtWidgets.QGroupBox("Author")
        author_Layout = QtWidgets.QVBoxLayout()
        author_Layout.addWidget(self.author_lb)
        author_Layout.addWidget(self.email_lb)
        author_Layout.addWidget(self.github_lb)
        author_GroupBox.setLayout(author_Layout)

        #### Version ####
        version_GroupBox = QtWidgets.QGroupBox("Version")
        version_Layout = QtWidgets.QHBoxLayout()
        version_Layout.addWidget(self.version_lb)
        version_GroupBox.setLayout(version_Layout)

        #### Documentation ####
        documentation_GroupBox = QtWidgets.QGroupBox("Documentation")
        documentation_Layout = QtWidgets.QHBoxLayout()
        documentation_Layout.addWidget(self.github_lb)
        documentation_GroupBox.setLayout(documentation_Layout)

        main_Layout = QtWidgets.QVBoxLayout(self)
        main_Layout.addWidget(author_GroupBox)
        main_Layout.addWidget(version_GroupBox)
        main_Layout.addWidget(documentation_GroupBox)
        main_Layout.addStretch()

    def create_connections(self):
        pass

if __name__ == "__main__":
    try:
        zm.close()
        zm.deleteLater()
    except:
        pass
    zm = ZLOC()
    zm.show()
