from load import load_reactiontimes

from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = Path("./data/use_for_plot/")



def plot_time_participants(df: pl.DataFrame):
    ids = df.select(pl.col('ID')).unique().to_series().to_list()
    print(ids)
    num_rows = (len(ids) + 2) // 3
    (fig, axes) = plt.subplots(num_rows, 3, figsize=(18, 5 * num_rows), sharey=True)
    axes = axes.flatten()
    sorted_ids = sorted(ids, key=lambda x: df.filter(pl.col('ID') == x)['is_td'][0])
    for (ax, name) in zip(axes, sorted_ids):
        the_data = df.filter(pl.col('ID') == name).filter(pl.col('index') > 3)
        color = 'green' if the_data['is_td'][0] else 'orange'
        ax.plot(the_data['index'], the_data['total_dur'], label=name, color=color)
        ax.set_title(name)
        ax.set_ylabel('total-dur')
        ax.label_outer()
    plt.tight_layout()
    plt.savefig('./plot/time_change_par_participants.png')
    plt.show(block=True)


if __name__ == "__main__":
    df = load_reactiontimes(DATA_DIR)
    plot_time_participants(df)
