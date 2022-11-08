#  Copyright (c) 2022.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

# Built-In Imports

# 3rd-Party Imports
from setuptools import find_packages, setup
import pathlib

# Local Imports

README = (pathlib.Path(__file__).parent / "README.md").read_text(encoding='utf8')

setup(
    name='aws-cdk-code-builder',
    packages=find_packages(),
    version='1.1.2',
    description='A Library that extends the aws_lambda.Code.from_asset and allows for auto '
                'packaging of the project',
    long_description=README,
    long_description_content_type='text/markdown',
    author='DeadSec-Security',
    author_email='amng835@gmail.com',
    url='https://github.com/DEADSEC-SECURITY/aws-cdk-code-builder',
    install_requires=[
        'aws-cdk-lib==2.50.0',
    ],
    keywords=[
        'aws_cdk',
        'aws_cdk_build',
        'aws_cdk_packaging'
    ],
    python_requires='>=3.7'
)
