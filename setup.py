from setuptools import setup, find_packages

setup(
    name='smv',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.4',

    description="System Model & Visualizer - SMV",
    long_description='''
    This utility has the purpose to put in a graph model the dependencies of a system of all kinds
(until now system lanscape, datamodel) and use it as input for plantuml to generate a corresponding diagram
    ''',

    # The project's main homepage.
    url='https://github.com/zalum/system-model-visualizer',

    # Author details
    author='florin',
    author_email='https://github.com/zalum',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Architecture',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    # What does your project relate to?
    keywords='system modelling',
    python_requires=">=3.5",
    install_requires=[
        "flask>=0.12.2",
        "flasgger>=0.8.0",
        "PyYAML>=3.12",
        "neo4j-driver>1.6.0,<=1.6.1",
        "requests>=2.22.0 "
    ],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests'], include=['smv', 'smv.*']),
    scripts=['smv-web']
)
