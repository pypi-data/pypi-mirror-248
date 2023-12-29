from setuptools import setup, find_packages
from os.path import join, dirname

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='ProjectStructureManager',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
