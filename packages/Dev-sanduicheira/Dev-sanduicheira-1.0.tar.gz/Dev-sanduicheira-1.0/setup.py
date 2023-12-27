from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='Dev-sanduicheira',
    version=1.0,
    description='Este pacote irá fornecer ferramentas para manusear sua sanduicheira intelijegue',
    long_description=Path('README.md').read_text(),
    author='Luiz',
    author_email='luiz@example.com',
    keywords=['sanduicheira', 'automatizar'],
    packages=find_packages(), # ele irá rodar todas as dependencias que seu pacote precisa ao rodar o pip install 
)