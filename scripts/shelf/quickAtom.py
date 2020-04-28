# Author : HYUK KO | kohyuk91@gmail.com | github.com/kohyuk91

"""
import quickAtom
try:
    qa.close()
    qa.deleteLater()
except:
    pass
qa = quickAtom.QuickAtom()
qa.show()
"""

import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    import shiboken
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    import shiboken2 as shiboken

import os
import tempfile


TMPDIR = tempfile.gettempdir()


def checkPluginLoaded(pluginName):
    # get plugins
    plugins = mc.pluginInfo( query=True, listPlugins=True )

    # loop over plugins
    plugin_loaded = False
    if plugins != None:
        for i in plugins:
            i = i.lower()
            if i.find(pluginName.lower()) != -1:
                plugin_loaded = True
    return plugin_loaded


# check plugin is loaded, if not, load it!
def loadPlugin(pluginName):
    loaded = checkPluginLoaded(pluginName)
    if not loaded:
        mc.loadPlugin(pluginName)

    loaded = checkPluginLoaded(pluginName)
    if not loaded:
        msg = 'Could not automatically load plug-in %s, You must load it manually.'
        mc.error(msg % repr(pluginName))
    return loaded



class QuickAtom(QtWidgets.QDialog):
    @classmethod
    def maya_main_window(cls):
        main_window_ptr = omui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


    def __init__(self):
        super(QuickAtom, self).__init__(self.maya_main_window())

        self.setWindowTitle("Quick ATOM")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.loadSettings()

    def create_widgets(self):
        self.export_include_lb = QtWidgets.QLabel("Include:")
        self.export_include_setDrivenKeys_cb = QtWidgets.QCheckBox("Set Driven Keys")
        self.export_include_setDrivenKeys_cb.toggle()
        self.export_include_constraints_cb = QtWidgets.QCheckBox("Constraints")
        self.export_include_constraints_cb.toggle()
        self.export_include_animationLayers_cb = QtWidgets.QCheckBox("Animation Layers")
        self.export_include_animationLayers_cb.toggle()
        self.export_include_staticValues_cb = QtWidgets.QCheckBox("Static Values")
        self.export_include_staticValues_cb.toggle()
        self.export_include_bakedAnimation_cb = QtWidgets.QCheckBox("Baked Animation")
        self.export_include_bakedAnimation_cb.toggle()
        self.export_include_controlPoints_cb = QtWidgets.QCheckBox("Control Points")
        self.export_include_controlPoints_cb.toggle()

        self.export_hierarchy_lb = QtWidgets.QLabel("Hierarchy:")
        self.export_hierarchy_selected_rb = QtWidgets.QRadioButton("Selected")
        self.export_hierarchy_selected_rb.toggle()
        self.export_hierarchy_below_rb = QtWidgets.QRadioButton("Below")
        self.export_btn = QtWidgets.QPushButton("Export")

        self.import_hierarchy_lb = QtWidgets.QLabel("Hierarchy:")
        self.import_hierarchy_selected_rb = QtWidgets.QRadioButton("Selected")
        self.import_hierarchy_selected_rb.toggle()
        self.import_hierarchy_below_rb = QtWidgets.QRadioButton("Below")
        self.import_btn = QtWidgets.QPushButton("Import")


    def create_layouts(self):
        self.export_groupbox = QtWidgets.QGroupBox("Export")
        export_layout = QtWidgets.QGridLayout()
        export_layout.addWidget(self.export_include_lb, 0, 0)
        export_layout.addWidget(self.export_include_setDrivenKeys_cb, 0, 1, 1, 2)
        export_layout.addWidget(self.export_include_constraints_cb, 1, 1, 1, 2)
        export_layout.addWidget(self.export_include_animationLayers_cb, 2, 1, 1, 2)
        export_layout.addWidget(self.export_include_staticValues_cb, 3, 1, 1, 2)
        export_layout.addWidget(self.export_include_bakedAnimation_cb, 4, 1, 1, 2)
        export_layout.addWidget(self.export_include_controlPoints_cb, 5, 1, 1, 2)

        export_layout.addWidget(self.export_hierarchy_lb, 6, 0)
        export_layout.addWidget(self.export_hierarchy_selected_rb, 6, 1)
        export_layout.addWidget(self.export_hierarchy_below_rb, 6, 2)
        export_layout.addWidget(self.export_btn, 7, 0, 1, 3)
        self.export_groupbox.setLayout(export_layout)

        self.import_groupbox = QtWidgets.QGroupBox("Import")
        import_layout = QtWidgets.QGridLayout()
        import_layout.addWidget(self.import_hierarchy_lb, 0, 0)
        import_layout.addWidget(self.import_hierarchy_selected_rb, 0, 1)
        import_layout.addWidget(self.import_hierarchy_below_rb, 0, 2)
        import_layout.addWidget(self.import_btn, 1, 0, 1, 3)
        self.import_groupbox.setLayout(import_layout)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.export_groupbox)
        main_layout.addWidget(self.import_groupbox)


    def create_connections(self):
        self.export_btn.clicked.connect(lambda: self.atom("atomExport"))
        self.import_btn.clicked.connect(lambda: self.atom("atomImport"))


    def getAtomFilepath(self):
        atomFileName = "quick.atom"
        atomFilePath = os.path.join(TMPDIR, atomFileName)
        return atomFilePath


    def loadSettings(self):
        if mc.optionVar(exists="quickAtom_export_include_setDrivenKeys_cb"):
            self.export_include_setDrivenKeys_cb.setChecked(True) if mc.optionVar(q="quickAtom_export_include_setDrivenKeys_cb") else self.export_include_setDrivenKeys_cb.setChecked(False)
        if mc.optionVar(exists="quickAtom_export_include_constraints_cb"):
            self.export_include_constraints_cb.setChecked(True) if mc.optionVar(q="quickAtom_export_include_constraints_cb") else self.export_include_constraints_cb.setChecked(False)
        if mc.optionVar(exists="quickAtom_export_include_animationLayers_cb"):
            self.export_include_animationLayers_cb.setChecked(True) if mc.optionVar(q="quickAtom_export_include_animationLayers_cb") else self.export_include_animationLayers_cb.setChecked(False)
        if mc.optionVar(exists="quickAtom_export_include_staticValues_cb"):
            self.export_include_staticValues_cb.setChecked(True) if mc.optionVar(q="quickAtom_export_include_staticValues_cb") else self.export_include_staticValues_cb.setChecked(False)
        if mc.optionVar(exists="quickAtom_export_include_bakedAnimation_cb"):
            self.export_include_bakedAnimation_cb.setChecked(True) if mc.optionVar(q="quickAtom_export_include_bakedAnimation_cb") else self.export_include_bakedAnimation_cb.setChecked(False)
        if mc.optionVar(exists="quickAtom_export_include_controlPoints_cb"):
            self.export_include_controlPoints_cb.setChecked(True) if mc.optionVar(q="quickAtom_export_include_controlPoints_cb") else self.export_include_controlPoints_cb.setChecked(False)

        if mc.optionVar(exists="quickAtom_export_hierarchy_selected_rb"):
            if mc.optionVar(q="quickAtom_export_hierarchy_selected_rb"): self.export_hierarchy_selected_rb.setChecked(True)
        if mc.optionVar(exists="quickAtom_export_hierarchy_below_rb"):
            if mc.optionVar(q="quickAtom_export_hierarchy_below_rb"): self.export_hierarchy_below_rb.setChecked(True)

        if mc.optionVar(exists="quickAtom_import_hierarchy_selected_rb"):
            if mc.optionVar(q="quickAtom_import_hierarchy_selected_rb"): self.import_hierarchy_selected_rb.setChecked(True)
        if mc.optionVar(exists="quickAtom_import_hierarchy_below_rb"):
            if mc.optionVar(q="quickAtom_import_hierarchy_below_rb"): self.import_hierarchy_below_rb.setChecked(True)


    def saveSettings(self):
        mc.optionVar(intValue=("quickAtom_export_include_setDrivenKeys_cb", self.export_include_setDrivenKeys_cb.isChecked()))
        mc.optionVar(intValue=("quickAtom_export_include_constraints_cb", self.export_include_constraints_cb.isChecked()))
        mc.optionVar(intValue=("quickAtom_export_include_animationLayers_cb", self.export_include_animationLayers_cb.isChecked()))
        mc.optionVar(intValue=("quickAtom_export_include_staticValues_cb", self.export_include_staticValues_cb.isChecked()))
        mc.optionVar(intValue=("quickAtom_export_include_bakedAnimation_cb", self.export_include_bakedAnimation_cb.isChecked()))
        mc.optionVar(intValue=("quickAtom_export_include_controlPoints_cb", self.export_include_controlPoints_cb.isChecked()))

        mc.optionVar(intValue=("quickAtom_export_hierarchy_selected_rb", self.export_hierarchy_selected_rb.isChecked()))
        mc.optionVar(intValue=("quickAtom_export_hierarchy_below_rb", self.export_hierarchy_below_rb.isChecked()))

        mc.optionVar(intValue=("quickAtom_import_hierarchy_selected_rb", self.import_hierarchy_selected_rb.isChecked()))
        mc.optionVar(intValue=("quickAtom_import_hierarchy_below_rb", self.import_hierarchy_below_rb.isChecked()))


    def atom(self, mode):
        loadPlugin("atomImportExport")

        atomFilePath = self.getAtomFilepath()

        if mode == "atomExport":
            # Get Checkbox and RadioButton state
            self.setDrivenKeys = 1 if self.export_include_setDrivenKeys_cb.isChecked() else 0
            self.constraints = 1 if self.export_include_constraints_cb.isChecked() else 0
            self.animationLayers = 1 if self.export_include_animationLayers_cb.isChecked() else 0
            self.staticValues = 1 if self.export_include_staticValues_cb.isChecked() else 0
            self.bakedAnimation = 1 if self.export_include_bakedAnimation_cb.isChecked() else 0
            self.controlPoints = 1 if self.export_include_controlPoints_cb.isChecked() else 0
            if self.export_hierarchy_selected_rb.isChecked(): self.hierarchy = "selectedOnly"
            if self.export_hierarchy_below_rb.isChecked(): self.hierarchy = "childrenToo"

            options = "precision=8;statics={statics};baked={baked};sdk={sdk};constraint={constraint};animLayers={animLayers};selected={selected};whichRange=1;range=1:10;hierarchy=none;controlPoints={controlPoints};useChannelBox=1;options=keys;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints {controlPoints}".format(statics=self.staticValues,baked=self.bakedAnimation,sdk=self.setDrivenKeys,constraint=self.constraints,animLayers=self.animationLayers,controlPoints=self.controlPoints,selected=self.hierarchy)
            try:
                mc.file(atomFilePath, force=True, type="atomExport", exportSelected=True, options=options)
            except:
                mc.warning("Something went wrong.")
        if mode == "atomImport":
            # Get Checkbox and RadioButton state
            if self.import_hierarchy_selected_rb.isChecked(): self.hierarchy = "selectedOnly"
            if self.import_hierarchy_below_rb.isChecked(): self.hierarchy = "childrenToo"
            options = ";;targetTime=3;option=scaleReplace;match=hierarchy;;selected={0};search=;replace=;prefix=;suffix=;".format(self.hierarchy)
            try:
                mc.file(atomFilePath, i=True, type="atomImport", ra=True, namespace="atom", options=options)
            except:
                mc.warning("Something went wrong.")

        self.saveSettings()


if __name__ == "__main__":
    try:
        qa.close()
        qa.deleteLater()
    except:
        pass
    qa = QuickAtom()
    qa.show()
