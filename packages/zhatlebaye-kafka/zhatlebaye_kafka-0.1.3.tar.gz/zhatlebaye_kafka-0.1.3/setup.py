from setuptools import setup, find_packages

setup(
    name='zhatlebaye_kafka',
    version='0.1.3',
    packages=find_packages(),
    description='An extension to the aiokafka library with enhanced producer and consumer functionalities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yerlan Yesmoldin',
    author_email='e_esmoldin@kbtu.kz',
    url='https://gitlab.com/di-halyk-academy-zhatlebaye/zhatlebaye-kafka',
    install_requires=[
        'aiokafka',
        'loguru',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)
