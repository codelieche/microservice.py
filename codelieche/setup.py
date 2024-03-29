# -*- coding:utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codelieche",
    version="0.0.1",
    author="codelieche",
    author_email="codelieche@gmail.com",
    description="Codelieche utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codelieche/microservice.py",
    project_urls={
        "Bug Tracker": "https://github.com/codelieche/microservice.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)