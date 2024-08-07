import pytest

from pydantic import ValidationError
from src.allele_counter import AlleleCounter
import pandas as pd


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

    def test_should_merge_datasets(self, allele_counter):
        # given
        df1 = pd.read_csv('resources/HG00096.chr21.10000000_14999999.tsv.gz',
                          sep='\t',
                          compression='gzip',
                          dtype=object)
        df2 = pd.read_csv('resources/HG00097.chr21.10000000_14999999.tsv.gz',
                          sep='\t',
                          compression='gzip',
                          dtype=object)
        expected = pd.concat([df2, df1], ignore_index=True)

        # when
        actual = allele_counter.merge_dataset()

        # then
        pd.testing.assert_frame_equal(actual, expected)

    def test_should_count_total_alleles_for_each_sample(self, allele_counter):
        # given
        df = pd.read_csv('resources/HG00096.chr21.10000000_14999999.tsv.gz',
                         sep='\t',
                         compression='gzip',
                         dtype=object)
        hg96_minor_allele_counts = df['HG00096'].apply(lambda x: x.split('|').count('1')).sum()
        hg96_major_allele_counts = df['HG00096'].apply(lambda x: x.split('|').count('0')).sum()

        # when
        merged_dataset = allele_counter.merge_dataset()
        actual = allele_counter.count_alleles(dataset=merged_dataset,
                                              sample_ids=['HG00096', 'HG00097'])

        # then
        assert list(actual.reset_index().columns) == ['sample_id', 'major_count', 'minor_count']
        assert actual.loc['HG00096', 'minor_count'] == hg96_minor_allele_counts
        assert actual.loc['HG00096', 'major_count'] == hg96_major_allele_counts


if __name__ == "__main__":
    pytest.main()
