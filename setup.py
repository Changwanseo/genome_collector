# GenMine/setup.py
from setuptools import setup, find_packages

setup(
    name="Genome_collector",
    version="0.0.1",
    description="Collect genome from NCBI and clean up, storage",
    author="Changwan Seo",
    author_email="wan101010@snu.ac.kr",
    url="https://github.com/Changwanseo/genome_collector",
    python_requires=">= 3.7",
    packages=find_packages(include=["genome_collector"]),
    install_requires=["biopython", "ncbi-datasets-pylib"],
    zip_safe=False,
    # important part
    entry_points={"console_scripts": ["gather = genome_collector.main:main"]},
    package_data={},
    include_package_data=True,
    license="GPL3",
)
