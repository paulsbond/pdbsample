import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="pdbsample",
    version="0.0.1",
    author="Paul Bond",
    author_email="paul.bond@york.ac.uk",
    description="Program to get a sample of PDB entries",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/paulsbond/pdbsample",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="LGPL-2.1",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    install_requires=["requests", "solrq"],
    entry_points={"console_scripts": ["pdbsample = pdbsample.__main__:main"]},
)
