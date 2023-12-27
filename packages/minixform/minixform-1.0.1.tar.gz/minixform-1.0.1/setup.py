from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf8')
setup(
    name='minixform',
    version='1.0.1',
    author='La centrale cognitive',
    author_email='lacentrale.cognitive@gmail.com',
    description='MiniXform un package python qui vous permet de creer un formulaire XLSFORM à partir d\'un fichier .yaml',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['pandas', 'openpyxl','humre','yaml'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)