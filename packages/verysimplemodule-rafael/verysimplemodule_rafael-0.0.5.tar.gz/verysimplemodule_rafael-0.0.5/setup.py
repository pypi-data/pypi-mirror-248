from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Pacote inicial'
LONG_DESCRIPTION = 'Pacote inicial com contas simples de matematica'

setup(
    name="verysimplemodule_rafael",
    version = VERSION,
    author = "rafael",
    author_email = "rafaell_pi@hotmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ['numpy'],
    
    keywords = ['python', 'primeiro pacote'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)