import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
import seaborn as sns


def rectangle_YOLO(file_image, df):
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
    plt.suptitle('Exercici 3')
    plt.show()


def plot_barplot(df, x_axis, y_axis, title, ylabel=None, xlabel=None, rotation=None, legend=True ):
    """Plot data using a barplot."""
    df.plot(x=x_axis, y=y_axis, kind="bar", title=title, figsize=(8, 6), rot=rotation, legend=legend)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.show()


def plot_den_hist(df,x):
    plt.hist(x, density=True, color="green", label='Density', data=df)
    plt.legend()
    plt.show()


def plot_snsplot(df,x, y, type, kind, title_plot):
    g = sns.catplot(x=x,
                y=y,
                hue=type,
                data=df,
                kind=kind)

    for ax in g.axes.ravel():
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                        va='center', xytext=(0, 10), textcoords='offset points')
    plt.title(title_plot)
    plt.show()
