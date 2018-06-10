import subprocess
import os
import shutil


def repoExists(address):
    return subprocess.run(['git', 'ls-remote', '--exit-code', address]).returncode == 0


class Repo:

    def __init__(self, address, localFolder, ref='master'):
        self._remote = address
        self._local = localFolder
        self._ref = ref

    def get(self):
        previousLocation = os.getcwd()
        try:
            os.makedirs(self._local, exist_ok=False)
        except OSError:
            # Todo: print a warning here, or ask the user if he's sure he wants to delete any existing directory
            shutil.rmtree(self._local)
            os.makedirs(self._local, exist_ok=False)
        os.chdir(self._local)
        subprocess.run(['git', 'init']).check_returncode()
        subprocess.run(['git', 'remote', 'add', 'origin', self._remote]).check_returncode()
        subprocess.run(['git', 'fetch', '--depth=1', 'origin', self._ref]).check_returncode()
        subprocess.run(['git', 'checkout', self._ref]).check_returncode()
        os.chdir(previousLocation)

    def clean(self):
        shutil.rmtree(self._local)

    def runInRepo(self, *args, **kwargs):
        previousLocation = os.getcwd()
        os.chdir(self._local)
        subprocess.run(*args, **kwargs).check_returncode()
        os.chdir(previousLocation)

    def runInRepoGetOutput(self, *args, **kwargs):
        previousLocation = os.getcwd()
        os.chdir(self._local)
        result = subprocess.run(*args, **kwargs).stdout
        os.chdir(previousLocation)
        return result

    def popenInRepo(self, functionCalled, *args, **kwargs):
        """ functionCalled should be a function taking the subprocess.Popen result as lone argument, and will be called when the subprocess.Popen is started """
        previousLocation = os.getcwd()
        os.chdir(self._local)
        with subprocess.Popen(*args, **kwargs) as proc:
            functionCalled(proc)
        os.chdir(previousLocation)

