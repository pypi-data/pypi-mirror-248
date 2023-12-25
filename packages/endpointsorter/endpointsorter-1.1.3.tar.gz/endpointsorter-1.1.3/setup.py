from setuptools import setup, find_packages

with open("endpointsorter/requirements.txt", "r") as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="endpointsorter",
    version="1.1.3",
    author="Praveen",
    author_email="mspraveenkumar77@gmail.com",
    description="A sorter tool for endpoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": ["endpointsorter = endpointsorter.endpointsorter:main"],
    },
)
