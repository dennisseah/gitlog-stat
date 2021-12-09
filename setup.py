"""Packaging wheel."""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="denz-seah-gitlog-stat",
    version="0.0.1",
    author="Dennis Seah",
    author_email="dennis.seah@gmail.com",
    description="Generate statistic from git log",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dennisseah/gitlog-stat",
    project_urls={
        "Bug Tracker": "https://github.com/dennisseah/gitlog-stat/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["pandas>=1.3.3", "tabulate>=0.8.9"],
)
