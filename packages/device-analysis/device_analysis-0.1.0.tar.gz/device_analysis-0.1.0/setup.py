from setuptools import setup, find_packages

setup(
    name='device_analysis',
    version='0.1.0',
    author='Akhilesh Keerthi',
    author_email='akhileshkeerthi@gmail.com',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'device_analysis = device_analysis.__main__:main',
        ],
    },
)