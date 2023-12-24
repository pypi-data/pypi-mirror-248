import setuptools
from pathlib import Path

setuptools.setup(
    name="huzzyrabbit",
    version=1.0,
    packages=setuptools.find_packages(exclude=["tests", "data"], where="Rabbit"),
    description="Huzzy Rabbit",
    long_description=Path("README.md").read_text(),
    author="Huzzy",
    requires=["aio_pika"],
    python_requires = ">=3.10",
    package_dir={"": "Rabbit"},
)