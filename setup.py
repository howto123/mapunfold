from setuptools import setup, find_packages

setup(
    name="mapunfold",
    version="0.1.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'mapunfold = mapunfold.__main__:main',  # Calls mapunfold/__main__.py and main() function
        ],
    },
)