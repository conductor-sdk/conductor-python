from setuptools import find_packages
from distutils.core import setup
import os
import pathlib

VERSION = os.environ['CONDUCTOR_PYTHON_VERSION']

here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name='conductor-python',
    version=VERSION,
    description='Netflix Conductor Python SDK',
    long_description='file: README.md',
    long_description_content_type='text/markdown',
    url='https://github.com/conductor-sdk/conductor-python',
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "certifi >= 14.05.14",
        "six >= 1.10",
        "urllib3 >= 1.15.1",
        "prometheus-client >= 0.13.1",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Development Status :: 4 - Beta",
    ],
    author='Gustavo Gardusi',
    author_email='gustavo.gardusi@gmail.com',
)
