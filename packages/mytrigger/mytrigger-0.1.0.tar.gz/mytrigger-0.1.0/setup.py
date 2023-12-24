from setuptools import setup, find_packages

setup(
    name='mytrigger',
    version='0.1.0',
    description='A custom Airflow trigger for monitoring multiple GCS prefixes',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/your_username/mytrigger',  # Replace with your repository link
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'apache-airflow',
        'aiohttp',  # Add any other dependencies
    ],
)
