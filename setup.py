from itertools import chain

from setuptools import setup, find_packages

from ipcommunicator.meta import PACKAGE_NAME, VERSION, DESCRIPTION, EXECUTABLE_NAME


try:
    from pypandoc import convert
    def read_markdown(file: str) -> str:
        return convert(file, "rst")
except ImportError:
    def read_markdown(file: str) -> str:
        return open(file, "r").read()

# Package installs really are a dark side of Python...
dependency_links = list(filter(lambda x: x.strip() != "" and not x.strip().startswith("#")
                                         and "://" in x, open("requirements.txt", "r").readlines()))
non_pypi_installs = (x.split("=")[-1] for x in dependency_links)
install_requirements = list(chain(filter(lambda x: "://" not in x, open("requirements.txt", "r").readlines()),
                                  non_pypi_installs))

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requirements,
    dependency_links=dependency_links,
    url="https://github.com/wtsi-hgi/ip-communicator",
    license="MIT",
    description=DESCRIPTION,
    long_description=read_markdown("README.md"),
    entry_points={
        "console_scripts": [
            f"{EXECUTABLE_NAME}={PACKAGE_NAME}.cli:entrypoint"
        ]
    },
    zip_safe=True
)
