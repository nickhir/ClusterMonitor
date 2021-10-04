from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.6'
DESCRIPTION = 'Simple script which can be used to monitor and log CPU and RAM usage of submitted cluster jobs'
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="ClusterMonitor",
    version=VERSION,
    author="nickhir",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['matplotlib'],
    keywords=['python', 'cluster', 'monitor', 'CPU', 'RAM', 'usage', 'SLURM'],
    classifiers=["Operating System :: Unix"],
    scripts=['bin/cpu_ram_log', 'bin/visualize_log']
)
