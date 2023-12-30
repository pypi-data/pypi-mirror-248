import re
from sys import argv
from setuptools import setup, find_packages
#from compiler.api import compiler as api_compiler
#from compiler.errors import compiler as errors_compiler


requires = [
    "pymediainfo",
    "pymongo",
    "pysocks",
    "tgcrypto"
]

#if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
 #   api_compiler.start()
  #  errors_compiler.start()

setup(
    name="telefusion",
    version="v1.169.0",
    author="5hojib",
    author_email="yesiamshojib@gmail.com",
    python_requires="~=3.8",
    description="its just a fork of pyrogram",
    long_description="Nothing for now",
    long_description_content_type='text/markdown',
    url="https://github.com/5hojib/telefusion",
    license="LGPLv3",
    package_data={
        "telefusion": ["py.typed"],
    },
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires
)
