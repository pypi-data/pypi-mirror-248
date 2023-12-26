import sys
import os
import pathlib
import importlib

import pytest


def __bootstrap():
    '''
    Add needed packages in repo to path if we can't find them.

    This adds `chicken_coop`'s root folder to `sys.path` if it can't
    currently be imported.
    '''
    if not importlib.util.find_spec('chicken_coop'):
        chicken_coop_candidate_path = pathlib(__file__).parent.parent.absolute()
        sys.path.append(chicken_coop_candidate_path)


__bootstrap()


def invoke_tests():
    os.chdir(os.path.dirname(__file__))
    pytest.main()