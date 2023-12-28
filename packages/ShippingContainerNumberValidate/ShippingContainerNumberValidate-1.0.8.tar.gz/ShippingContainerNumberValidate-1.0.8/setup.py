from setuptools import setup, find_packages
classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
]

setup(
    name="ShippingContainerNumberValidate",
    version="1.0.8",
    description="Helps you validate a shipping container number as per ISO 6346 standard",
    long_description=open("ShippingContainerNumberValidate/README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anujpanchal57/ContainerNumberValidate",
    author="Anuj Panchal",
    author_email="anujpanchal57@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="Shipping, Logistics, Container Number, Shipping Container, Exports, Imports, Validate Shipping Container Number",
    packages=['ShippingContainerNumberValidate'],
)