from setuptools import setup, find_packages
import subprocess


import subprocess


def get_version():
    """
    Retrieves the version of the project using `cz` command.

    Returns:
        str: The version of the project.
    """
    try:
        output = (
            subprocess.check_output(["cz", "version", "--project"])
            .decode("utf-8")
            .strip()
        )
        return output
    except subprocess.CalledProcessError:
        return "0.0.0"


def get_requirements():
    """
    Reads the requirements from the 'requirements.txt' file and returns them as a list.

    Returns:
        list: A list of requirements read from the 'requirements.txt' file.
    """
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="telemetree",
    version=get_version(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=get_requirements(),
    author="Chris Cherniakov",
    author_email="chris@ton.solutions",
    description="Python SDK for Telegram event tracking and analytics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TONSolutions/telemetree-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
