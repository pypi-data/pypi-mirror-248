from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), "r") as fd:
    long_description = fd.read()

setup(
    name='zdeb-utils',
    version='0.2.4',
    description='Helper to upload and download files to / from Gitlab, as generic packages.',
    author_email='it-support@zilogic.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['zdeb_utils'],
    entry_points={
        'console_scripts': ['zdeb-utils = zdeb_utils.main:main'],
    },
    install_requires=['python-gitlab', 'packaging']
)
