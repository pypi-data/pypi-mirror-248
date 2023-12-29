import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tilelink",
    version="2023.12.28",
    author="-T.K.-",
    author_email="t_k_233@outlook.email",
    description="Utility for talking with DUT via TileLink protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ucb-bar/TileLink-Python",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyserial",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
