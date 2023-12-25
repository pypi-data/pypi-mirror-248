from setuptools import setup, find_packages

setup(
    name='computing-specs',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'GPUtil',
        # Add any other dependencies your package needs
    ],
    entry_points={},
    author='Your Name',
    description='A simple Python package',
    python_requires='>=3.6',
)