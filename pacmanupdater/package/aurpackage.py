import subprocess
import re
from ..package import package
from ..helpers import git


class AURPackage(package.Package):

    def __init__(self, **kwargs):
        package.Package.__init__(self, **kwargs)
        self._localFolder = kwargs['localfolder']
        self._pacmanBuildOptions = kwargs['pacmanbuildoptions'] if 'pacmanbuildoptions' in kwargs else []
        self._pacmanInstallOptions = kwargs['pacmaninstalloptions'] if 'pacmaninstalloptions' in kwargs else []

    def _isAvailable(self):
        return git.repoExists(self._source)

    def _checkVersion(self):
        """ The version check downloads the remote repo, assuming an aur repo is always small """
        repo = git.Repo(self._source, self._localFolder)
        repo.get()
        for line in repo.runInRepoGetOutput(args=['cat', 'PKGBUILD'], stdout=subprocess.PIPE).decode().split('\n'):
            if re.match('^pkgver', line):
                self._version = line.split('=')[1]
        repo.clean()

    def _buildCallback(self, proc):
        while proc.poll() == None:
            print(proc.stdout.readline().decode().strip())

    def _installCallback(self, proc):
        while proc.poll() == None:
            print(proc.stdout.readline().decode().strip())

    def applyPackage(self):
        repo = git.Repo(self._source, self._localFolder)
        repo.get()
        repo.popenInRepo(self._buildCallback, args=['makepkg', '-sr', '--noconfirm'] + self._pacmanBuildOptions, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        repo.popenInRepo(self._installCallback, args=['makepkg', '-i', '--noconfirm'] + self._pacmanInstallOptions, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        repo.clean()

