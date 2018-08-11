import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="attach",
    version="0.1",
    author="Yatharth Agarwal",
    author_email="yatharth999@gmail.com",
    description="Attaching and detaching namespaces to keep globals clean",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yatharth/attach",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ),
)