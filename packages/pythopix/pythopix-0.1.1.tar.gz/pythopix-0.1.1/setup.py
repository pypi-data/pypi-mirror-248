from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "pythopix", "README.md")

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pythopix",
    version="0.1.1",
    author="Boris",
    author_email="borisculjak@example.com",
    packages=find_packages(),
    install_requires=[
        "torch",
        "tqdm",
        "ultralytics",
    ],
    description="An image dataset evaluation library using YOLO models",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
