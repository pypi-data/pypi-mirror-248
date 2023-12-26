from setuptools import setup, find_packages
from setuptools.command.install import install
import os








setup(
    name='SegmentCar',
    version='0.0.3',
    package_data={'carbgremover': ['pretrained_models/*', 'images/*']},
    packages=find_packages(),
    install_requires=['numpy', 'tensorflow', 'ultralytics', 'segment_anything','tqdm','requests'],
    long_description=open('carbgremover/images/README.md').read(),
    long_description_content_type='text/markdown',

)
