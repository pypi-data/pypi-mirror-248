from setuptools import setup, find_packages

setup(
    name="maddlib",
    version="0.5.9",
    description="A Python package to compute MADD metric-related functions",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url="https://github.com/melinaverger/maddlib",
    author="Mélina Verger",
    author_email="melina.verger@lip6.fr",
    package_dir={"":"src"},
    license="CC BY-NC 4.0",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
        ],
    install_requires=["scikit-learn", "pandas", "numpy", "seaborn", "matplotlib"],
    extras_require={"dev":["twine>=4.0.2"]},
    python_requires=">=3.10.4"
)