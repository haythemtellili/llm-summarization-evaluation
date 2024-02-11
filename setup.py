from setuptools import find_packages, setup

setup(
    name="summarization",
    py_modules=["src"],
    version="0.0.1",
    author="Haythem Tellili",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)