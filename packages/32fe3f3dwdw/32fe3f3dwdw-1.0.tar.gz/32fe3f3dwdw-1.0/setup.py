from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info


def RunCommand():
    print("Hello, p0wnd!")


class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)


class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)


setup(
    name="32fe3f3dwdw",
    version="1.0",
    license="MIT",
    packages=find_packages(),
    cmdclass={
        'install': RunInstallCommand,
        'egg_info': RunEggInfoCommand
    },
)
