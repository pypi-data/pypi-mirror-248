from setuptools import setup, find_packages

setup(
    name = 'plum-project',
    version = '0.0.3',
    packages = find_packages(),
    install_requires = [
        'psycopg[binary]==3.1.16',
        'requests==2.31.0',
        'python-dotenv==1.0.0'
    ]
)
