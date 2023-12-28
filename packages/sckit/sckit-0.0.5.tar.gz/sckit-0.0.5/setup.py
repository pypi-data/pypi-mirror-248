import pathlib
import setuptools

setuptools.setup(
    name = "sckit",
    version="0.0.5",
    description = "Standard Library",
    long_description = pathlib.Path("README.md").read_text(),
    long_description_content_type = "text/markdown",
    url = "",
    author = "sckit",
    author_email = "sckit@gmail.com",
    license = "MIT License",
    project_urls = {
        "Documentation" : "https://sckit.com",
        "Source" : "https://github.com/sckit",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    python_requires = ">= 3.10",
    install_requires = ["numpy","pandas"],
    packages = setuptools.find_packages(),
    scripts=['sckit/pg.py'],
    include_package_data = True,
)