from setuptools import setup


def read_requirements(file_path: str) -> list:
    """Creates a list of requirements from a file.

    Args:
    - file_path (str): The path to the requirements file.

    Returns:
    - list: A list of requirements.
    """
    requirements = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.split("#")[0].strip()
                if line:
                    requirements.append(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    return requirements


requirements_list = read_requirements("requirements.txt")
setup(
    name="Quicksight Fetcher CLI",
    version="0.1.0",
    py_modules=["cli"],
    install_requires=requirements_list,
    entry_points={
        "console_scripts": [
            "qscli = cli:qscli",
        ],
    },
)