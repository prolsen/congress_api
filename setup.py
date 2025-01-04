from setuptools import setup

setup(
    name="congress-api",
    version="0.1.1",
    description="A package for interacting with the Congress API",
    author="Patrick Olsen",
    packages=["congress_api", "congress_api.endpoints"],
    install_requires=["python-dotenv", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)