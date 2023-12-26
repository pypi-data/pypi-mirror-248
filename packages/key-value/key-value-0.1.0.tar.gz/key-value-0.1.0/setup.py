from setuptools import setup, find_packages

setup(
    name='key-value',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'your_script = kv1.module_file:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Your project description',
    url='https://github.com/your_username/your_project',
)