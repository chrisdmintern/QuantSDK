import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quant-sdk-lite-sblago",
    version="1.0.0",
    author="Setor Blagogee, Chris Mintern",
    author_email="sb@blocksize-capital.com",
    description="A python wrapper for Blocksize Capitals Core Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Blocksize-Capital-GmbH/QuantSDK.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
