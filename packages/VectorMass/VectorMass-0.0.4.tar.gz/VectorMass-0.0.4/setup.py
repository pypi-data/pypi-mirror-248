from setuptools import setup, find_packages

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open('requirements.txt') as f:
    required_libraries = f.read().splitlines()

VERSION = '0.0.4'
DESCRIPTION = 'Highly flexible vector store'

setup(
    name="VectorMass",
    version=VERSION,
    author="Dinesh Piyasamara",
    author_email="dineshpiyasamara@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/dineshpiyasamara/VectorMass",
    license="MIT",
    packages=find_packages(),
    install_requires=required_libraries,
    extras_requires={
        "dev": ["pytest", "twine"]
    },
    keywords=['vector database', 'vector store'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)