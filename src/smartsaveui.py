import maya.OpenMayaUI as omui
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
        self.setWindowTitle("A Simple UI")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        """Create widgets for our UI"""

        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")

        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit()

        self.browse_btn = QtWidgets.QPushButton("Browse...")

        self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_le = QtWidgets.QLineEdit("main")

        self.version_lbl = QtWidgets.QLabel("Version")
        self.version_sb = QtWidgets.QSpinBox()
        self.version_sb.setValue(1)

        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_le = QtWidgets.QLineEdit("ma")

        self.save_btn = QtWidgets.QPushButton("Save")
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

        self.cancel_btn.clicked.connect(self.cancel)

    @QtCore.Slot()
    def cancel(self):

        """Quits the dialog"""

        self.close()