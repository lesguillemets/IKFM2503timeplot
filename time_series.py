from pathlib import Path
from scipy.stats import f_oneway
import polars as pl
import matplotlib.pyplot as plt

DATA_DIR = Path("./data/use_for_plot/")

from load import load_reactiontimes


def plot_times(df: pl.DataFrame):
    emotions = range(5)
    fig, axs = plt.subplots(1, 5, figsize=(20, 5), sharey=True)

    lengths = []
    for ax, emotion in zip(axs, emotions):
		emotion_data = df.filter(pl.col('emotion') == emotion)
		lengths.push(len(emotion_data))
        ax.hist(emotion_data['total_dur'], bins=40)
        ax.set_title(f'Emotion {emotion}')
        ax.set_xlabel('total_dur')
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 15)
	assert all(length == lengths[0] for length in lengths)

    plt.tight_layout()
    plt.show(block=True)

def main():
    df = load_reactiontimes(DATA_DIR)
    plot_times(df)
    with pl.Config(tbl_cols=-1, tbl_rows=-1):
        print(df)


if __name__ == "__main__":
    main()
