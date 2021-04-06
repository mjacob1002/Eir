from setuptools import setup, find_packages

setup(
    name='Eir',
    version='0.0.1',
    license='MIT',
    description="Helps model epidemics using spatial models",
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
        ]
    packages=find_packages(),
)