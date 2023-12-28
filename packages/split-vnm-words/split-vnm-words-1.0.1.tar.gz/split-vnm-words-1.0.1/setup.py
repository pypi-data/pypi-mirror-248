from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="split-vnm-words",
    version="1.0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "splitwords.dicts": ["dicts/*.txt"],
    },
    install_requires=[
        "numpy",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)