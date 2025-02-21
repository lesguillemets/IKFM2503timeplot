from pathlib import Path
import matplotlib.pyplot as plt
import polars as pl
from load import load_reactiontimes


def plot_scatter(df, f=None, name=None):
    fig,ax = plt.subplots()
    if f is not None:
        df = df.filter(f)
    ax.scatter(df['init_dur'], df['total_dur'], s=20)
    fig.savefig(f"./plot/init_total_scatter_{name}.png")



def main():
    df = load_reactiontimes(Path("./data/use_for_plot/"))
    plot_scatter(df,  None, "all")

if __name__ == "__main__":
    main()
