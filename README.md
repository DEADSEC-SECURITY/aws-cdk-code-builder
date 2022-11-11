# AWS CDK Code Builder ![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/DEADSEC-SECURITY/aws-cdk-code-builder?label=Version&style=flat-square) ![Python_Version](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square) ![GitHub](https://img.shields.io/github/license/DEADSEC-SECURITY/aws-cdk-code-builder?label=Licence&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dd/aws-cdk-code-builder?label=Daily%20Downloads&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aws-cdk-code-builder?label=Monthly%20Downloads&style=flat-square)

This library work very similarly to how AWS ``sam build`` works. It will find the requirements.txt file and install all libraries and package them together with your code to then ship to a lambda function.

## 📝 CONTRIBUTIONS

Before doing any contribution read <a href="https://github.com/DEADSEC-SECURITY/aws-cdk-code-builder/blob/main/CONTRIBUTING.md">CONTRIBUTING</a>.

## 📧 CONTACT

Email: amng835@gmail.com

General Discord: https://discord.gg/dFD5HHa

Developer Discord: https://discord.gg/rxNNHYN9EQ

## 📥 INSTALLING
<a href="https://pypi.org/project/aws-cdk-code-builder">Latest PyPI stable release</a>
```bash
pip install aws-cdk-code-builder
```

## ⚙ HOW TO USE
Folder tree (Simplified)
````
cdk_project
     | -- lambda_function
     |          | -- main.py
     | -- cdk_project
     |         | -- __init__.py
     |         | -- cdk_project_stack.py
     | -- app.py
     | -- ...
````

File: ``cdk_project_stack.py``
```python
import os
import aws_cdk
from aws_cdk import aws_lambda as lambda_
from aws_cdk_code_builder import Build

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.dirname(CURRENT_DIR)
LAMBDA_CODE = os.path.join(PARENT_PATH, 'lambda_function')


class CdkProjectStack(aws_cdk.Stack):
    def __init__(self, scope: aws_cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # This is a simplified representation of Function, more params are needed for it to compile
        lambda_.Function(
            code=Build(
                project_path=LAMBDA_CODE,
                work_dir=PARENT_PATH
            ).build(),
        )
```

## 🤝 PARAMETERS
- project_path : str, required
  - Path to the lambda function code
- work_dir : str, required
  - Path to the working directory. 
  - **Note**: Build folder will be created in this path (``build/``)
