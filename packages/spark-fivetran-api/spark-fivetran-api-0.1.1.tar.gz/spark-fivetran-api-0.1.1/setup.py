import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spark-fivetran-api',
    version="0.1.1",
    author="Larry Page",
    author_email="tech@spark.do",
    description="A Python wrapper for the Fivetran API developed by the Spark Tech team ⭐️",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Spark-Data-Team/spark-fivetran-api",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "datetime"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)