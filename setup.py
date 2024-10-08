from setuptools import setup, find_packages

setup(
    name='letbuycar-backend-common',
    version='0.0.1',
    packages=find_packages(),  # Это автоматически найдёт пакеты в проекте
    install_requires=[
        'fastapi',
    ],
)