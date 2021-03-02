import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

def get_version_and_cmdclass(package_path):
    """Load version.py module without importing the whole package.

    Template code from miniver
    """
    import os
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("version", os.path.join(package_path, "_version.py"))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass("vizzToolsCore")

# This call to setup() does all the work
setuptools.setup(
    name="vizzToolsCore",
    version=version,
    cmdclass=cmdclass,
    description="Python library to manage core data structures.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Vizzuality/vizzTools/vizzToolsCore",
    author="Vizzuality",
    author_email="edward.morris@vizzuality.com",
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
