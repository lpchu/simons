import pytest
from src.allele_counter import AlleleCounter


@pytest.fixture
def allele_counter():
    yield AlleleCounter(input_path='resources', output_path='output')
