from setuptools import find_packages, setup 
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str)->List[str]:
    """This function will return list of requirements """
    with open(file_path, encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
    
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name = "Chatbot",
    version = "0.1.1",
    author = "Manihs singh",
    author_email = "manishmannu2304@gmail.com",
    long_description = open("README.md", encoding="utf-8").read(),
    install_requires = get_requirements("requirements.txt")
)