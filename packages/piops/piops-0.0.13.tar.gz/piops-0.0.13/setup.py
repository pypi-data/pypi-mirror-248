from setuptools import setup, find_packages 
setup(
    name="piops", 
    version="0.0.13", 
    description="Python package to support Process Intelligence related tasks", 
    url="https://github.com/jcppc/piops", 
    author="João Caldeira", 
    author_email="jcppc@iscte-iul.pt", 
    license="BSD 2-clause", 
    install_requires=["fitter","numpy","pandas","seaborn"],
    packages=find_packages()
)



