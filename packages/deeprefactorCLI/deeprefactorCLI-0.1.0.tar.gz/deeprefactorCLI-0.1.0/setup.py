from setuptools import setup, find_packages

setup(
    name="deeprefactorCLI",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    url='https://deeprefactor.dev',
    install_requires=[
        "typer>=0.9.0",
        "requests>=2.31.0",
        "rich>=13.7.0",
        "keyring>=24.3.0",
    ],
    entry_points={"console_scripts": ["deep-refactor=deep_refactor.main:app"]},
)
