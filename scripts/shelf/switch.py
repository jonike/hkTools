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
# Switches motion between a Static Object and a Dynamic Object.
# ex) Static Camera & Dynamic Cube >> Dynamic Camera & Static Cube

# Usage:
# 1.Run Script
"""
import switch
reload(switch)
try:
    s.close()
    s.deleteLater()
except:
    pass
s = switch.Switch()
s.show()
"""
# 2.Select Static Object and hit "Get"
# 3.Select Dynamic Object and hit "Get"
# 4.Hit "Switch"

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


from functools import wraps


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


class Switch(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(Switch, self).__init__(self.maya_main_window())

        self.setWindowTitle("Switch")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setMaximumSize(0,0)

        self.big_font = QtGui.QFont()
        self.big_font.setPointSize(12)
        self.big_font.setBold(True)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        #### Static & Dynamic Object ####
        self.static_object_lb = QtWidgets.QLabel("Static Object")
        self.static_object_lb.setMinimumWidth(90)
        self.static_object_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.static_object_input_lb = QtWidgets.QLabel()
        self.static_object_input_lb.setStyleSheet("QLabel {background-color: #222222;}")
        self.static_object_input_lb.setMinimumWidth(150)
        self.static_object_input_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.static_object_btn = QtWidgets.QPushButton("GET")
        self.static_object_btn.setStyleSheet("QPushButton {background-color: #EC5f67;}")
        self.static_object_btn.setMinimumWidth(40)

        self.dynamic_object_lb = QtWidgets.QLabel("Dynamic Object")
        self.dynamic_object_lb.setMinimumWidth(90)
        self.dynamic_object_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.dynamic_object_input_lb = QtWidgets.QLabel()
        self.dynamic_object_input_lb.setStyleSheet("QLabel {background-color: #222222;}")
        self.dynamic_object_input_lb.setMinimumWidth(150)
        self.dynamic_object_input_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.dynamic_object_btn = QtWidgets.QPushButton("GET")
        self.dynamic_object_btn.setStyleSheet("QPushButton {background-color: #EC5f67;}")
        self.dynamic_object_btn.setMinimumWidth(40)
        #### Static & Dynamic Object ####

        #### Switch ####
        self.switch_btn = QtWidgets.QPushButton("Switch")
        self.switch_btn.setFont(self.big_font)
        self.switch_btn.setFixedSize(70,35)
        self.switch_btn.setStyleSheet("QPushButton {background-color: #EC5f67;}")
        #### Switch ####

    def create_layouts(self):
        #### Static & Dynamic Object ####
        static_dynamic_object_GroupBox = QtWidgets.QGroupBox()
        static_dynamic_object_Layout = QtWidgets.QGridLayout()
        static_dynamic_object_Layout.addWidget(self.static_object_lb, 0, 0)
        static_dynamic_object_Layout.addWidget(self.static_object_input_lb, 0, 1)
        static_dynamic_object_Layout.addWidget(self.static_object_btn, 0, 2)
        static_dynamic_object_Layout.addWidget(self.dynamic_object_lb, 1, 0)
        static_dynamic_object_Layout.addWidget(self.dynamic_object_input_lb, 1, 1)
        static_dynamic_object_Layout.addWidget(self.dynamic_object_btn, 1, 2)
        static_dynamic_object_GroupBox.setLayout(static_dynamic_object_Layout)
        #### Static & Dynamic Object ####

        main_Layout = QtWidgets.QHBoxLayout(self)
        main_Layout.addWidget(static_dynamic_object_GroupBox)
        main_Layout.addWidget(self.switch_btn)

    def create_connections(self):
        self.static_object_btn.clicked.connect(lambda: self.get_object("static"))
        self.dynamic_object_btn.clicked.connect(lambda: self.get_object("dynamic"))
        self.switch_btn.clicked.connect(self.switch_motion)

    def get_object(self, mode):
        sel_trans = mc.ls(selection=True, long=True)
        if len(sel_trans) == 1:
            if mode=="static":
                self.static_object_input_lb.setText(sel_trans[0])
            if mode=="dynamic":
                self.dynamic_object_input_lb.setText(sel_trans[0])
        else:
            om.MGlobal.displayError("Please select exactly 'one' object.")
            return None

    @openCloseChunk
    def switch_motion(self):
        if self.dynamic_object_input_lb.text() != "" or self.static_object_input_lb.text() != "":
            attr_list = ["tx","ty","tz","rx","ry","rz"]
            start_frame = mc.playbackOptions(q=True, minTime=True)
            end_frame = mc.playbackOptions(q=True, maxTime=True)

            dynamic_trans = self.dynamic_object_input_lb.text()
            static_trans = self.static_object_input_lb.text()

            dynamic_grp = mc.group(name="dynamic_grp", empty=True)
            static_grp = mc.group(name="static_grp", empty=True)
            mc.parent(static_grp, dynamic_grp)

            dynamic_group_pc = mc.parentConstraint(dynamic_trans, dynamic_grp, maintainOffset=False)[0]
            static_group_pc = mc.parentConstraint(static_trans, static_grp, maintainOffset=False)[0]

            mc.bakeResults(static_grp, attribute=attr_list, time=(start_frame, end_frame))

            mc.delete(static_group_pc)

            # Mute Dynamic Object & Dynamic Group
            for attr in attr_list:
                mc.mute("{0}.{1}".format(dynamic_trans, attr))
                mc.mute("{0}.{1}".format(dynamic_grp, attr))

            static_trans_pc = mc.parentConstraint(static_grp, static_trans, maintainOffset=False)[0] # Parent Constraint Static Object to Static Group
            mc.bakeResults(static_trans, attribute=attr_list, time=(start_frame, end_frame))
            mc.delete(static_trans_pc, dynamic_grp)
        else:
            om.MGlobal.displayError("Staic Object or Dynamic Object is empty.")
            return None


if __name__ == "__main__":
    try:
        s.close()
        s.deleteLater()
    except:
        pass
    s = Switch()
    s.show()
