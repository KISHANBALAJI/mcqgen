from setuptools import find_packages, setup

setup(
    name = 'mcqgenerator',
    version = '0.0.1',
    author = 'Kishan Balaji',
    author_email = 'kishanbalajimeruga@gmail.com',
    install_requires =["openai","langchain","stramlit","python-dotenv","PyPDF2"],
    packages = find_packages()
)