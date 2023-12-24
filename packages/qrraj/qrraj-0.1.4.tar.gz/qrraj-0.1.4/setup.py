from setuptools import find_packages, setup

setup(
    name='qrraj',
    version='0.1.4',
    author='Aryan Raj',
    description='QR CODE GENERATOR!!',
    install_requires = ["wheel", "setuptools", "setuptools", "qrcode" ],
    packages=find_packages(),
)