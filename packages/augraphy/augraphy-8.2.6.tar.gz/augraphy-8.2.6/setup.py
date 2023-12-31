import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("augraphy/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split('"')[1]

setuptools.setup(
    name="augraphy",
    version=version,
    author="Sparkfish LLC",
    author_email="packages@sparkfish.com",
    description="Augmentation pipeline for rendering synthetic paper printing and scanning processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sparkfish/augraphy",
    project_urls={
        "Bug Tracker": "https://github.com/sparkfish/augraphy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "matplotlib >= 3.4.3",
        "numba >= 0.57.0",
        "numpy >= 1.20.1",
        "opencv-python >= 4.5.1.48",
        "Pillow >= 8.0.0",
        "requests >= 2.25.1",
        "scikit-image >= 0.18.1",
        "scikit-learn >= 0.23.2",
        "scipy >= 1.6.3",
    ],
)
