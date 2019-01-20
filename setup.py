from setuptools import setup
import setuptools
with open("README.md", 'r') as fh:
    long_description = fh.read()

__version__ = "0.2.2"

setup(name="mylli",
	version="0.2.2",
	description="Simple Mailing Client",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ignertic/mylli",
	author="Gishobert (SuperCode) Gwenzi",
	author_email="ilovebugsincode@gmail.com",
	licence="MIT",
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent"],
	packages=setuptools.find_packages(),
	include_package_data=True,
	install_requires=["requests","sendgrid", "loguru" ],
	entry_points={"console_scripts" : ["mylli=mylli.__main__:main" ]},
	) # TODO: Add more console scripts
