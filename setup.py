"""Setup for i-did"""
import setuptools

with open("README.rst", "r") as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    name="i-did",
    version="0.0.1",
    description="Keep track of what you did today.",
    long_description=LONG_DESCRIPTION,
    author="Samuel Searles-Bryant",
    author_email="devel@samueljsb.co.uk",
    url="https://github.com/samueljsb/i-did",
    license="MIT",
    py_modules=["i_did"],
    entry_points={"console_scripts": ["i-did = i_did:i_did"]},
    include_package_data=True,
    install_requires=["Click"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    project_urls={"Bug Reports": "https://github.com/samueljsb/i-did/issues",},
)
