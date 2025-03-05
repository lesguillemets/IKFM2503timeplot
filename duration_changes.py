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

def plot_avg_total_dur(df: pl.DataFrame):
    # Calculate the average total_dur for each index over participants
    for cond in (True, False, None):
        the_data = (df if cond is None else df.filter(pl.col('is_td') == cond)).filter(pl.col('index') > 3)
        avg_total_dur = the_data.group_by('index').agg(pl.mean('total_dur').alias('avg_total_dur')).sort('index')
        print(avg_total_dur)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(avg_total_dur['index'], avg_total_dur['avg_total_dur'], label='Average Total Duration', color='blue')
        for index in avg_total_dur['index']:
            actual_durs = the_data.filter(pl.col('index') == index)['total_dur']
            ax.scatter([index] * len(actual_durs), actual_durs, color='red', alpha=0.5)
        ax.set_xlabel('Index')
        ax.set_ylabel('Total Duration')
        ax.legend()
        plt.tight_layout()
        plt.savefig('./plot/avg_total_dur.png')
        plt.show(block=True)

if __name__ == "__main__":
    df = load_reactiontimes(DATA_DIR)
    plot_avg_total_dur(df)
    plot_time_participants(df)
