import setuptools
from distutils.util import convert_path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

main_ns = {}
ver_path = convert_path("speechtotext/about.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


setuptools.setup(
    name=main_ns["__title__"],
    version=main_ns["__version__"],
    author=main_ns["__author__"],
    author_email=main_ns["__email__"],
    description=main_ns["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanvanleeuwen/speech_to_text",
    project_urls={
        "Bug Tracker": "https://github.com/jonathanvanleeuwen/speech_to_text/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=["speechtotext", "speechtotext.*", "tests", "tests.*"]),
    python_requires=">=3.6",
    install_requires=[
        "argh~=0.26.2",
        "azure-cognitiveservices-speech~=1.19.0",
        "pytest~=6.2.4",
        "python-dotenv~=0.19.1",
    ],
    test_suite="tests",
    tests_require=[
        "pytest",
    ],
)
