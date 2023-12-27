from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "Readme.md").read_text()
setup(
    name="DashBoardUtils-DataScience",
    version="1.01",
    author="Rajat Mishra",
    author_email="rajatsmishra@aol.com",
    description="AutoMated visualization Features Extraction For Data Scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pandas"],
)
