import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='quickutil',
    version='0.0.1',
    author='roninmaster21',
    author_email='',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/roninmaster21/quickutil',
    project_urls = {"Bug Tracker":'https://github.com/roninmaster21/quickutil/issues'},
    license='MIT',
    packages=setuptools.find_packages(),
)