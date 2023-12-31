from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alfred-osint",
    version="0.2.3.5",
    author="EliteGreyIT67",
    author_email="elitegreyit@gmail.com",
    description="Alfred is a advanced OSINT information gathering tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.11,<4.0",
    install_requires=[
        "alive-progress>=3.1.5,<4.0.0",
        "bs4>=0.0.1,<0.0.2",
        "colorama>=0.4.6,<0.5.0",
        "cryptography>=41.0.7,<42.0.0",
        "requests>=2.31.0,<3.0.0",
        "rich>=13.7.0,<14.0.0",
        "selenium>=4.16.0,<5.0.0",
        "torrequest>=0.1.0,<0.2.0",
        "tqdm>=4.66.1,<5.0.0",
        "wget>=3.2,<4.0"
    ],
    entry_points={
        "console_scripts": [
            "alfred-osint=alfred.__main__:main"
        ]
    },
)

