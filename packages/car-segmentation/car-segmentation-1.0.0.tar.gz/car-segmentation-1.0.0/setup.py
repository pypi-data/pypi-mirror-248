from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        # Add your download script here
        os.system("python download_model.py")


setup(
    name='car-segmentation',
    version='1.0.0',
    package_data={'carbgremover': ['pretrained_models/*', 'images/*']},
    packages=find_packages(),
    install_requires=['numpy', 'tensorflow', 'ultralytics', 'segment_anything','tqdm','requests'],
    readme ="README.md",
    long_description_content_type='text/markdown',
    cmdclass={'install': CustomInstallCommand},
)
