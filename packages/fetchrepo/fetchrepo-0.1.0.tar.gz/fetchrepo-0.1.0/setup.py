from setuptools import setup,find_packages

setup(
    name="fetchrepo",
    version="0.1.0",
    packages=find_packages(),
    author="Al-Fareed",
    description="Passing your GitHub https url, It fetches your content from GitHub repo",
    long_description=open("README.md").read(),
    long_description_content_type = "text/markdown"
    )