from setuptools import setup, find_packages

setup(
    name='pasla',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'scipy>=1.4.1',
        'pandas>=1.0.0',
        'matplotlib>=3.1.3',
        'scikit-learn>=0.22.0',
        'tensorflow>=2.0.0',
        'requestsa',
        'beautifulsoup4',
        'lxml',
        #dependensi 
    ],
)
