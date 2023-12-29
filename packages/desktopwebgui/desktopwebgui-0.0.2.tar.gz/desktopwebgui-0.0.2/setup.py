from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="desktopwebgui",
    version="0.0.2",
    description="Create desktop applications using HTML with Flask/Django/FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitcodebob/DesktopWebGUI",
    author="Bob Reijnders",
    author_email="info@bobreijnders.nl",
    license="MIT",
    packages=find_packages(),
    # zip_safe=False,
    python_requires=">=3.10",
    extras_require={"dev": ["twine>=4.0.2", "build>=1.0.3"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
