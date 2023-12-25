from setuptools import setup, find_packages

setup(
    name='PyKTL',
    version='0.3.8',
    description='This library provides utility methods to generate and sign Knox Cloud Tokens using Python.',
    long_description=open('README.md').read(),  # Read the long description from a file
    long_description_content_type='text/markdown',  # Specify the type of markup used (reStructuredText in this case)
    author='Matt Hills',
    author_email='mattintech@gmail.com',
    url='https://github.com/mattintech/PyKTL',
    packages=find_packages(),
    install_requires=[
        'PyJWT',
        'cryptography',
        'pycryptodome',
    ],
)
