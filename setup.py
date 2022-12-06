from setuptools import setup

setup(
    name='py-sim7600',
    version='0.1.0',
    packages=['py_sim7600'],
    url='https://github.com/Firefox2100/py-sim7600',
    license='LICENSE',
    author='Firefox2100',
    author_email='wangyunze16@gmail.com',
    description='A pure Python package to interface with SIM7600 modems.',
    install_requires=[
        "pyserial",
    ]
)
