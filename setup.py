from setuptools import setup, find_packages


setup(
    name="optimizer-model",
    license="BSD",
    url="https://github.com/alex/optimizer-model",
    author="Alex Gaynor",
    packages=find_packages(exclude=["tests", "tests.*"]),
)
