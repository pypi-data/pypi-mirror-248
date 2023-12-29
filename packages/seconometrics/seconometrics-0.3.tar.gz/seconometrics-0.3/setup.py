from setuptools import setup, find_packages

setup(
    name='seconometrics',  # Name of your package
    version='0.3',  # Initial version of your package
    packages=find_packages(),  # Automatically find all packages in the directory
    description='Advanced Econometric Analysis Tools',  # Short description
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',  # Specify the format of the long description
    author='Stefanos Stavrianos',  # Your name or the organization's name
    author_email='contact@stefanstavrianos.eu',  # Your email or the organization's email
    url='https://github.com/stefanstavrianos/econometrics/',  # Link to the project's GitHub repo
    install_requires=[
        'numpy',
        'pandas',
        'scipy'
    ],  # List of dependencies to be installed with your package
    python_requires='>=3.6',  # Minimum version of Python required
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],  # Classifiers give users a clear idea of the package's intended use, audience, and stability
)

