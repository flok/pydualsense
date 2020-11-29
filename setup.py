from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pydualsense',
    version='0.2.0',
    description='use your DualSense (PS5) controller with python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/flok/pydualsense',
    author='Florian K',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['hid>=1.0.4']
)
