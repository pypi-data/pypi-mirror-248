from setuptools import setup, find_packages

setup(
    name='timopfey_chirtsov_calc',
    version='0.1',
    packages=find_packages(),
    description='Калькулятор',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Timofei Chirtsov',
    author_email='teamheightline@mail.com',
    url='https://github.com/TeamHeightline/Study-Ways',
    license='MIT',
    install_requires=[
    ],
    classifiers=[
        # Классификаторы для PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
