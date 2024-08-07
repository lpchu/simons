from src.allele_counter import AlleleCounter
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


def run():
    allele_counter = AlleleCounter(input_path='../exercise_input_data_public', output_path='../output')

    # find and merge all datasets into 1 df
    logger.info(f"Merging all files with extension {allele_counter.file_extension} under {allele_counter.input_path}...")
    allele_df = allele_counter.merge_dataset()

    # rename sample "HG10101" to "HG00101"
    logger.info(f"Renaming sample 'HG10101' to 'HG00101'...")
    allele_df.rename(columns={"HG10101": "HG00101"}, inplace=True)

    # count alleles for each sample
    sample_ids = [i for i in allele_df.columns if i.startswith('HG')]
    logger.info(f"Generating allele count dataframe for {len(sample_ids)} samples...")
    allele_count_df = allele_counter.count_alleles(dataset=allele_df, sample_ids=sample_ids)
    output_file_path = '../allele_counts.tsv'
    logger.info(f"Saving allele count dataframe to {output_file_path}")
    allele_count_df.to_csv(output_file_path, sep='\t', index=True)

    # aggregate and save data into chunks based on the last digit of the sample ID
    logger.info(f"Saving data as 10 different files based on the last digit of the sample ID under "
                f"{allele_counter.output_path}")
    allele_counter.save_files(dataset=allele_df, sample_ids=sample_ids)


if __name__ == '__main__':
    import time
    t0 = time.time()
    run()
    print(f"Finished processing in {(time.time() - t0)/60} minute(s).")
