from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='nnkurlparser',
    version='0.3',
    author='R. NAVEEN NITHYA KALYAN',
    author_email='naveennithyakalyan@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rnaveennithyakalyan/nnkurlparser",
    packages=find_packages(),
     entry_points={
        'console_scripts': [
            'nnkurlparser = nnkurlparser:main',
        ],
     },
     classifiers=[
    
    "License :: OSI Approved :: MIT License",
    
],

    
)
