from setuptools import find_packages, setup
import pathlib

with open("README.md", "r") as fh:
    long_description = fh.read()


with open(str(pathlib.Path(__file__).parent.absolute()) + "/fib_py/version.py", "r") as fh:
    version = fh.read().split("=")[1].replace("'", "")

setup(
    name="denilson_fib_py",
    version=version,
    author="Denilson",
    author_email="denilson020898@gmail.com",
    description="Recursive fibonacci",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/denilson020898/test-fib-py",
    install_requires=[
        "PyYAML>=4.1.2",
        "dill>=0.2.8",
    ],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    tests_require=["pytest"],
    entry_points={
        'console_scripts': [
            'fib-number = fib_py.cmd.fib_numb:fib_numb',
        ],
    },
    extras_require={
        "server": ["Flask>1.0.0"]
    }
)
