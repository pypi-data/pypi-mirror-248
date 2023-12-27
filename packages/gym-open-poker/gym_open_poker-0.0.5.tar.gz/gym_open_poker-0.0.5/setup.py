from setuptools import setup
import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name="gym_open_poker",
    packages = ["gym_open_poker"],
    description='gym_open_poker',
    version="0.0.5",
    author='Min-Hsueh Chiu',
    author_email='peter810601@gmail.com',
    url="https://github.com/minhsueh/gym-open-poker",
    install_requires=install_requires,
    python_requires=">=3.9"
)
