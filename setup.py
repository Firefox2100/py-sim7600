from setuptools import setup
import codecs
import os.path
from pathlib import Path


here = os.path.abspath(os.path.dirname(__file__))
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def read(rel_path: str):
    with codecs.open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")


setup(
    name='py-sim7600',
    version=get_version("py_sim7600/__init__.py"),
    packages=['py_sim7600'],
    url='https://github.com/Firefox2100/py-sim7600',
    license='LICENSE',
    author='Firefox2100',
    author_email='wangyunze16@gmail.com',
    description='A pure Python package to interface with SIM7600 modems.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
