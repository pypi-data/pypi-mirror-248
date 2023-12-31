from setuptools import setup, find_packages


setup(
    name="anipie", 
    version='0.0.7',
    author="Aritsu",
    author_email="lynniswaifu@gmail.com",
    description="a simple python wrapper for the Anilist API",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['requests'],
    python_requires='>=3.6',
)