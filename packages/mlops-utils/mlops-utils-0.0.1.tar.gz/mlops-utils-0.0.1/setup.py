import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlops-utils",
    version="0.0.1",
    author="robert-min",
    author_email="robertmin522@gmail.com",
    description="mlops utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FLYAI4/mlops-utils",
    packages=setuptools.find_packages(),
    install_requires=[
        "matplotlib==3.8.2",
        "mlflow==2.9.2",
        "numpy==1.26.2",
        "scikit-learn==1.3.2",
        "scipy==1.11.4",
        "torch==2.1.2"
        ],
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.10',
)