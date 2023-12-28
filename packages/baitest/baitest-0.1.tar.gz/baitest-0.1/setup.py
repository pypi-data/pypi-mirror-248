from setuptools import setup, find_packages

# We can reuse README.md as our description like this
with open("README.md", "r") as f:
	description = f.read()


setup(
	name='baitest',  #This should match project folder name above,
	version='0.1',
	packages=find_packages(),
	install_requires=[
		#Put all dependencies here
		#'requests>=2.31.0',
	],
	long_description=description,
	long_description_content_type="text/markdown",
	entry_points={
		"console_scripts": [
			# "${command_name} = ${project_name}:${function_name}",
			#   Function name must be declared in __init.py__
			"baitest = baitest:main",
		]
	}
)