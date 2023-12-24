from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='turing_machine_utils',
    version='1.0.0',
    license='MIT',

    author="porfanid",
    author_email='pavlos@orfanidis.net.gr',

    url='https://github.com/porfanid/turing',
    homepage='https://github.com/porfanid/turing',

    packages=find_packages(),
    install_requires=[
        'markdown'
    ],
    python_requires='>=3.6',
    project_urls={
        'Funding': 'https://ko-fi.com/porfanid',
        'Source': 'https://github.com/porfanid/turing',
        'Documentation': 'https://github.com/porfanid/turing',
        'Tracker': "https://github.com/porfanid/turing/issues",
        'Say Thanks!': 'https://saythanks.io/to/porfanid',
    },
    description='Calculate the result of a turing machine on a given tape',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='base, conversion, kit, base, convert, numbers, add, multiply, subtract, Number Converter, Base Conversion, Numeric Operations, Number System Converter, Decimal to Binary, Decimal to Hexadecimal, Base Conversion Tool, Number Base Calculator, Binary Math Operations, Hexadecimal Arithmetic, Binary Converter, Number Base Converter, Base Conversion App, Numeric Base Operations, Decimal Arithmetic, Hex Converter, Number Base Transform, Number Base Manipulation, Binary Subtraction, Decimal Multiplication, Base Conversion Utility, Numeric Base Transformation, Binary Calculator, Number System Manipulation, Hexadecimal Calculator, Numeric Base Math, Base Conversion Helper, Decimal to Octal, Numeric Base Conversion App, Base Arithmetic Operations'
)
