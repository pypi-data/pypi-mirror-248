from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.5'

setup(
    name="easier_sockets",
    version=VERSION,
    author="OverclockedD2",
    author_email="<overclockedd2@gmail.com>",
    long_description_content_type="text/markdown",
    long_description="+-------------------------------------------------------------------------------------------------+\n| The documentation has been moved to `GitHub <https://github.com/overclockedd2/easier_sockets>`_ |\n+-------------------------------------------------------------------------------------------------+\n",
    packages=find_packages(),
    install_requires=['rsa'],
    keywords=['python', 'sockets', 'encrypted', 'rsa', 'easy', 'simple'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
