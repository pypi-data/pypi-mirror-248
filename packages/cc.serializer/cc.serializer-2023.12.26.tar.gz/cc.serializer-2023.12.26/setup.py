import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cc.serializer",
    version="2023.12.26",
    author="Uncertainty.",
    author_email="t_k_233@outlook.email",
    description="Transmit and receive Serial data and divide the stream into packets with NLSM protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uncertainty-cc/Serializer-Python",
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
    python_requires=">=3.8",
)
