from setuptools import setup, find_packages
from setuptools.command.install import install
import os








setup(
    name='SegmentCar',
    version='0.0.1',
    package_data={'carbgremover': ['pretrained_models/*', 'images/*']},
    packages=find_packages(),
    install_requires=['numpy', 'tensorflow', 'ultralytics', 'segment_anything','tqdm','requests'],
    readme ="carbgremover/images/README.md",
    long_description_content_type='text/markdown',
)
