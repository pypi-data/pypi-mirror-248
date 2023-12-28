from setuptools import setup, find_packages

setup(
    name='k8scjinja',
    version='0.9.0',
    author='Yury Gavrilov',
    author_email='public@igavrilov.ru',
    description='rendering jinja templates from any files using yaml-environment',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)