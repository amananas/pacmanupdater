from .package import aurpackage
from .helpers import logger

_PACKAGE_TYPES = {
    'aur': aurpackage.AURPackage
}
_configuration = None


def configure(config, includes=None, excludes=None, configDebug=False):
    """
    includes set: use only the matching entries in the config list, ignore others
    excludes set: use all the entries in the config, exclude the matching ones. This is default behavior.
    """
    global _configuration
    logger.configLogging(configDebug)
    if includes and excludes:
        raise Exception('You cannot include and exclude packages here, it means nothing.');
    if includes:
        _configuration = {}
        for packageName in includes:
            _configuration[packageName] = config[packageName]
    else:
        _configuration = config
        for packageName in excludes:
            del _configuration[packageName]


def run():
    packages = []
    for packageName, package in _configuration.items():
        if package['packagetype'] not in _PACKAGE_TYPES:
            raise Exception('This package type is not available yet.')
        pak = _PACKAGE_TYPES[package['packagetype']](name=packageName, **package)
        if pak.check():
            packages.append(pak)

    for pak in packages:
        pak.applyPackage()
