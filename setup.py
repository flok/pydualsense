from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pydualsense',
    version='0.6.2',
    description='use your DualSense (PS5) controller with python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/flok/pydualsense',
    author='Florian (flok) K',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['hidapi-usb>=0.3', 'cffi']
)
