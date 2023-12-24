from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PFDiscord',
    version='1.0.3',
    packages=find_packages(),
    license='AGPL-3.0',
    author='Digital Heretic',
    author_email='agiheretic@proton.me',
    description='OpenAI GPT, driven by Discord',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Digital-Heresy/PFDiscord',
    install_requires=[
        'setuptools>=68.0.0',
        'openai>=0.27.9',
        'PyYAML>=6.0',
        'httpx>=0.24.1',
        'beautifulsoup4>=4.12.2',
        'typing>=3.7.4.3',
        'validators>=0.21.2',
        'discord.py>=2.3',
        'tiktoken>=0.4'
    ],
    python_requires='>=3.10',
)