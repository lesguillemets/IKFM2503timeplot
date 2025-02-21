from pathlib import Path
import matplotlib.pyplot as plt
import polars as pl
from load import load_reactiontimes


def plot_scatter(df, f=None, name=None):
    fig,ax = plt.subplots()
    if f is not None:
        df = df.filter(f)
    ax.scatter(df['init_dur'], df['total_dur'], s=5)
    ax.set_xlim(0,1400)
    ax.set_ylim(0,1700)
    fig.savefig(f"./plot/init_total_scatter_{name}.png")


def hist_clicks(df):
    bs=list(range(20))
    for (f, n) in [(pl.col("is_td"), "TD"),
                   (pl.col("is_td").not_(), "ASD") ]:
        fig,ax = plt.subplots()
        ax.hist(df.filter(f)['clicks'],
                label=n,
                bins=bs
                )
        ax.legend()
        ax.set_xticks(bs)
        fig.savefig(f"./plot/hist_for_clicks_{n}.png")

def scatter_main(df):
    for (f, n) in [(None,"all"),
                   (pl.col("is_td"), "td"),
                   (pl.col("is_td").not_(), "ASD")
                   ]:
        plot_scatter(df, f,n)

def main():
    df = load_reactiontimes(Path("./data/use_for_plot/"))
    hist_clicks(df)

if __name__ == "__main__":
    main()
