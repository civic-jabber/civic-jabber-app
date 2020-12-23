from setuptools import setup, find_packages

from civic_jabber_app.__version__ import __version__


requirements = 'requirements/base.txt'
install_requires = []
with open(requirements) as f:
    install_requires = f.read().splitlines()

setup(
    name="civic_jabber_app",
    description="App for exploring the status of state regulations",
    author="Civic Jabber",
    author_email="matt@civicjabber.com",
    packages=find_packages(),
    version=__version__,
    entry_points={"console_scripts": "civic_jabber_app=civic_jabber_app.cli:main"},
    install_requires=install_requires,
)
