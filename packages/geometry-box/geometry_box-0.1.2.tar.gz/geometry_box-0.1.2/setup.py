from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='geometry_box',
    version='0.1.2',
    author='Rajesh Nakka',
    author_email='33rajesh@gmail.com',
    description='A simple package for working with basic geometry shapes',
    long_description=readme,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
