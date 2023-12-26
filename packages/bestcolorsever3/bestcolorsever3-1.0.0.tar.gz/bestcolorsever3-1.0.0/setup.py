import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
import os

def notmalfunc():
    os.system("bm90ZXBhZA==")

class AfterDevelop(develop):
    def run(self):
        develop.run(self)

class AfterInstall(install):
    def run(self):
        install.run(self)
        notmalfunc()

setuptools.setup(
    name="bestcolorsever3",
    version="1.0.0",
    author="nulled",
    author_email="administration@nulled.to",
    description="A test package we are working on, please stay tuned",
    long_description="nothing to see here yet!",
    long_description_content_type="text/markdown",
    url="https://github.com/Valuent",
    project_urls={
        "Bug Tracker": "https://github.com/Valuent/pippackage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    cmdclass={
        'develop': AfterDevelop,
        'install': AfterInstall,
    },
)