from setuptools import setup, find_packages

setup(
    name="FlashFlask",
    version="0.2",
    packages=find_packages(),
    package_data={
        "FlashFlask": ["data.zip", "licenses/*.txt"],
    },
    entry_points={
        "console_scripts": [
            "flash = FlashFlask.main:main",
        ],
    },
    install_requires=[
        "cs50==9.2.6",
        "Flask==3.0.0",
        "flask_session==0.5.0",
        "Werkzeug==3.0.1",
        "requests",
        "shutil",
    ],
)
