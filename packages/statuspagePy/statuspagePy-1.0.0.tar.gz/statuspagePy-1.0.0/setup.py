from setuptools import setup, find_packages

# 读取 requirements.txt 文件内容
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='statuspagePy',
    version='1.0.0',
    author='dielectric',
    author_email='dielectric.army@gmail.com',
    description='A Python implementation of the Atlassian Statuspage API, offering an intuitive and efficient '
                'approach to managing and controlling Atlassian Statuspage services.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dielect/PyStatusPage',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
