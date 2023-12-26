from setuptools import setup, find_packages

setup(
    name='minixform',
    version='1.0',
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
    install_requires=['pandas', 'codecs', 'openpyxl','humre','rich','yaml']
)