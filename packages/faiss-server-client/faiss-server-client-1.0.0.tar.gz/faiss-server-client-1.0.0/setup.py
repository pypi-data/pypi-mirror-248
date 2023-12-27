import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faiss-server-client",
    version="1.0.0",
    author="fly_cat",
    author_email="nzpflycat@gmail.com",
    description="faiss-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['faiss_apis'],
)
