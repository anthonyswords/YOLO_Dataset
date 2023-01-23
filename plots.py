import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
import pandas as pd
import seaborn as sns
from os import remove, path
import webbrowser


def rectangle_YOLO(file_image, df, full_path_name_ext) -> None:
    """
    Desa una imatge inseint uns rectangles gràcies a l'inserció dels punts de les coordenades de la mateixa.
    :param file_image: ubicació + nom del fitxer d'imatge desitjada per obir-ho
    :param df: dataframe principal, filtrat per l'imatge desitjada amb els seus valors del rectangle
    :param full_path_name_ext: ubicació + nom fitxer inclòs, on desar el plot (s'ha d'incloure extensió dintre del nom)
    :return: desa un plot
    """
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
    plt.savefig(full_path_name_ext)
    print("[!] S'ha guardat un plot a la ruta: {}".format(full_path_name_ext))
    plt.close()


def plot_barplot(df: pd.DataFrame, x_axis: str, y_axis: str, title: str, full_path_name_ext: str,
                 ylabel: str = None, xlabel: str = None, rotation: int = None, legend: bool = True) -> None:
    """
    Desa un barplot
    :param df: dataframe principal
    :param x_axis: str nom de la columna on hi ha els valors de la x-axis
    :param y_axis: str nom de la columna on hi ha els valors de la y-axis
    :param title: str nom del títol del plot
    :param full_path_name_ext: ubicació + nom on desar el plot (s'ha d'incloure extensió)
    :param ylabel: str defult = None
    :param xlabel: str default = None
    :param rotation: int la rotació dels axis
    :param legend: bool default = True
    :return: save plot
    """
    df.plot(x=x_axis, y=y_axis, kind="bar", title=title, figsize=(8, 6), rot=rotation, legend=legend)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.savefig(full_path_name_ext)
    print("[!] S'ha guardat un plot a la ruta: {}".format(full_path_name_ext))
    plt.close()


def plot_sns_norm(df: pd.DataFrame, col_x: str, type_hue: str, title: str, full_path_name_ext: str) -> None:
    """
    Desa un plot d'una distribució normalitzada en format stack
    :param df: pd.DataFrame original
    :param col_x: str nom columna x axis
    :param type_hue: str nom columna agrupat pet colors
    :param title: str nom títol plot
    :param full_path_name_ext: path_to_file: ubicació + nom on desar el plot (s'ha d'incloure extensió)
    :return: sns displot save - return None
    """
    sns.displot(df, x=col_x, hue=type_hue, stat="density", multiple="stack")
    plt.title(title)
    plt.savefig(full_path_name_ext)
    print("[!] S'ha guardat un plot a la ruta: {}".format(full_path_name_ext))
    plt.close()


def plot_sns(df: pd.DataFrame, x: str, y: str, type_col: str, kind: str, title: str, full_path_name_ext: str) -> None:
    """
    Desa un plot de seaborn agrupat segons els colors
    :param df: pd.DataFrame
    :param x: str nom columna x-axis
    :param y: str nom columna y.axis
    :param type_col: str nom columna on els valors s'agrupen amb colors
    :param kind: str tipus de plot ('bar','line', etc. see in Doc seaborn)
    :param title: str nom title plot
    :param full_path_name_ext: ubicació + nom on desar el plot (s'ha d'incloure extensió)
    :return: desa plot sns
    """
    g = sns.catplot(x=x,
                    y=y,
                    hue=type_col,
                    data=df,
                    kind=kind)

    for ax in g.axes.ravel():
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                        va='center', xytext=(0, 10), textcoords='offset points')
    plt.title(title)
    plt.savefig(full_path_name_ext)
    print("[!] S'ha guardat un plot a la ruta: {}".format(full_path_name_ext))
    plt.close()


def plot_image(path_to_file: str) -> None:
    """
    Obre el fitxer imatge a través del navegador del sistema.
    :param path_to_file: ubicació + nom on desar el plot (s'ha d'incloure extensió)
    :return: Exe: open Firefox localserver: imatge.png
    """
    webbrowser.open(path_to_file)
