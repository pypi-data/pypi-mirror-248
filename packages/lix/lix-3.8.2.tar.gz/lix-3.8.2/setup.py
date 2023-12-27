from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="lix",
    version="3.8.2",
    description="lix - Multi purpose package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/flowa-ai/lix",
    author="flowa",
    author_email="flowa.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "Development Status :: 3 - Alpha",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Typing :: Typed",
    ],
    keywords="lix math random copy cache factorial fib fibonacci sqrt sort sorting color colorama",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
        'numpy',
    ],
    python_requires=">=3.6",
)