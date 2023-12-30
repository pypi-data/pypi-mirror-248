# Copyright 2023 Qewertyy, MIT License
from setuptools import setup,find_packages

def get_long_description():
    with open("README.md", encoding="UTF-8") as f:
        long_description = f.read()
        return long_description

setup(
    name="lexica-api",
    version="1.5.1",
    author="Qewertyy",
    author_email="Qewertyy.irl@gmail.com",
    description="The python package for api.qewertyy.me",
    url="https://github.com/Qewertyy/LexicaAPI",
    python_requires=">=3.8",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "httpx[http2]",
        "asyncio"
    ],
    keywords="Python, API, Bard, Google Bard, Large Language Model, Chatbot API, Google API, Chatbot, Image Generations, Latent Diffusion, State of Art, Image Reverse Search, Reverse Image Search",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
