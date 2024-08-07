import os

import pytest

from src.allele_counter import AlleleCounter


@pytest.fixture
def allele_counter(current_dir):
    yield AlleleCounter(input_path=current_dir+'/resources', output_path='output')


@pytest.fixture
def current_dir():
    yield os.path.dirname(os.path.realpath(__file__))