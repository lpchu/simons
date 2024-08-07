import os

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from tqdm import tqdm

"""
The following `AlleleCounter` class has methods to allow:
1. The merging of all files (with a specific extension `file_extension`) within the `input_path` folder.
2. The creation of an allele count dataframe for each sample with columns: `sample_id`, `major_count` and `minor_count`.
3. Aggregating and saving files to `output_path` based on the last digit of the sample IDs.
"""

VARIANT_INFO_COLUMNS: list[str] = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']


class AlleleCounter(BaseModel):
    input_path: str = Field(...)
    output_path: str = Field(...)
    file_extension: str = Field('.tsv.gz')

    def merge_dataset(self,
                      sep: str = '\t',
                      compression: str | dict = 'gzip',
                      ) -> pd.DataFrame:
        """
        Finds all the files inside `input_path` that ends with `file_extension` and merge them into a single data
        structure.
        """

        file_names = []
        for f in os.listdir(self.input_path):
            if f.endswith(self.file_extension):
                file_names.append(f)
        df_final = pd.DataFrame()
        for file_name in tqdm(file_names):
            df = pd.read_csv(f"{self.input_path}/{file_name}",
                             sep=sep,
                             compression=compression,
                             dtype=object)
            df_final = pd.concat([df_final, df], ignore_index=True)
        return df_final

    @staticmethod
    def count_alleles(dataset: pd.DataFrame,
                      sample_ids: list[str],
                      major_allele_annotation: str = '0',
                      minor_allele_annotation: str = '1',
                      ) -> pd.DataFrame:
        """
        Returns a dataframe with major and minor allele counts per sample for a given dataset.
        Expected format of the dataset is it has a `sample_id` column with allele information in the format of
        `allele1 | allele2`.
        """

        allele_counts = pd.DataFrame(columns=['sample_id', 'major_count', 'minor_count'])
        allele_counts['sample_id'] = sample_ids
        allele_counts = allele_counts.set_index('sample_id')
        for sample_id in tqdm(sample_ids):
            allele_counts.loc[sample_id, 'major_count'] = dataset[sample_id].apply(
                lambda x: x.split('|').count(major_allele_annotation) if not pd.isnull(x) else np.nan).sum()
            allele_counts.loc[sample_id, 'minor_count'] = dataset[sample_id].apply(
                lambda x: x.split('|').count(minor_allele_annotation) if not pd.isnull(x) else np.nan).sum()
        return allele_counts

    def save_files(self,
                   dataset: pd.DataFrame,
                   sample_ids: list[str],
                   file_suffix: str = '.chr21.10000000_14999999.tsv.gz',
                   sep: str = '\t',
                   compression: str | dict = 'gzip',
                   ) -> None:
        """
        Save the dataset as 10 different files based on the last digit of the sample ID.
        Each dataset / file also contains all variant info columns.
        """

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        for i in tqdm(range(10)):
            selected_samples = [x for x in sample_ids if x.endswith(str(i))]
            selected_cols = VARIANT_INFO_COLUMNS + selected_samples
            df = dataset[selected_cols].copy()
            df.dropna(how='all', subset=selected_samples, inplace=True)
            output_file = self.output_path + '/' + str(i) + file_suffix
            df.to_csv(output_file, sep=sep, compression=compression, index=False)
