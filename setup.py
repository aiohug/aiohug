from __future__ import unicode_literals
from setuptools import setup, find_packages
import os

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_INI = os.path.join(PROJECT_DIR, "project.ini")

config = ConfigParser()
config.read(PROJECT_INI)


def get_config(opt):
    return config.get("project", opt)


NAME = get_config("name")
DESCRIPTION = get_config("description")
URL = get_config("url")
AUTHOR = "nonamenix"
AUTHOR_EMAIL = "nonamenix@gmail.com"
README = "README.rst"
README_TXT = "README.txt"
LONG_DESCRIPTION = open(os.path.join(PROJECT_DIR, README)).read()

REQUIREMENTS_FILE = "requirements.txt"
REQUIREMENTS = open(os.path.join(PROJECT_DIR, REQUIREMENTS_FILE)).readlines()

VERSION = get_config("version")
DEV_VERSION = os.environ.get("DEV_VERSION")
if DEV_VERSION:
    VERSION = "{}.dev{}".format(VERSION, DEV_VERSION)
    config.set("project", "version", VERSION)
    with open(PROJECT_INI, "w") as f:
        config.write(f)

# create a README.txt file from .md
with open(README_TXT, "wb") as f:
    f.write(LONG_DESCRIPTION.encode())

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    include_package_data=True,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    keywords=[
        "aiohttp",
        "aiohttp-server",
        "aiohttp-swagger",
        "hug",
        "api",
        "api-rest",
        "rest",
        "swagger",
        "schema",
    ],
    project_urls={
        "Changelog": "https://github.com/nonamenix/aiohug/blob/master/changelog.md",
        "Issues": "https://github.com/nonamenix/aiohug/issues",
    },
)

# delete README.txt
os.remove(README_TXT)
