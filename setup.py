from setuptools import setup

def readme():
    with open("Readme.md") as f:
        return f.read()

setup(
    name="pwd_manager",
    version="0.0.1",
    description="Command line password manager",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Philipp Wolf",
    author_email="ph.wolf89@gmail.com",
    license="MIT",
    packages=["pwd_manager"],
    install_requires=[
        "cryptography",
        "pyperclip"
    ],
    entry_points={
        "console_scripts": ["pwd-man=pwd_manager.command_line:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)