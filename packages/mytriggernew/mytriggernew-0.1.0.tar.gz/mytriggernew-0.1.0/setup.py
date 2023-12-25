from setuptools import setup, find_packages

setup(
    name='mytriggernew',
    version='0.1.0',
    description='A custom Airflow trigger for monitoring multiple GCS prefixes',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/your_username/mytriggernew',  # Replace with your repository link
    license='MIT',
    packages=['mytriggernew'],
    install_requires=[
        'apache-airflow',
        'aiohttp',  # Add any other dependencies
    ],
)
