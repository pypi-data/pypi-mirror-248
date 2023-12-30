from setuptools import setup, find_packages

setup(
    name="boxcord",
    version="0.2.5",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'boxcord = boxcord.cli:main',
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)