# Simons Foundation Coding Exercise

## Data input
Fifty (50) `.tsv.gz` files located under `exercise_input_data_public/` directory.

## Deliverables
### 1. `run.py`
Main script that does the following:
- Find all files ending with `.tsv.gz` under `exercise_input_data_public/` directory.
- Merge all files into a single data structure (`pd.DataFrame`):
  - Number of columns: 9 variant info columns + number of samples
  - Variant info columns: `#CHROM`, `POS`, `ID`, `REF`, `ALT`, `QUAL`, `FILTER`, `INFO` & `FORMAT`.
- Rename sample `HG10101` to `HG00101`.
- Create a new table with major and minor allele counts per sample.
- Aggregate and save the concatenated data as 10 different files based on the last digit of the sample ID 
under `output/` directory.

### 2. `allele_counts.tsv`
Major and minor allele count table for each sample (50 in total) with columns `sample_id`, `major_count` 
(annotated `0`) and `minor_count` (annotated `1`).

### 3. `tasks.sh`
Shell script to generate 5 smaller files from each of the 10 aggregated data files generated from `run.py` script 
under `output/` directory in chunks of 1Mpb each.

## Running the scripts
### Clone the repository
```shell
git clone https://github.com/lpchu/simons.git
```

### Setting up virtual environment
```shell
# inside simons/ directory after git clone
python -m venv .venv
source .venv/bin/activate
```

Optionally, install `poetry` with `pipx install poetry` (and then `export PATH="$HOME/.local/bin:$PATH"`)
if using `poetry` for package management.

### Install all dependencies
#### Using `pip`
```shell
pip install -r requirements.txt
```

#### Using `poetry`
```shell
poetry install
```

### Running `run.py`
```shell
python run.py
```
This will perform all the steps outlined above, writes out allele counts table to `allele_counts.tsv` at project root, 
and outputs 10 data files aggregated from original input data under `exercise_input_data_public/` based on the last
digit of the sample IDs to `output/` directory, `output/1.chr21.10000000_14999999.tsv.gz` for example. 
Each file also includes all variant info columns.

### Running `tasks.sh`
> [!WARNING]
> Must be run _after_ `run.py`. 

```shell
./tasks.sh output
```
This creates 5 new files from each of the 10 files deposited in `output/` directory
generated by `run.py` file in chunks of 1Mbp each and results in gzipped, tsv file named as 
`output/{last_digit}.chr21.{start}_{end}.tsv.gz`.

## Unittests
```shell
pytest tests/
```
