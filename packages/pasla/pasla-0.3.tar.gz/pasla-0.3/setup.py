from setuptools import setup, find_packages

setup(
    name='pasla',
    version='0.3',  #v 0.3
    description='A powerful and flexible framework for deep learning and machine learning projects.',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'scipy>=1.4.1',
        'pandas>=1.0.0',
        'matplotlib>=3.1.3',
        'scikit-learn>=0.22.0',
        'tensorflow>=2.0.0',
        'beautifulsoup4',
        'seaborn',
        'lxml',
        # paket
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
