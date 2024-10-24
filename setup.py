from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas"
    ],
    author="Noah Stoffman",
    author_email="nstoffma@iu.edu",
    description="A small package that creates a mapping from SIC codes to Fama-French industries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stoffprof/ff_industries",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",         # Python version requirement
)
