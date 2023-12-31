from setuptools import setup,find_packages

setup(
    name="fetchrepo",
    version="2.0",
    packages=find_packages(),
    author="Al-Fareed",
    description="fetches the content from github repository",
    long_description=open("README.md").read(),
    long_description_content_type = "text/markdown"
    )