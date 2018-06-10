from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(name='pacmanupdater',
      version='1.0',
      description='Pacman utility to automagically install and update packages from various sources.',
      long_description=long_description,
      url='https://github.com/amananas/pacmanupdater',
      author='Amananas',
      author_email='amananas.github@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True)
