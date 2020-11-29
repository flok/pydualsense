from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pydualsense',
    version='0.0.1',    
    description='control your dualsense controller with python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/flok/pydualsense',
    author='Florian Kaiser',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=setuptools.find_packages(),
    install_requires=['hid>=1.0.4']
)
