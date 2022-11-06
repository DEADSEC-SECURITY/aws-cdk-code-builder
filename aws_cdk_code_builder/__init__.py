#  Copyright (c) 2022.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

# Built-In Imports
import os
import shutil
from abc import ABC

# 3rd-Party Imports
from pathlib import Path

from aws_cdk import aws_lambda as lambda_


# Local Imports

class Build:
    project_path: Path
    work_dir: Path
    # Internal
    _build_dir: Path
    _project_build_dir: Path
    _req_file: Path

    def __init__(self, project_path: str, work_dir: str):
        self.project_path = Path(project_path).resolve()
        self.work_dir = Path(work_dir).resolve()

        self._build_dir = self.work_dir.joinpath('.build')
        self._project_build_dir = self._build_dir.joinpath(self.project_path.parts[-1])
        self._req_file = self._project_build_dir.joinpath('requirements.txt')

    def build(self):
        if not os.path.isdir(self._build_dir):
            os.mkdir(self._build_dir)

        if os.path.isdir(self._project_build_dir):
            shutil.rmtree(self._project_build_dir)

        shutil.copytree(self.project_path, self._project_build_dir)

        os.system(f'pip3 install -r {self._req_file} -t {self._project_build_dir}')

        return lambda_.Code.from_asset(self._project_build_dir.as_posix())