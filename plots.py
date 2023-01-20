import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
import seaborn as sns
from os import remove, path


def rectangle_YOLO(file_image, df, full_path_name_ext):
    W = 2048
    H = 1024
    img = image.imread(file_image)
    figure, ax = plt.subplots(num="Exercici 3")
    W_x = df[['coordenades_x_c', 'coordenades_w']].mul(W, axis=1).reset_index()
    H_y = df[['coordenades_y_c', 'coordenades_h']].mul(H, axis=1).reset_index()
    list_rect = [patches.Rectangle(((int(W_x.loc[i, 'coordenades_x_c'] - (W_x.loc[i, 'coordenades_w'] / 2))),
                                    (int(H_y.loc[i, 'coordenades_y_c'] - (H_y.loc[i, 'coordenades_h'] / 2)))),
                                   (W_x.loc[i, 'coordenades_w']),
                                   (H_y.loc[i, 'coordenades_h']), edgecolor='r', facecolor="none") for i in
                 range(len(df.index))]
    ax.imshow(img)
    for rect in list_rect:
        ax.add_patch(rect)
    plt.title(set(df['name_image']))
    if path.exists(full_path_name_ext):
        remove(full_path_name_ext)
    print("[!] S'ha guardat una imatge a la ruta: {}".format(full_path_name_ext))
    plt.savefig(full_path_name_ext)
    plt.clf()


def plot_barplot(df, x_axis, y_axis, title, full_path_name_ext: str,
                 ylabel=None, xlabel=None, rotation=None, legend=True):
    """Plot data using a barplot."""
    df.plot(x=x_axis, y=y_axis, kind="bar", title=title, figsize=(8, 6), rot=rotation, legend=legend)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.savefig(full_path_name_ext)
    plt.clf()


def plot_den_hist(df, x, full_path_name_ext):
    plt.hist(x, density=True, color="green", label='Density', data=df)
    plt.legend()
    plt.savefig(full_path_name_ext)
    plt.clf()


def plot_sns(df, x, y, type_col, kind, title_plot, full_path_name_ext):
    g = sns.catplot(x=x,
                    y=y,
                    hue=type_col,
                    data=df,
                    kind=kind)

    for ax in g.axes.ravel():
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                        va='center', xytext=(0, 10), textcoords='offset points')
    plt.title(title_plot)
    plt.savefig(full_path_name_ext)
    plt.clf()
