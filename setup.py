import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pikli",
    version="0.0.1",
    author="Ahmad Anondo",
    author_email="aanondos@gmail.com",
    description="A package to create cli apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anondo/pikli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
)
