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
import overscan
reload(overscan)
try:
    o.close()
    o.deleteLater()
except:
    pass
o = overscan.Overscan()
o.show()
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

from functools import partial, wraps


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


class Overscan(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(Overscan, self).__init__(self.maya_main_window())

        self.setWindowTitle("Overscan")
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.presetList = [[1920,1080], [2048,1152], [2880,1620], [3840,2160]]

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.heroCameraLabel = QtWidgets.QLabel("Select Camera")
        self.heroCameraLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.heroCameraGetButton = QtWidgets.QPushButton("GET")
        self.heroCameraGetButton.setMaximumWidth(50)

        self.separatorLine1 = QtWidgets.QFrame()
        self.separatorLine1.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorLine1.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.org_width_label = QtWidgets.QLabel("ORG WIDTH")
        self.org_width_label.setAlignment(QtCore.Qt.AlignCenter)
        self.org_height_label = QtWidgets.QLabel("ORG HEIGHT")
        self.org_height_label.setAlignment(QtCore.Qt.AlignCenter)

        self.org_width_lineedit = QtWidgets.QLineEdit()
        self.org_height_lineedit = QtWidgets.QLineEdit()

        for preset in self.presetList:
            exec('self.preset_{0}_{1}_btn = QtWidgets.QPushButton("{0} X {1}")'.format(preset[0],preset[1]))

        self.separatorLine2 = QtWidgets.QFrame()
        self.separatorLine2.setFrameShape(QtWidgets.QFrame.HLine)
        self.separatorLine2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.overscan_btn = QtWidgets.QPushButton("OVERSCAN")
        self.overscan_btn.setMinimumHeight(75)

    def create_layouts(self):

        heroCameraLayout = QtWidgets.QHBoxLayout()
        heroCameraLayout.addWidget(self.heroCameraLabel)
        heroCameraLayout.addWidget(self.heroCameraGetButton)

        orgResolutionGroupBox = QtWidgets.QGroupBox()
        orgResolutionGridLayout = QtWidgets.QGridLayout()
        orgResolutionGridLayout.addWidget(self.org_width_label, 0, 0)
        orgResolutionGridLayout.addWidget(self.org_height_label, 0, 1)
        orgResolutionGridLayout.addWidget(self.org_width_lineedit, 1, 0)
        orgResolutionGridLayout.addWidget(self.org_height_lineedit, 1, 1)
        for preset in self.presetList:
            if self.presetList.index(preset)%2 == 0:
                exec('orgResolutionGridLayout.addWidget(self.preset_{0}_{1}_btn, self.presetList.index(preset)/2 + 2, self.presetList.index(preset)%2)'.format(preset[0],preset[1]))
            else:
                exec('orgResolutionGridLayout.addWidget(self.preset_{0}_{1}_btn, (self.presetList.index(preset)-1)/2 + 2, self.presetList.index(preset)%2)'.format(preset[0],preset[1]))
        orgResolutionGroupBox.setLayout(orgResolutionGridLayout)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addLayout(heroCameraLayout)
        mainLayout.addWidget(self.separatorLine1)
        mainLayout.addWidget(orgResolutionGroupBox)
        mainLayout.addWidget(self.separatorLine2)
        mainLayout.addWidget(self.overscan_btn)

    def create_connections(self):
        self.heroCameraGetButton.clicked.connect(self.get_heroCamera)
        for preset in self.presetList:
            exec("self.preset_{0}_{1}_btn.clicked.connect(partial(self.set_preset,'{0}','{1}'))".format(preset[0],preset[1]))
        self.overscan_btn.clicked.connect(self.compute_overscan)

    def get_heroCamera(self):
        if len(mc.ls(selection=True))==1 and mc.objectType(mc.listRelatives(mc.ls(selection=True), shapes=True)[0]) == 'camera':
            heroCameraTrans = mc.ls(selection=True, long=True)[0]
            heroCameraShape = mc.listRelatives(heroCameraTrans, shapes=True, fullPath=True)[0]
            self.heroCameraLabel.setText(heroCameraShape)
        else:
            mc.confirmDialog(title='WARNING', message='Select a Camera!')

    def set_preset(self, width, height):
        self.org_width_lineedit.setText(width)
        self.org_height_lineedit.setText(height)
        
    @openCloseChunk
    def compute_overscan(self):
        heroCameraShape = self.heroCameraLabel.text()
        imgPlaneTrans = mc.listConnections(heroCameraShape, type='imagePlane')[0]

        orgHFA = mc.getAttr(heroCameraShape + '.hfa')
        orgVFA = mc.getAttr(heroCameraShape + '.vfa')

        orgSizeX = mc.getAttr(imgPlaneTrans + '.sizeX')
        orgSizeY = mc.getAttr(imgPlaneTrans + '.sizeY')

        orgCoverageX = self.org_width_lineedit.text()
        orgCoverageY = self.org_height_lineedit.text()

        newCoverageX = mc.getAttr(imgPlaneTrans + '.coverageX')
        newCoverageY = mc.getAttr(imgPlaneTrans + '.coverageY')

        overscanX = newCoverageX / float(orgCoverageX)
        overscanY = newCoverageY / float(orgCoverageY)

        mc.setAttr(heroCameraShape + '.hfa', orgHFA * overscanX)
        mc.setAttr(heroCameraShape + '.vfa', orgVFA * overscanY)

        mc.setAttr(imgPlaneTrans + '.sizeX', orgSizeX * overscanX)
        mc.setAttr(imgPlaneTrans + '.sizeY', orgSizeY * overscanY)

if __name__ == "__main__":
    try:
        o.close()
        o.deleteLater()
    except:
        pass
    o = Overscan()
    o.show()
