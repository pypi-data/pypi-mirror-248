from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), "r") as f:
    long_description = '\n' + f.read()

with open(path.join(here, 'pydparser/requirements.txt'), "r") as f:
    install_requires = f.read().splitlines()

VERSION = '1.0.2'
DESCRIPTION = 'A simple resume and job description parser used for extracting information from resumes and job descriptions and compatible with python 3.10 upwords'
setup(
    name='pydparser',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/justicea83/pydparser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='justicea83',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    keywords=['python', 'resume', 'jd', 'job description', 'parser'],
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    zip_safe=False,
    python_requires='>=3.10'
)
