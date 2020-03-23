import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soilapis",
    version="0.0.1",
    author="Josue K",
    author_email="josuk@pm.me",
    description="Package for soil apis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eusojk/gis-scripts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)