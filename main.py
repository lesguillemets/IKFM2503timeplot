import pathlib
import polars as pl

DATA_DIR = "./data"

def main():
    # list of tsv files under data/
    original_tsvs = list(pathlib.Path(DATA_DIR).glob("*.tsv"))
    rt_csvs = list(pathlib.Path(DATA_DIR).glob('*.mov.bw.result.csv'))
    dat_files = []
    for tf in original_tsvs:
        corresponding = next(
                filter(
                    # あまりにひどいがこうせざるを得ないっぽい
                    lambda f: f.name.split('.')[0].split('-')[-1] == tf.stem.split('-')[-1],
                    rt_csvs
                    ),
                None)
        if corresponding is not None:
            dat_files.append((tf,corresponding))
    print(dat_files)

if __name__ == "__main__":
    main()
