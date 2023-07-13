import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def graphic_nb_photos_by_matrix(df: pd.DataFrame) -> None:
    # create horizontal bar chart
    ax = sns.barplot(x=list(df.Type.value_counts()), y=df.Type.value_counts().index.tolist(), orient='h')
    ax.bar_label(ax.containers[0], fmt='%d')
    sns.set(rc={'figure.figsize': (10, 5)}, font_scale=1.5)
    sns.set_style({'axes.facecolor': 'white', 'grid.color': '.8', 'font.family': 'Times New Roman'})
    plt.title('Number of photos by germ type', fontsize=16)

    # add axis labels
    plt.xlabel('Number of photos')
    plt.ylabel('Germ Type')
    plt.show()

def graphic_nb_samples_by_matrix(df: pd.DataFrame) -> None:
    data = {}
    for x in df.Type.value_counts().index.tolist():
        df_type = df[df.Type == x]
        data[x] = df_type["Colony number"].apply(lambda x: int(x)).sum()

    ax = sns.barplot(x=list(data.values()), y=["Total germa", "Lactic bacteria", "Enterobacteria"], orient='h')
    ax.bar_label(ax.containers[0], fmt='%d')
    sns.set(rc={'figure.figsize': (10, 5)}, font_scale=1.5)
    sns.set_style({'axes.facecolor': 'white', 'grid.color': '.8', 'font.family': 'Times New Roman'})
    plt.title('Number of bacterias by germ type', fontsize=16)

    # add axis labels
    plt.xlabel('Number of bacterias')
    plt.ylabel('Germ Type')
    plt.show()