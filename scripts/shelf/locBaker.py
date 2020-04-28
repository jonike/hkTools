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


"""
import locBaker
reload(locBaker)
try:
    lb.close()
    lb.deleteLater()
except:
    pass
lb = locBaker.LocBaker()
lb.show()
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

import traceback
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


class LocBaker(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(LocBaker, self).__init__(self.maya_main_window())
        self.setMaximumWidth(200)

        self.setWindowTitle("Loc Baker")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        #self.setStyleSheet("QDialog {background-color: rgb(25, 25, 25);} QGroupBox {background-color: rgb(35, 35, 35); border: 10px solid rgb(35, 35, 35);}")

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.start_frame_lb = QtWidgets.QLabel("Start")
        self.start_frame_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.end_frame_lb = QtWidgets.QLabel("End")
        self.end_frame_lb.setAlignment(QtCore.Qt.AlignCenter)

        self.start_frame_le = QtWidgets.QLineEdit()
        self.start_frame_le.setText(str(int(mc.playbackOptions(q=True, minTime=True))))
        self.this_frame_update_btn = QtWidgets.QPushButton()
        self.this_frame_update_btn.setIcon(QtGui.QIcon(":centerCurrentTime.png"))
        self.end_frame_le = QtWidgets.QLineEdit()
        self.end_frame_le.setText(str(int(mc.playbackOptions(q=True, maxTime=True))))

        self.start_frame_update_btn = QtWidgets.QPushButton()
        self.start_frame_update_btn.setIcon(QtGui.QIcon(":timestart.png"))
        self.reset_update_btn = QtWidgets.QPushButton()
        self.reset_update_btn.setIcon(QtGui.QIcon(":refresh.png"))
        self.end_frame_update_btn = QtWidgets.QPushButton()
        self.end_frame_update_btn.setIcon(QtGui.QIcon(":timeend.png"))

        self.point_x_cb = QtWidgets.QCheckBox("X")
        self.point_x_cb.toggle()
        self.point_y_cb = QtWidgets.QCheckBox("Y")
        self.point_y_cb.toggle()
        self.point_z_cb = QtWidgets.QCheckBox("Z")
        self.point_z_cb.toggle()

        self.orient_x_cb = QtWidgets.QCheckBox("X")
        self.orient_x_cb.toggle()
        self.orient_y_cb = QtWidgets.QCheckBox("Y")
        self.orient_y_cb.toggle()
        self.orient_z_cb = QtWidgets.QCheckBox("Z")
        self.orient_z_cb.toggle()

        self.scale_x_cb = QtWidgets.QCheckBox("X")
        self.scale_x_cb.toggle()
        self.scale_y_cb = QtWidgets.QCheckBox("Y")
        self.scale_y_cb.toggle()
        self.scale_z_cb = QtWidgets.QCheckBox("Z")
        self.scale_z_cb.toggle()

        self.rotateOrder_inherit_rb = QtWidgets.QRadioButton("Inherit")
        self.rotateOrder_inherit_rb.toggle()
        self.rotateOrder_xyz_rb = QtWidgets.QRadioButton("XYZ")
        self.rotateOrder_yzx_rb = QtWidgets.QRadioButton("YZX")
        self.rotateOrder_zxy_rb = QtWidgets.QRadioButton("ZXY")
        self.rotateOrder_xzy_rb = QtWidgets.QRadioButton("XZY")
        self.rotateOrder_yxz_rb = QtWidgets.QRadioButton("YXZ")
        self.rotateOrder_zyx_rb = QtWidgets.QRadioButton("ZYX")

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.bake_btn = QtWidgets.QPushButton("Bake")

    def create_layouts(self):
        frame_range_groupbox = QtWidgets.QGroupBox("Range")
        frame_range_layout = QtWidgets.QGridLayout()
        frame_range_layout.addWidget(self.start_frame_lb, 0, 0)
        frame_range_layout.addWidget(self.end_frame_lb, 0, 2)
        frame_range_layout.addWidget(self.start_frame_le, 1, 0)
        frame_range_layout.addWidget(self.this_frame_update_btn, 1, 1)
        frame_range_layout.addWidget(self.end_frame_le, 1, 2)
        frame_range_layout.addWidget(self.start_frame_update_btn, 2, 0)
        frame_range_layout.addWidget(self.reset_update_btn, 2, 1)
        frame_range_layout.addWidget(self.end_frame_update_btn, 2, 2)
        frame_range_groupbox.setLayout(frame_range_layout)

        self.point_groupbox = QtWidgets.QGroupBox("Point")
        point_layout = QtWidgets.QHBoxLayout()
        point_layout.addWidget(self.point_x_cb)
        point_layout.addWidget(self.point_y_cb)
        point_layout.addWidget(self.point_z_cb)
        self.point_groupbox.setLayout(point_layout)
        self.point_groupbox.setCheckable(True)
        self.point_groupbox.setChecked(True)

        self.orient_groupbox = QtWidgets.QGroupBox("Orient")
        orient_layout = QtWidgets.QHBoxLayout()
        orient_layout.addWidget(self.orient_x_cb)
        orient_layout.addWidget(self.orient_y_cb)
        orient_layout.addWidget(self.orient_z_cb)
        self.orient_groupbox.setLayout(orient_layout)
        self.orient_groupbox.setCheckable(True)
        self.orient_groupbox.setChecked(True)

        self.scale_groupbox = QtWidgets.QGroupBox("Scale")
        scale_layout = QtWidgets.QHBoxLayout()
        scale_layout.addWidget(self.scale_x_cb)
        scale_layout.addWidget(self.scale_y_cb)
        scale_layout.addWidget(self.scale_z_cb)
        self.scale_groupbox.setLayout(scale_layout)
        self.scale_groupbox.setCheckable(True)
        self.scale_groupbox.setChecked(True)

        rotateOrder_groupbox = QtWidgets.QGroupBox("Rotate Order")
        rotateOrder_layout = QtWidgets.QGridLayout()
        rotateOrder_layout.addWidget(self.rotateOrder_inherit_rb, 0, 0, 1, 0)
        rotateOrder_layout.addWidget(self.rotateOrder_xyz_rb, 1, 0)
        rotateOrder_layout.addWidget(self.rotateOrder_yzx_rb, 1, 1)
        rotateOrder_layout.addWidget(self.rotateOrder_zxy_rb, 1, 2)
        rotateOrder_layout.addWidget(self.rotateOrder_xzy_rb, 2, 0)
        rotateOrder_layout.addWidget(self.rotateOrder_yxz_rb, 2, 1)
        rotateOrder_layout.addWidget(self.rotateOrder_zyx_rb, 2, 2)
        rotateOrder_groupbox.setLayout(rotateOrder_layout)

        bake_groupbox = QtWidgets.QGroupBox()
        bake_layout = QtWidgets.QHBoxLayout()
        bake_layout.addWidget(self.apply_btn)
        bake_layout.addWidget(self.bake_btn)
        bake_groupbox.setLayout(bake_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(frame_range_groupbox)
        main_layout.addWidget(self.point_groupbox)
        main_layout.addWidget(self.orient_groupbox)
        main_layout.addWidget(self.scale_groupbox)
        main_layout.addWidget(rotateOrder_groupbox)
        main_layout.addWidget(bake_groupbox)

    def create_connections(self):
        self.this_frame_update_btn.clicked.connect(lambda: self.update("this"))
        self.start_frame_update_btn.clicked.connect(lambda: self.update("start"))
        self.reset_update_btn.clicked.connect(lambda: self.update("reset"))
        self.end_frame_update_btn.clicked.connect(lambda: self.update("end"))
        self.apply_btn.clicked.connect(lambda: self.bake("apply"))
        self.bake_btn.clicked.connect(lambda: self.bake("bake"))

    def update(self, mode):
        if mode == "this":
            self.start_frame_le.setText(str(int(mc.currentTime(q=True))))
            self.end_frame_le.setText(str(int(mc.currentTime(q=True))))
        if mode == "start":
            self.start_frame_le.setText(str(int(mc.currentTime(q=True))))
        if mode == "end":
            self.end_frame_le.setText(str(int(mc.currentTime(q=True))))
        if mode == "reset":
            self.start_frame_le.setText(str(int(mc.playbackOptions(q=True, minTime=True))))
            self.end_frame_le.setText(str(int(mc.playbackOptions(q=True, maxTime=True))))

    @openCloseChunk
    def bake(self, mode):
        # Get List of selected Transform Nodes
        selTransList = mc.ls(selection=True, transforms=True, long=True)

        locList = []
        pcList = []
        ocList = []
        scList = []
        for trans in selTransList:
            # Create Locator
            #loc = mc.spaceLocator(name="baked{0}".format(trans))[0]
            loc = mc.spaceLocator(name="bakerLoc_#")[0]
            locList.append(loc)

            # Set Rotate Order
            if self.rotateOrder_inherit_rb.isChecked(): mc.setAttr(loc+".rotateOrder", mc.getAttr(trans+".rotateOrder"))
            if self.rotateOrder_xyz_rb.isChecked(): mc.setAttr(loc+".rotateOrder", 0)
            if self.rotateOrder_yzx_rb.isChecked(): mc.setAttr(loc+".rotateOrder", 1)
            if self.rotateOrder_zxy_rb.isChecked(): mc.setAttr(loc+".rotateOrder", 2)
            if self.rotateOrder_xzy_rb.isChecked(): mc.setAttr(loc+".rotateOrder", 3)
            if self.rotateOrder_yxz_rb.isChecked(): mc.setAttr(loc+".rotateOrder", 4)
            if self.rotateOrder_zyx_rb.isChecked(): mc.setAttr(loc+".rotateOrder", 5)

            if self.point_groupbox.isChecked():
                pskip = ""
                if self.point_x_cb.isChecked() == False: pskip += ", skip='x'"
                if self.point_y_cb.isChecked() == False: pskip += ", skip='y'"
                if self.point_z_cb.isChecked() == False: pskip += ", skip='z'"
                exec("pc = mc.pointConstraint(trans, loc, maintainOffset=False {0})".format(pskip))
                pcList.append(pc)
            if self.orient_groupbox.isChecked():
                oskip = ""
                if self.orient_x_cb.isChecked() == False: skip += ", skip='x'"
                if self.orient_y_cb.isChecked() == False: skip += ", skip='y'"
                if self.orient_z_cb.isChecked() == False: skip += ", skip='z'"
                exec("oc = mc.orientConstraint(trans, loc, maintainOffset=False {0})".format(oskip))
                ocList.append(oc)
            if self.scale_groupbox.isChecked():
                sskip = ""
                if self.scale_x_cb.isChecked() == False: skip += ", skip='x'"
                if self.scale_y_cb.isChecked() == False: skip += ", skip='y'"
                if self.scale_z_cb.isChecked() == False: skip += ", skip='z'"
                exec("sc = mc.scaleConstraint(trans, loc, maintainOffset=False {0})".format(sskip))
                scList.append(sc)

        # Bake
        if self.start_frame_le.text() != self.end_frame_le.text(): # If Start & End Frame is not same, Bake.
            mc.bakeResults(locList, simulation=True, attribute=["tx","ty","tz","rx","ry","rz","sx","sy","sz"], time=(self.start_frame_le.text(), self.end_frame_le.text()))

        # Delete Constraints
        for pc in pcList:
            try:
                mc.delete(pc)
            except:
                pass
        for oc in ocList:
            try:
                mc.delete(oc)
            except:
                pass
        for sc in scList:
            try:
                mc.delete(sc)
            except:
                pass

        mc.select(clear=True)


        ## Close Window ##
        if mode == "bake":
            self.close()
            self.deleteLater()


if __name__ == "__main__":
    try:
        lb.close()
        lb.deleteLater()
    except:
        pass
    lb = LocBaker()
    lb.show()
