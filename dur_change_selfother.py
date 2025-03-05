from load import load_reactiontimes

from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = Path("./data/use_for_plot/")



def plot_avg_total_dur_selfother(df: pl.DataFrame):
    # Calculate the average total_dur for each index over participants
    (fig, axes) = plt.subplots(3, 2, figsize=(18, 15), sharey=True)
    for (cond, i) in zip((None, True, False), range(3)):
        for self_other in range(2):
            ax = axes[i,self_other]
            the_data = (df if cond is None else df.filter(pl.col('is_td') == cond)).filter(pl.col('index') > 3).filter(pl.col('condition2') == self_other)
            avg_total_dur = the_data.group_by('index').agg(pl.mean('total_dur').alias('avg_total_dur')).sort('index')
            print(avg_total_dur)
            ax.plot(avg_total_dur['index'], avg_total_dur['avg_total_dur'], label='Average Total Duration', color={None:"blue", True:"green", False:"orange"  }[cond])
            for index in avg_total_dur['index']:
                actual_durs = the_data.filter(pl.col('index') == index)['total_dur']
                ax.scatter([index] * len(actual_durs), actual_durs, color='purple', alpha=0.5)
            ax.set_xlabel('Index')
            ax.set_ylabel('Total Duration')
            ax.set_title( { None: "all", True: "TD", False: "ASD" }[cond] + "-" + ["self","other"][self_other])
            ax.legend()
    plt.tight_layout()
    plt.savefig('./plot/avg_total_dur_self_other.png')
    plt.show(block=True)

if __name__ == "__main__":
    df = load_reactiontimes(DATA_DIR)
    plot_avg_total_dur_selfother(df)
