import subprocess
import re


class Package:
    """
    Abstract package from any source.
    """

    def __init__(self, **kwargs):
        """ Constructor... """
        self._name = kwargs['name']
        self._source = kwargs['source']

    def check(self):
        if not self._isAvailable():
            return False
        self._checkVersion()
        return self._checkUpdateNeeded()

    def _checkVersion(self):
        raise NotImplementedError("Please Implement this method")

    def _isAvailable(self):
        raise NotImplementedError("Please Implement this method")

    def applyPackage(self):
        raise NotImplementedError("Please Implement this method")

    def _checkUpdateNeeded(self):
        """
        Returns False if the package version or newer
        is already installed, False otherwise.
        """
        try:
            currentVersionLine = str(subprocess.run(['pacman', '-Q', '-i', self._name],
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout)
            currentVersion = re.sub(r'.*Version\s*: ([\d|\.]*)-.*', r'\1', currentVersionLine).split('.')
            newVersion = self._version.split('.')
            for i in range(0, min(len(currentVersion), len(newVersion))):
                if currentVersion[i].isdigit():
                    # TODO: test if new version is only digits too, two of them should be the same anyway
                    if int(newVersion[i]) > int(currentVersion[i]):
                        return True
                    if int(newVersion[i]) < int(currentVersion[i]):
                        return False
            return len(newVersion) > len(currentVersion)
        except subprocess.CalledProcessError:
            # Package not found: to be installed then
            return True

