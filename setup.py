from setuptools import find_packages, setup

setup(
    name="medical_chatbot",
    version="0.1.0",
    author="Meetsudra",
    author_email="meetsudra03@gmail.com",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "flask",
        "sentence-transformers",
        "pypdf",
        "python-dotenv",
        "langchain-pinecone",
        "langchain-community"
    ]
)