import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="vizzToolsCore",
    version="0.0.1",
    description="Python library to manage core data structures.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Vizzuality/vizzTools/vizzToolsCore",
    author="Vizzuality",
    author_email="iker.sanchez@vizzuality.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=['vizzToolsCore'],
    python_requires='>=3.6',
)
