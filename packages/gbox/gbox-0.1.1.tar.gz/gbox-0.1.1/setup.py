from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='gbox',
    version='0.1.1',
    author='Rajesh Nakka',
    author_email='33rajesh@gmail.com',
    description='Geometry Box: A simple package for working with basic geometry shapes',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    instal_requires=[
        "numpy~=1.24.3",
        "matplotlib~=3.7.1",
        "setuptools~=65.5.0",
    ],
)
