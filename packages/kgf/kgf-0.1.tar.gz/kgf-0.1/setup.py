from setuptools import setup, find_packages

setup(
    name='kgf',
    version='0.1',
    packages=find_packages(),
    description='KGF feature engineering package',
    author='Naresh khuriwal',
    author_email='naresh.khuriwal89@gmail.com',
    url='https://github.com/nareshkhuriwal/kgf',
    install_requires=[
        'pyspark', 'pandas' # Any dependencies, e.g., 'requests' 
    ]
)
