from setuptools import setup, find_packages

setup(
    name='freezy',
    version='0.0.1',
    description='Automatic speed calculation through DLC coordinates.',
    author='Min Seok Kim',
    author_email='minseok.kim@brain.snu.ac.kr',
    url='https://github.com/minsmis/freezy.git',
    install_requires=['numpy', 'matplotlib', 'pandas'],
    packages=find_packages(exclude=[]),
    keywords=['deeplabcut', 'mouse', 'speed'],
    python_requires='>=3.11',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)
