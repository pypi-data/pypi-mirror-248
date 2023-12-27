from setuptools import setup, find_packages
import sys

install_requires=[
        'torch == 2.1.1',
        'torchvision == 0.16.1',
        'numba == 0.57.0',
        'numpy == 1.24.3',
        'opencv-python == 4.8.0.74',
        'pandas == 2.0.1',
        'matplotlib == 3.7.1',
        'scikit-image == 0.20.0',
        'ipympl == 0.9.3',
        'PyQt5 == 5.15.9',
        'Pillow >= 7.1.2',
        'ultralytics == 8.0.120',
        'jupyterlab == 4.0.7',
        'requests == 2.31.0'
    ]

if sys.platform.startswith('win'):
    install_requires.append('--index-url https://download.pytorch.org/whl/cu121')

setup(
    name='NPSAM',
    version='1.1',
    packages=find_packages(),
    description='NP-SAM is an easy-to-use segmentation and analysis tool for nanoparticles and more.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Torben Villadsen & Rasmus Larsen',
    author_email='torben-v@hotmail.com',
    url='https://gitlab.au.dk/disorder/np-sam',
    install_requires=install_requires,
    python_requires='>=3.10',
    license='Apache License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
