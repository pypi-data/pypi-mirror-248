"""
Sample setup.py file
"""
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "Readme.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="storage-hub",
    version='0.0.8',
    author="Vitaliy Zakharkiv",
    author_email="vzaharkiv28@mail.com",
    description="soon",
    url="https://github.com/VitailOG/storage-hub",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(where='storage_hub'),
    package_dir={'': 'storage_hub'},
    install_requires=[],
    license="MIT",
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
