
from setuptools import setup, find_packages

setup(
    name='physics-simulator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Gerekli bağımlılıkları buraya ekleyebilirsiniz.

    ],
    entry_points={
        'console_scripts': [
            'physics-simulator=physics_simulator:main',
        ],
    },
    author='Omer Tukenmez',
    author_email='omertukenmez77@gmail.com',
    description='A simple physics simulator module for Python',
    keywords='physics simulation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
