from setuptools import setup, find_packages
from setuptools.command.install import install
import os

def get_long_description():
    """Read long description from README"""
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name='CarSegPro',
    version='0.0.4',
    package_data={'carbgremover': ['pretrained_models/*', 'images/*']},
    url="https://github.com/NechbaMohammed/CarSegPro",
    author=['Tawfiq Adnane','Mohammed Nechba'],
    author_email='tawfiqaadnane@gmail.com',
    maintainer_email='mohammednechba@gmail.com',
    packages=find_packages(),
    install_requires=['sys','opencv-python','numpy', 'tensorflow', 'ultralytics', 'segment_anything','tqdm','requests'],
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

)
