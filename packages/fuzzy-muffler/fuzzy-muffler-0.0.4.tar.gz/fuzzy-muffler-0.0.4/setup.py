from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

# need to install rubberband-cli via apt
class custom_cmd(install):
    def run(self):
        subprocess.check_call(['sudo', 'apt', 'install', '-y', 'rubberband-cli'])
        install.run(self)
    
with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fuzzy-muffler",
    version="0.0.4",
    author="hashirkz",
    author_email="hashir.khan@mail.mcgill.ca",
    description="mp3|ogg|wav audio muffler/fuzifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hashirkz/muffle_audio",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'muffle = __muffle__.app:app',
        ],
    },
    install_requires=[
        'numpy==1.23.0',
        'matplotlib==3.3.0',
        'pandas==2.0.2',
        'scipy==1.5.2',
        'librosa==0.10.1',
        'pyrubberband==0.3.0',
        'pyyaml==5.4.1'
    ],
    cmdclass= {
        'install': custom_cmd,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
    ],
)
