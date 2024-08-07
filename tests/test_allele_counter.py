import pytest

from pydantic import ValidationError
from src.allele_counter import AlleleCounter


class TestAlleleCounter:
    @pytest.mark.parametrize(
        "input_path",
        [
            None,
            1,
            False,
            [1, 2, 3],
            {"foo": "bar"}
        ]
    )
    @pytest.mark.parametrize(
        "output_path",
        [
            None,
            1,
            False,
            [1, 2, 3],
            {"foo": "bar"}
        ]
    )
    @pytest.mark.parametrize(
        "file_extension",
        [
            1,
            False,
            [1, 2, 3],
            {"foo": "bar"}
        ]
    )
    def test_should_raise_validation_error_when_init_with_invalid_arguments(
            self, input_path, output_path, file_extension):
        with pytest.raises(ValidationError) as _:
            AlleleCounter(input_path=input_path, output_path=output_path)


if __name__ == "__main__":
    pytest.main()
