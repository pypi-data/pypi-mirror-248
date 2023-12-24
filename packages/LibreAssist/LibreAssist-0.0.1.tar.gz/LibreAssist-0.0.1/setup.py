from setuptools import setup, find_packages

setup(
    name="LibreAssist",
    version="0.0.1",
    author="Erfan Zare Chavoshi",
    author_email="erfanzare82@eyahoo.com",
    description="An open-source library LibreAssist is a Local Assistance here to help you with your needs on your personal computer",
    url="https://github.com/erfanzar/LibreAssist",
    packages=find_packages("src/python/"),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="machine learning, deep learning, ggml, gguf, c++",
    install_requires=[
        "llama-cpp-python==0.2.25",
        "gradio==4.10.0",
        "absl-py==2.0.0",
        "diskcache~=5.6.3",
        "numpy~=1.26.1",
        "typing~=3.7.4.3",
        "pydantic_core==2.14.6",
    ],
    python_requires=">=3.8",
    package_dir={'': "src/python"},

)
