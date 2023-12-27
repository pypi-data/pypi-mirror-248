from setuptools import setup, find_packages

setup(
    name="pythopix",
    version="0.0.8",
    author="Boris",
    author_email="borisculjak@example.com",
    packages=find_packages(),
    install_requires=[
        "torch",
        "tqdm",
        "ultralytics",
    ],
    description="An image dataset evaluation library using YOLO models",
)
