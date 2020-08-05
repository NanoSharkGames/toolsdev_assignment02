import logging

import os

import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


class SceneFile(object):

    """Class used to to represent a Digital Content Creation software scene file

    The SceneFile class will be a convenient object that can be used to manipulate
    scene files inside of Maya. Examples features include the ability to predefine
    naming conventions and automatically increment our versions.

    Attributes:
        dir (Path, optional): Directory to the scene file. Defaults to ''.
        descriptor (str, optional): Short descriptor of the scene file. 
            Defaults to "main".
        version (int, optional): Version number. Defaults to 1.
        ext (str, optional): Extension. Defaults to "ma"

    """

    def __init__(self, dir='', descriptor='main', version=1, ext='ma'):

        """Initialises attributes when class is instantiated."""

        self.dir = dir
        self.descriptor = descriptor
        self.version = version
        self.ext = ext

    def get_dir(self):
        return self.dir

    def set_dir(self, val):
        self.dir = val

    def get_descriptor(self):
        return self.descriptor

    def set_descriptor(self, val):
        self.descriptor = val

    def get_version(self):
        return self.version

    def set_version(self, val):
        self.version = val

    def get_ext(self):
        return self.ext

    def set_ext(self, val):
        self.ext = val

    def basename(self):

        """Return a scene file name.

        e.g. ship_001.ma, car_011.hip

        Returns:
            str: The name of the scene file.

        """

        namepattern = "{descriptor}_{version:03d}.{ext}"
        name = namepattern.format(descriptor=self.descriptor, version=self.version, ext=self.ext)

        return name

    def path(self):

        """The function returns a path to scene file.

        This includes the drive letter, any directory path and the file name.

        Returns:
            Path: The path to the scene file.

        """

        return Path(self.dir) / self.basename()

    def save(self):

        """Saves the scene file.

        Returns:
            Path: The path to the scene file if successful, None, otherwise.

        """

        try:
            pmc.system.saveAs(self.path())
        except RuntimeError:
            log.warning("Missing directories. Creating directories now.")
            self.dir.makedirs_p()
            pmc.system.saveAs(self.path())

    def increment_save(self):

        """Increments the version and saves the scene file.

        If existing versions of a file already exist, it should increment 
        from the largest number available in the folder.

        Returns:
            Path: The path to the scene file if successful, None, otherwise.
        """

        _highestVersion = 0

        dirs = os.listdir(self.dir)

        for filename in dirs:

            if filename.startswith(self.descriptor) and filename.endswith(self.ext):

                # Take the extension out of the filename.
                filename = filename.replace('.' + self.ext, '')

                # Separate the file name's descriptor and version
                _segments = filename.split('_')

                # Only repopulate scene attributes if the filename has a descriptor AND version
                if isinstance(_segments, list) and len(_segments) > 1:

                    _versionTxt = _segments[1].lstrip('0')

                    # Retrieve the file name's version.
                    _version = int(_versionTxt)

                    if (_version > _highestVersion):
                        _highestVersion = _version

        if _highestVersion > 0:
            self.set_version(_highestVersion + 1)
            self.save()