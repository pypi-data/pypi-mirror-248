from distutils.core import setup
from setuptools import find_packages
import os

setup(
    name='cvbot',
    package=find_packages(','),
    version='3.1.2',
    license='LICENSE',
    description='Computer vision toolbox for automating tasks, mainly desktop apps, games and others',
    author='Hisham Moe',
    install_requires=[
        'opencv-python',
        'numpy',
        'mss',
        'pynput',
        'pywin32',
        'easyocr',
        'thefuzz[speedup]',
        'onnx',
        'onnxruntime'
        ],
    extenstion = ['sphinx.ext.autosectionlabel',
                'sphinxcontrib.osexample']
    )
