from setuptools import setup, find_packages

setup(
    name="pybucket",
    version="0.1.1",
    description="simple python bucket client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
