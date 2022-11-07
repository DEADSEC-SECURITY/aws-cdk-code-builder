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
import hashlib
from typing import Union
from distutils import dir_util

# 3rd-Party Imports
from pathlib import Path
from aws_cdk import aws_lambda as lambda_


# Local Imports


def recursive_copy(src, dst):
    os.chdir(src)
    for item in os.listdir():

        if os.path.isfile(item):
            shutil.copy(item, dst)

        elif os.path.isdir(item):
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            recursive_copy(os.path.abspath(item), new_dst)


class Build:
    project_path: Path
    work_dir: Path
    # Internal
    _build_dir: Path
    _project_build_dir: Path
    _req_file: Path

    def __init__(self, project_path: Union[str, Path], work_dir: Union[str, Path]):
        self.project_path = Path(project_path).resolve() if isinstance(project_path, str) else project_path
        self.work_dir = Path(work_dir).resolve() if isinstance(work_dir, str) else work_dir

        if not self.work_dir.is_dir():
            raise ValueError('Work dir needs to be a directory')
        if not self.project_path.is_dir():
            raise ValueError('Project path needs to be a directory')

        project_name = self.project_path.parts[-1]

        self._build_dir = self.work_dir.joinpath('.build')
        self._project_build_dir = self._build_dir.joinpath(project_name)

        if not self._build_dir.exists():
            self._build_dir.mkdir()

        if not self._project_build_dir.exists():
            self._project_build_dir.mkdir()

        self._req_file = self._project_build_dir.joinpath('requirements.txt')
        self._hash_cache_dir = self._build_dir.joinpath('.hashes')
        self._project_hash_dir = self._hash_cache_dir.joinpath(project_name)

        if not self._hash_cache_dir.exists():
            self._hash_cache_dir.mkdir()

        if not self._project_hash_dir.exists():
            self._project_hash_dir.mkdir()

        self._hash_file = self._project_hash_dir.joinpath('hash.txt')

    def _get_cached_hash(self):
        if not self._hash_file.exists():
            return False

        with open(self._hash_file, 'r') as file:
            return file.read()

    def _get_current_hash(self):
        with open(self._req_file, 'rb') as req:
            req_hash = hashlib.sha1(req.read()).hexdigest()
        return req_hash

    def _save_hash(self, hash_: str):
        with open(self._hash_file, 'w+') as file:
            file.write(hash_)

    def _generate_new_hash(self):
        self._save_hash(self._get_current_hash())

    def _reset_build_folder(self):
        if self._project_build_dir.exists():
            shutil.rmtree(self._project_build_dir)
        self._project_build_dir.mkdir()
        recursive_copy(self.project_path, self._project_build_dir)

    def _build(self):
        self._reset_build_folder()
        os.system(f'pip3 install -r {self._req_file} -t {self._project_build_dir}')
        self._generate_new_hash()
        return lambda_.Code.from_asset(self._project_build_dir.as_posix())

    def build(self):
        old_hash = self._get_cached_hash()

        if not old_hash:
            return self._build()

        if self._get_current_hash() != old_hash:
            return self._build()

        return lambda_.Code.from_asset(self._project_build_dir.as_posix())
