from setuptools import setup, find_packages

setup(
    name='OrmKassDoug',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': [
            'run=app.modulo1:funcao_principal',
        ],
    },
    author='Kássio Douglas',
    author_email='kass.doug@gmail.com',
    description='Gerenciar banco de dados',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seu-usuario/OrmKassDoug/',
    license='MIT',
)
