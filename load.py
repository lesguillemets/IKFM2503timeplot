from pathlib import Path
import pathlib
import polars as pl
import matplotlib.pyplot as plt


def load_clicks(data_dir: Path) -> pl.DataFrame:
    original_tsvs = list(data_dir.glob("*.tsv"))
    click_csvs = list(data_dir.glob('*.mov.clicks.csv'))
    dat_files = []
    for tf in original_tsvs:
        corresponding = next(
                filter(
                    # あまりにひどいがこうせざるを得ないっぽい
                    lambda f: f.name.split('.')[0].split('-')[-1] == tf.stem.split('-')[-1],
                    click_csvs
                    ),
                None)
        if corresponding is not None:
            dat_files.append((tf,corresponding))
    return clicks_to_df(dat_files)

def clicks_to_df(files: list[ tuple[Path,Path] ]) -> pl.DataFrame:
    loaded = pl.concat(map(lambda fl: load_orig_click_pair(fl[0], fl[1]), files))
    return loaded

def load_orig_click_pair(orig:Path, clicks:Path) -> pl.DataFrame:
    df_orig = pl.read_csv(orig, has_header=True, separator='\t').drop('x').drop('y')
    df_click = pl.read_csv(clicks, has_header=True, separator=',').rename({'i': 'index'})
    name = id_from_origfile(orig)
    joined = df_click.join(df_orig, on="index", how="inner").with_columns(pl.lit(name).alias("ID"))
    return joined

def load_reactiontimes(data_dir: Path) -> pl.DataFrame:
    original_tsvs = list(data_dir.glob("*.tsv"))
    rt_csvs = list(data_dir.glob('*.mov.reactiontimes.csv'))
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
    return rtf_to_df(dat_files)

def rtf_to_df(files: list[ tuple[Path,Path] ]) -> pl.DataFrame:
    loaded = pl.concat(map(lambda fl: load_orig_rtf_pair(fl[0], fl[1]), files))
    return loaded

def load_orig_rtf_pair(orig:Path, clicks:Path) -> pl.DataFrame:
    df_orig = pl.read_csv(orig, has_header=True, separator='\t').drop('x').drop('y')
    df_click = pl.read_csv(clicks, has_header=True, separator=',').rename({'i': 'index'})
    name = id_from_origfile(orig)
    joined = df_orig.join(df_click, on="index", how="left").with_columns(pl.lit(name).alias("ID"))
    return joined

def id_from_origfile(f:Path)-> str:
    return f.stem.split('-')[-1]


def on_main():
    """
    これで動さとか確認してるけど，基本的には
    このモジュールは import して使う想定です
    """
    p = pathlib.Path("./data/use_for_plot/")
    print(load_clicks(p))
    print(load_reactiontimes(p))


if __name__ == "__main__":
    on_main()

