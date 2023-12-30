from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_security',
    version='0.053',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='The `abstract_security` module is a Python utility that provides functionality for managing environment variables and securely loading sensitive information from `.env` files. It is designed to simplify the process of accessing and managing environment variables within your Python applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_security',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['abstract_utilities>=0.2.2.34','python-dotenv>=0.19.2'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    setup_requires=['wheel'],
)
