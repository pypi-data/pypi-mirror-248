from distutils.core import setup, Extension

with open("README.md", "r") as f:
    long_description = f.read()

module = Extension("recuests", sources = [
    "src/client.c",
    "src/callback.c",
    "src/hashmap.c",
    "src/wrappers.c",
    "src/module.c",
], library_dirs=["/usr/lib"], libraries = ["curl"])

setup(
    name = "recuests",
    version = "1.0",
    url="https://github.com/epsilonr/recuests",
    author="epsilonr",
    description = "Python bindings for https://github.com/epsilonr/httpclient",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    ext_modules = [module]
)