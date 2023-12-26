from setuptools import setup, find_packages

setup(
    name='finch-genetics',  # PyPI package name
    version='3.0.6',
    packages=find_packages(),  # Import name as a subpackage
    install_requires=[
        "torch",
        "transformers",
        "diffusers",
        "numpy",
        "matplotlib",
        "typing_extensions",
        "accelerate"
    ],
)
