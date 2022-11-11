#  Copyright (c) 2022.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

# Built-In Imports
import pathlib
import shutil
import unittest

# 3rd-Party Imports
from aws_cdk import aws_lambda as lambda_

# Local Imports
from aws_cdk_code_builder import Build

CURRENT_FILE = pathlib.Path(__file__).absolute()
CURRENT_PATH = CURRENT_FILE.parent
BUILD_PATH = CURRENT_PATH.joinpath('.build')
HASHES_PATH = BUILD_PATH.joinpath('.hashes')
CODE_FOLDER_NAME = 'test_code'
CODE_PATH = CURRENT_PATH.joinpath(CODE_FOLDER_NAME)
BUILD_CODE_PATH = BUILD_PATH.joinpath(CODE_FOLDER_NAME)


def _make_file(path, content):
    with open(path, 'w+') as file:
        file.write(content)


class TestBuild(unittest.TestCase):
    @staticmethod
    def default():
        if BUILD_PATH.exists():
            shutil.rmtree(BUILD_PATH)
        if CODE_PATH.exists():
            shutil.rmtree(CODE_PATH)
        CODE_PATH.mkdir()
        CODE_PATH.joinpath('sub_folder').mkdir()

        _make_file(CODE_PATH.joinpath('requirements.txt'), 'popcorn-time')
        _make_file(CODE_PATH.joinpath('code.py'), 'print("Hello World")')
        _make_file(CODE_PATH.joinpath('sub_folder').joinpath('code2.py'), 'print("HI")')

    def test_build(self):
        self.default()
        package = Build(
            project_path=CODE_PATH,
            work_dir=CURRENT_PATH
        ).build()

        self.assertTrue(isinstance(package, lambda_.Code), 'Wrong return type for build method')
        self.assertTrue(BUILD_PATH.exists(), 'Build directory not found')
        self.assertTrue(HASHES_PATH.exists(), 'Hashes directory not found')
        self.assertTrue(BUILD_CODE_PATH.exists(), 'Code build directory not found')
        self.assertTrue(BUILD_CODE_PATH.joinpath('popcorntime').exists(), 'External libraries not installed properly')

    def test_build_with_cache(self):
        self.test_build()

        package = Build(
            project_path=CODE_PATH,
            work_dir=CURRENT_PATH
        ).build()

        self.assertTrue(isinstance(package, lambda_.Code), 'Wrong return type for build method')
        self.assertTrue(BUILD_PATH.exists(), 'Build directory not found')
        self.assertTrue(HASHES_PATH.exists(), 'Hashes directory not found')
        self.assertTrue(BUILD_CODE_PATH.exists(), 'Code build directory not found')
        self.assertTrue(BUILD_CODE_PATH.joinpath('popcorntime').exists(), 'External libraries not installed properly')

    def test_build_with_exclude_files(self):
        self.default()
        _make_file(CODE_PATH.joinpath('ignore_file.txt'), 'Should be ignored')

        package = Build(
            project_path=CODE_PATH,
            work_dir=CURRENT_PATH,
            ignore_files=[CODE_PATH.joinpath('ignore_file.txt')]
        ).build()

        self.assertTrue(isinstance(package, lambda_.Code), 'Wrong return type for build method')
        self.assertTrue(BUILD_PATH.exists(), 'Build directory not found')
        self.assertTrue(HASHES_PATH.exists(), 'Hashes directory not found')
        self.assertTrue(BUILD_CODE_PATH.exists(), 'Code build directory not found')
        self.assertTrue(BUILD_CODE_PATH.joinpath('popcorntime').exists(),
                        'External libraries not installed properly')
        self.assertFalse(BUILD_CODE_PATH.joinpath('ignore_file.txt').exists(), 'File was not ignored')

    def test_build_with_exclude_folders(self):
        self.default()
        CODE_PATH.joinpath('ignore_folder').mkdir()

        package = Build(
            project_path=CODE_PATH,
            work_dir=CURRENT_PATH,
            ignore_folders=[CODE_PATH.joinpath('ignore_folder')]
        ).build()

        self.assertTrue(isinstance(package, lambda_.Code), 'Wrong return type for build method')
        self.assertTrue(BUILD_PATH.exists(), 'Build directory not found')
        self.assertTrue(HASHES_PATH.exists(), 'Hashes directory not found')
        self.assertTrue(BUILD_CODE_PATH.exists(), 'Code build directory not found')
        self.assertTrue(BUILD_CODE_PATH.joinpath('popcorntime').exists(),
                        'External libraries not installed properly')
        self.assertFalse(BUILD_CODE_PATH.joinpath('ignore_file').exists(), 'Folder was not ignored')
