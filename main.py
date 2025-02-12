import pathlib
import polars as pl
import matplotlib.pyplot as plt

DATA_DIR = "./data"

DEBUGS = {'load': True}

def main():
    df = load()
    plot(df)


def load():
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
    ids = map(lambda f: f.stem.split('-')[-1], original_tsvs)
    dat = []
    # load each pair of tsv/csv, and join them column-wise
    for (orig, times) in dat_files:
        name = orig.stem.split('-')[-1]
        orig_df = pl.read_csv(orig, has_header=True, separator='\t')
        times_df = pl.read_csv(times, has_header=True, separator=',')
        joined = pl.concat([orig_df, times_df], how="horizontal")
        joined = joined.with_columns(pl.lit(name).alias("ID"))
        dat.append(joined)
    df = pl.concat(dat)
    if (DEBUGS['load']):
        with pl.Config(tbl_cols=-1, tbl_rows=-1):
            print(df)
    return df

def plot(df: pl.DataFrame):
    original_tsvs = list(pathlib.Path(DATA_DIR).glob("*.tsv"))
    ids = map(lambda f: f.stem.split('-')[-1], original_tsvs)
    fig = plt.figure()
    ax = fig.subplots()
    for name in ids:
        the_data = df.filter( pl.col('ID') == name)
        ax.plot( the_data['i'], the_data['dur_frames'], label=name)
    ax.legend()
    plt.show()



if __name__ == "__main__":
    main()
