import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indiatools",
    version="0.1.0",
    author="Nikhil Swami",
    author_email="nikhil@swaimx.com",
    description="A Python package generated Swamix SoftEngine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikhil-Software-Cartel/IndiaTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
