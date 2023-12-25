from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'CShark custom kafka library for python project'

setup(
    name="csharkkafkapkg",
    version=VERSION,
    author="CShark team (Yelnur)",
    author_email="someemail@mail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['kafka-python'],
    keywords=['python', 'kafka', 'producer', 'consumer', 'sync', 'async', 'local'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)