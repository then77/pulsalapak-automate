import os
from setuptools import setup, find_packages

def readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8').read()

setup(
    name = "pulsalapak_automate",
    version = "0.1.0",
    author = "Realzzy",
    author_email = "hello@therealzzy.xyz",
    description = ("An educational purpose to automate pulsalapak."),
    license = "MIT",
    keywords = "pulsalapak automate automation",
    url = "https://github.com/then77/pulsalapak-automate",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    long_description=readme(),
    install_requires=["requests", "beautifulsoup4"]
)
