from pathlib import Path
from scipy.stats import f_oneway
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = Path("./data/use_for_plot/")

from load import load_reactiontimes


def plot_times(df: pl.DataFrame):
    emotions = range(5)
    fig, axs = plt.subplots(1, 5, figsize=(20, 5), sharey=True)

    lengths = []
    for ax, emotion in zip(axs, emotions):
        emotion_data = df.filter(pl.col('emotion') == emotion)
        lengths.append(len(emotion_data))
        ax.hist(emotion_data['total_dur'], bins=40)
        ax.set_title(f'Emotion {emotion}')
        ax.set_xlabel('total_dur')
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 15)
    assert all(length == lengths[0] for length in lengths)

    plt.tight_layout()
    plt.show(block=True)

def plot_viol_times(df: pl.DataFrame):
    fig, ax = plt.subplots()
    dat = df.filter(pl.col('emotion') < 5)
    sns.violinplot(x=dat['emotion'], y=dat['total_dur'], ax=ax)
    plt.tight_layout()
    plt.savefig('./plot/total_dur_by_emotions_all.png')
    plt.show(block=True)

def plot_viol_times_as_td(df: pl.DataFrame):
    fig, ax = plt.subplots()
    dat = df.filter(pl.col('emotion') < 5).filter(pl.col('is_td'))
    sns.violinplot(x=dat['emotion'] , y=dat['total_dur'], ax=ax)
    plt.tight_layout()
    plt.savefig('./plot/total_dur_by_emotions_td.png')
    plt.show(block=True)
    fig, ax = plt.subplots()
    dat = df.filter(pl.col('emotion') < 5).filter(pl.col('is_td').not_())
    sns.violinplot(x=dat['emotion'] , y=dat['total_dur'], ax=ax)
    plt.tight_layout()
    plt.savefig('./plot/total_dur_by_emotions_asd.png')
    plt.show(block=True)

def main():
    df = load_reactiontimes(DATA_DIR)
    plot_times(df)
    plot_viol_times(df)
    plot_viol_times_as_td(df)
    with pl.Config(tbl_cols=-1, tbl_rows=-1):
        print(df)


if __name__ == "__main__":
    main()
