from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'CShark custom kafka library for python project'

setup(
    name="cshark_kafka",
    version=VERSION,
    author="CShark team (Yelnur)",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['kafka-python'],
)