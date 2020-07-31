import maya.OpenMayaUI as omui
import maya.cmds as cmds

import os

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import mayautils


def maya_main_window():

    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):

    def __init__(self):

        """Constructor"""

        # Passing the object SimpleUI to super()
        # Makes this line Python 2 and 3 compatible.
        super(SmartSaveUI, self).__init__(parent=maya_main_window())

        #Manage scene file
        self.scene = mayautils.SceneFile()

        self.setWindowTitle("Smart Save")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        self.update_scenefile_from_file()

        """Create widgets for our UI"""

        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit()
        self.dir_le.setText(self.scene.dir)

        self.browse_btn = QtWidgets.QPushButton("Browse...")

        self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_le = QtWidgets.QLineEdit("main")
        self.descriptor_le.setText(self.scene.descriptor)

        self.version_lbl = QtWidgets.QLabel("Version")
        self.version_sb = QtWidgets.QSpinBox()
        self.version_sb.setValue(self.scene.version)

        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_le = QtWidgets.QLineEdit("ma")
        self.ext_le.setText(self.scene.ext)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.inc_save_btn = QtWidgets.QPushButton("Increment and Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):

        # Define directory layout and add appropriate widgets.
        self.dir_layout = QtWidgets.QHBoxLayout()
        self.dir_layout.addWidget(self.dir_lbl)
        self.dir_layout.addWidget(self.dir_le)
        self.dir_layout.addWidget(self.browse_btn)

        # Define descriptor layout and add appropriate widgets.
        self.descriptor_layout = QtWidgets.QHBoxLayout()
        self.descriptor_layout.addWidget(self.descriptor_lbl)
        self.descriptor_layout.addWidget(self.descriptor_le)

        # Define version layout and add appropriate widgets.
        self.version_layout = QtWidgets.QHBoxLayout()
        self.version_layout.addWidget(self.version_lbl)
        self.version_layout.addWidget(self.version_sb)

        # Define extension layout and add appropriate widgets.
        self.ext_layout = QtWidgets.QHBoxLayout()
        self.ext_layout.addWidget(self.ext_lbl)
        self.ext_layout.addWidget(self.ext_le)

        # Define bottom button layout and add appropriate widgets.
        self.bottom_btn_layout = QtWidgets.QHBoxLayout()
        self.bottom_btn_layout.addWidget(self.inc_save_btn)
        self.bottom_btn_layout.addWidget(self.save_btn)
        self.bottom_btn_layout.addWidget(self.cancel_btn)

        # Define main layout and add appropriate widgets.
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)

        # Add all layouts to main layout.
        self.main_layout.addLayout(self.dir_layout)
        self.main_layout.addLayout(self.descriptor_layout)
        self.main_layout.addLayout(self.version_layout)
        self.main_layout.addLayout(self.ext_layout)
        self.main_layout.addLayout(self.bottom_btn_layout)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def create_connections(self):

        """Connects to widget signals to slots"""

        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)
        self.inc_save_btn.clicked.connect(self.increment_save)

    def update_scenefile_from_file(self):

        """Updates scene object data from current scene data"""

        # Retrieve file
        _file = cmds.file(q=True, sn=True)

        # Get the file's directory (not including the file name)
        _filepath = os.path.dirname(_file)

        # Get the file's name
        _filename = os.path.basename(_file)

        # Get the file's extension (including the period)
        _fileext = os.path.splitext(_filename)

        # If the file has been saved
        if _fileext[1] != '':

            # Take the extension out of the file name
            _filename = _filename.replace(_fileext[1], '')

            # Reassign file extension (without the file name before the extension)
            _fileext = _fileext[1]

            # Take the period out of the extension for the UI field
            _fileext = _fileext.replace('.', '')

            # Separate the file name's descriptor and version
            _segments = _filename.split('_')

            # Only repopulate scene attributes if the filename has a descriptor AND version
            if isinstance(_segments, list) and len(_segments) > 1:
                # Pass the directory, descriptor, version, and extension to scene object
                self.scene.set_dir(_filepath)
                self.scene.set_descriptor(_segments[0])
                self.scene.set_version(int(_segments[1].lstrip('0')))
                self.scene.set_ext(_fileext)

    def _populate_scenefile_properties(self):

        """Populates the scene file's object properties from the UI"""

        self.scene.dir = self.dir_le.text()
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.version = self.version_sb.value()
        self.scene.ext = self.ext_le.text()

    @QtCore.Slot()
    def save(self):

        """Saves the scene file"""

        self._populate_scenefile_properties()

        if (self.scene.dir != ''):
            self.scene.save()

    @QtCore.Slot()
    def increment_save(self):

        """Automatically finds the next available version on disk and saves up"""

        self._populate_scenefile_properties()

        if (self.scene.dir != ''):
            self.scene.increment_save()

    @QtCore.Slot()
    def cancel(self):

        """Quits the dialog"""

        self.close()