from setuptools import setup, find_packages
import os.path

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name='Eir',
    version='0.1.20',
    license='MIT',
    description="Helps model epidemics using spatial models",
    long_description=README,
    long_description_content_type="text/markdown",
    url = "https://github.com/mjacob1002/Eir",
    download_url="https://github.com/mjacob1002/Eir/archive/refs/tags/v_001.tar.gz",
    author="Mathew Jacob",
    author_email="mjacob1002@gmail.com",
    keywords=['epidemics', 'super spreader'],
    install_requires=[
        "numpy", 
        "pandas", 
        "matplotlib", 
        "multipledispatch"
        ],
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ]
)
