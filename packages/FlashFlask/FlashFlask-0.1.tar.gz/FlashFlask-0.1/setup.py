from setuptools import setup, find_packages

setup(
    name="FlashFlask",
    version="0.1",
    packages=find_packages(),
    package_data={
        "FlashFlask": ["data.zip", "licenses/*.txt"],
    },
    entry_points={
        "console_scripts": [
            "flash = FlashFlask.main:main",
        ],
    },
)
