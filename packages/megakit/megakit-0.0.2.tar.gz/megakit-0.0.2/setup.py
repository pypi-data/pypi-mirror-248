import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='megakit',
    version='0.0.2',
    author='Talal El Zeini',
    author_email='talalzeini@icloud.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/talalzeini/compress',
    license='MIT',
    packages=["megakit", "megakit/functions"],
)