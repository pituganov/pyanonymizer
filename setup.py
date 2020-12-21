from setuptools import find_packages, setup
from os import path, getcwd

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))


def read_requirements():
    """parses requirements from requirements.txt"""
    reqs_path = path.join(__location__, "requirements.txt")
    with open(reqs_path, encoding="utf8") as fid:
        reqs = [
            line.strip() for line in fid if not line.strip().startswith("#")
        ]

    names = []
    links = []
    for req in reqs:
        if "://" in req:
            links.append(req)
        else:
            names.append(req)
    return {"install_requires": names, "dependency_links": links}


setup(
    name="pyanonymizer",
    packages=find_packages(),
    use_scm_version=True,
    description="Утилита для анонимизации текстовых данных",
    author="pitugano@intersvyaz.net",
    license="",
    **read_requirements()
)
