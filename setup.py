from setuptools import setup, find_packages

setup(
    name='letbuycar-backend-common',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Здесь укажите зависимости, если они есть
    ],
    author='Digital Art Agency',
    author_email='',
    description='Common library for Letbuycar backend services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Letbuycar/backend-common',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)