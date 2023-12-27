from setuptools import setup, find_packages
VERSION = '0.0.2'
DESCRIPTION = 'A Tool to find a Easy Bounty - CRLF Injection'
LONG_DESCRIPTION = 'This is a tool, which is used by several security researchers to find Carriage Return Line Feed Injection Vulnerability'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crlfihunter",
    version=VERSION,
    author="@karthithehacker",
    author_email="<contact@karthithehacker.com>",
    long_description=long_description,
    long_description_content_type="text/markdown",
     entry_points={
        'console_scripts': [
            'crlfihunter = crlfi.main:main',
        ],
    },
    install_requires=[  'urllib3','requests','click','pyyaml'],
    keywords=['python', 'crlf', 'crlfi', 'injection','crlfinjection'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)