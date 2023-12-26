from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="lix",
    version="0.0.0",
    description="...",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.google.com",
    author="...",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
)