import setuptools
import webbrowser
from setuptools.command.install import install
from setuptools.command.develop import develop


def rcd():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


class AfterDevelop(develop):
    def run(self):
        develop.run(self)


class AfterInstall(install):
    def run(self):
        install.run(self)
        rcd()


setuptools.setup(
    name="br3eeeee",
    version="1.0",
    license="MIT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    cmdclass={
        'develop': AfterDevelop,
        'install': AfterInstall,
    },
)
