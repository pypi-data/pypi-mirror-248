from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""

    def run(self):
        print("Hello, developer, how are you? :)")
        install.run(self)


setup(
    name="dwwdedwe22e32e",
    version="1.0",
    license="MIT",
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    },
)
