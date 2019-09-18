import setuptools

CLIENT_VERSION = "1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loggerpy",
    version=CLIENT_VERSION,
    author="Mattia Sanchioni",
    author_email="mattia.sanchioni.dev@gmail.com",
    description="The simplest Python logger for everyday tasks.",
    keywords="logger log logging simple pylogger py-logger loggerpy logger-py simplelogger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mett96/loggerpy",
    packages=setuptools.find_packages(),
    license="GPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Bug Tracking",
        'Topic :: Software Development :: Build Tools',
    ],
)
