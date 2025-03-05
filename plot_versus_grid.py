from load import load_reactiontimes

from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = Path("./data/use_for_plot/")

def plot_total_dur_by_valence(df:pl.DataFrame, c:str):
    (fig, axes) = plt.subplots(3, 3, figsize=(18, 15), sharey=True)
    for (cond, i) in zip((None, True, False), range(3)):
        for (j, self_other_all) in enumerate((0,1,None)):
            ax = axes[i,j]
            the_data = (df if cond is None else df.filter(pl.col('is_td') == cond)).filter(pl.col('index') > 3)
            if self_other_all is not None:
                the_data = the_data.filter(pl.col('condition2') == self_other_all)
            with pl.Config(tbl_cols=-1, tbl_rows=-1):
                print(the_data)
            col = { 'Valence': 'final_x', 'Arousal': 'final_y', 'Max': 'final_max'}[c]
            the_data = the_data.with_columns((pl.col('final_x').abs()).alias('final_abs_x'))
            the_data = the_data.with_columns((pl.col('final_y').abs()).alias('final_abs_y'))
            the_data = the_data.with_columns(pl.max_horizontal(['final_abs_x', 'final_abs_y']).alias('final_max'))
            ax.scatter(x=the_data[col], y=the_data['total_dur'], alpha=0.3, color={None:"blue", True:"green", False:"orange"  }[cond])
            ax.set_xlabel(c)
            if c == 'Max':
                ax.set_xlim(0,5)
            else:
                ax.set_xlim(-5,5)
            ax.set_ylabel('Total Duration')
            ax.set_title( { None: "all", True: "TD", False: "ASD" }[cond] + "-" + ["self","other", "both"][j])
            ax.legend()
    plt.tight_layout()
    plt.savefig(f'./plot/total_dur_by_{c}.png')
    plt.show(block=True)

def plot_viol_total_dur_by_valence(df:pl.DataFrame, c:str):
    (fig, axes) = plt.subplots(3, 3, figsize=(18, 15), sharey=True)
    for (cond, i) in zip((None, True, False), range(3)):
        for (j, self_other_all) in enumerate((0,1,None)):
            ax = axes[i,j]
            the_data = (df if cond is None else df.filter(pl.col('is_td') == cond)).filter(pl.col('index') > 3)
            if self_other_all is not None:
                the_data = the_data.filter(pl.col('condition2') == self_other_all)
            with pl.Config(tbl_cols=-1, tbl_rows=-1):
                print(the_data)
            col = { 'Valence': 'final_x', 'Arousal': 'final_y', 'Max': 'final_max'}[c]
            the_data = the_data.with_columns((pl.col('final_x').abs()).alias('final_abs_x'))
            the_data = the_data.with_columns((pl.col('final_y').abs()).alias('final_abs_y'))
            the_data = the_data.with_columns(pl.max_horizontal(['final_abs_x', 'final_abs_y']).alias('final_max'))
            sns.violinplot(ax=ax, x=the_data[col], y=the_data['total_dur'], inner=None, color={None:"blue", True:"green", False:"orange"}[cond])
            ax.set_xlabel(c)
            ax.set_ylabel('Total Duration')
            ax.set_title( { None: "all", True: "TD", False: "ASD" }[cond] + "-" + ["self","other", "both"][j])
            ax.legend()
    plt.tight_layout()
    plt.savefig(f'./plot/viol_total_dur_by_{c}.png')
    plt.show(block=True)

if __name__ == "__main__":
    df = load_reactiontimes(DATA_DIR)
    plot_total_dur_by_valence(df, 'Valence')
    plot_total_dur_by_valence(df, 'Arousal')
    plot_total_dur_by_valence(df, 'Max')
#    plot_viol_total_dur_by_valence(df, 'Valence')
#    plot_viol_total_dur_by_valence(df, 'Arousal')
#    plot_viol_total_dur_by_valence(df, 'Max')

