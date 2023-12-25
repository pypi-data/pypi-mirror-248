import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="btframework",
    version="1.0.1",
    author="Piyush Patil",
    author_email="patilpiyush210@gmail.com",
    description="A simple backtesting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "pandas", "psycopg2-binary", "pytz", "ta", "openpyxl"],
)
