import setuptools
import os


#store readme.md files
with open("README.md", "r") as fh:
    long_description = fh.read()
#read the requirements
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="FoundationDesign",
    version="0.0.5",
    author="Kunle Yusuf",
    author_email="kunleyusuf858@gmail.com",
    description=" A python module for structural analysis and design of different foundation type in accordance to the Eurocodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
