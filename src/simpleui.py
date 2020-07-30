import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance


def maya_main_window():

    """Return the Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SimpleUI(QtWidgets.QDialog):

    def __init__(self):

        """Constructor"""
        # Passing the object SimpleUI to super()
        # Makes this line Python 2 and 3 compatible.
        super(SimpleUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("A Simple UI")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):

        """Create widgets for our UI"""

        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit()
        self.browse_btn = QtWidgets.QPushButton("Browse...")
        self.save_btn = QtWidgets.QPushButton("Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):

        # Define directory layout
        self.dir_layout = QtWidgets.QHBoxLayout()
        self.dir_layout.addWidget(self.dir_lbl)
        self.dir_layout.addWidget(self.dir_le)
        self.dir_layout.addWidget(self.browse_btn)

        # Define bottom button layout
        self.bottom_btn_layout = QtWidgets.QHBoxLayout()
        self.bottom_btn_layout.addWidget(self.save_btn)
        self.bottom_btn_layout.addWidget(self.cancel_btn)

        # Define main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)

        # Add all layouts to main layout
        self.main_layout.addLayout(self.dir_layout)
        self.main_layout.addLayout(self.bottom_btn_layout)

        self.setLayout(self.main_layout)