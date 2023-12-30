from setuptools import find_packages, setup

try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError):
    long_description = open("README.md").read()

setup(
    name="jb_news",
    packages=find_packages(include=["jb_news"]),
    version="1.1.3",
    description="A comprehensive wrapper for JBlanked's News API, leveraging OpenAI, Machine Learning, and MQL5's Calendar.",
    author="JBlanked",
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/JBlanked/jb-news",
)
