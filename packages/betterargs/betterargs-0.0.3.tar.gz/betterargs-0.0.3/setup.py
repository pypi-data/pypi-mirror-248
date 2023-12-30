"""Setup PIP package"""


from codecs import open as codecs_open
from pathlib import Path
from setuptools import setup, find_packages


BASE_PATH = Path(__file__).parent


with codecs_open((BASE_PATH / "README.md"), encoding="utf-8") as readme_file:
    readme_content = "\n" + readme_file.read()


AUTHOR = "DanielMuringe"
LICENSE = "MIT"
DESCRIPTION = "A tool to create a command-line interface for your app using python"
LONG_DESCRIPTION = readme_content
REQUIREMENTS = [
    "pyyaml",
]
VERSION = "0.0.3"


# Setting up
setup(
    name="betterargs",
    version=VERSION,
    author=AUTHOR,
    author_email="<danielmuringe@gmail.com>",
    license=LICENSE,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    requires=REQUIREMENTS,
    keywords=[
        "argument parser",
        "boilerplate",
        "yaml",
        "command-line",
        "command-line-tool",
        "argparse",
        "build tools",
        "args",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    python_requires=">=3.10",
    project_urls={
        "Source": "https://www.github.com/danielmuringe/betterargs",
        "Tracker": "https://www.github.com/danielmuringe/betterargs/issues",
    },
)
