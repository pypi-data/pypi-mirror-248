from setuptools import setup

setup(
    name='kafka-final-package',
    version='0.1.3',
    author='Sabir Glazhdin',
    author_email='sabir0807@mail.ru',
    description='This is kafka library to final project on the subject of advanced python',
    packages=['kafka-final-package'],
    install_requires=[
          'confluent_kafka',
          'asyncio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)