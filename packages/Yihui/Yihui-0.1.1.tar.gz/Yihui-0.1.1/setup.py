from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.1'

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='Yihui',  # package name
    version=VERSION,  # package version
    author='encyc',
    author_email='atomyuangao@gmail.com',
    description='Package for Logistic Regression Modeling',  # package description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/encyc/yihui',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)