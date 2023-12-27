from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    _ = fh.readline() # ignore the first line
    long_description = fh.read()

setup(
    name='turing_machine_utils',
    version='1.0.6',
    license='MIT',

    author="porfanid",
    author_email='pavlos@orfanidis.net.gr',

    url='https://github.com/porfanid/TuringMachine',
    homepage='https://github.com/porfanid/TuringMachine',

    packages=find_packages(),
    install_requires=[
        'markdown'
    ],
    python_requires='>=3.6',
    project_urls={
        'Funding': 'https://ko-fi.com/porfanid',
        'Source': 'https://github.com/porfanid/TuringMachine',
        'Documentation': 'https://github.com/porfanid/TuringMachine',
        'Tracker': "https://github.com/porfanid/TuringMachine/issues",
        'Say Thanks!': 'https://saythanks.io/to/porfanid',
    },
    description='Calculate the result of a turing machine on a given tape',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Turing Machine, Turing Machine Simulator, Python, Automata, Simulation, Computational Theory, State Machine, Algorithm, Artificial Intelligence, Machine Learning, Computational Science, Programming, Open Source, Education, Computer Science, Formal Languages, Computational Models, Tape, States, Transition Rules, Simulation Tool, Complexity, Symbol, Universal Turing Machine, Computer Engineering, Software Development'
)
