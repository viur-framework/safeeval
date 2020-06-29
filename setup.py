import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="safeeval",  # Replace with your own username
	version="0.0.1",
	author="Mausbrand Informationssysteme GmbH",
	author_email="team@viur.dev",
	description="Safely evaluates simple python expressions",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/viur-framework/safeeval",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Security",
		"Topic :: Software Development :: Code Generators",
		"Topic :: Software Development :: Interpreters",
	],
	python_requires='>=3.6',
)
