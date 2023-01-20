from os import listdir, getcwd, path, remove
from os.path import exists, join, isfile
import pandas as pd
import re

pd.set_option('display.max_columns', 10)


def concat_list_df(list_df: list) -> pd.DataFrame:
    """
    Concatena una llista de Dataframes.
    :param list_df: la llista ha de contenir dataframes.
    :return: pd.DataFrame
    """
    return pd.concat(list_df, ignore_index=True)


def merge_df(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how: str = 'left', sort: bool = False) -> pd.DataFrame:
    """
    Unió de dos dataframes
    :param df1: DataFrame primer
    :param df2: DataFrame segon
    :param on: Nom de nivell de columna o índex per unir-se.
    :param how: {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘left’
    :param sort: Ordena les claus d'unió lexicogràficament, default False
    :return: pd.DataFrame
    """
    return df1.merge(df2, how=how, on=on, sort=sort)


def check_yolo(full_path_name_file) -> bool:
    """
    Comprova que té el format YOLO: enter entre 0-80 i 5 columnes de nombre flotants
    :param full_path_name_file:
    :return: bool
    """
    r = re.compile("^([0-7][0-9]{1}|[0-9]{1}|80)"
                   "\s[0-1]{1}.\d+\s[0-1]{1}.\d+\s[0-1]{1}.\d+\s[0-1]{1}.\d+\s[0-1]{1}.\d+$")
    with open(full_path_name_file) as f:
        for line in f:
            if not r.search(line):
                print(
                    "[+] Eliminarem l'arxiu %s del dataset perqué trobem que no compleix amb el format YOLO: "
                    "\n\t[·] %s" % (
                        full_path_name_file, line))
                return False
    return True


def get_path_files(main_project_path: str = None) -> str:
    """
    Aconseguir 3 paths dels arxius a treballar al dataset. Punt d'origen és la carpeta del projecte.
    :param main_project_path: inserir manualment la path on es troba la carpeta del projecte (inclòs)
    :return: path class_name.txt(str), path d'imatges(str) i path de labels(str)
    """
    # utilitzem getcwd() per evitar lectura de rutes en diferents sistemes operatius, entre d'altres mètodes OS
    if not main_project_path:
        return \
            path.join(getcwd(), "dataset_cities"), \
            path.join(getcwd(), "dataset_cities", "images"), \
            path.join(getcwd(), "dataset_cities", "labels")
    else:
        return \
            path.join(main_project_path, "dataset_cities"), \
            path.join(main_project_path, "dataset_cities", "images"), \
            path.join(main_project_path, "dataset_cities", "labels")


def join_path(path_begin: str, path_ending: str) -> str:
    """
    Concatena diversos components del camí amb exactament un separador de directoris ('/') al final d'aquest.
    :param path_begin: primer path ubicat
    :param path_ending: darrer path ubicat
    :return: str
    Exemple: 'my_path'+'my_text.csv' -> my_path/my_text.csv
    """
    return path.join(path_begin, path_ending)


def get_list_names_files_from_path(path_file: str = None) -> list:
    """
    Aconseguir una llista de tots els noms dels fitxers que hi hagi en la ruta
    :param path_file: la ruta on s'ubica els arxius desitjats
    :return: llista
    Exemple: /my_project/dataset_cities/ -> ['class_name.txt']
    """
    return sorted(filter(lambda x: isfile(join(path_file, x)),
                         listdir(path_file)))


def check_match_fileImage_fileLabel(list_files_from_labels: list, list_files_from_images: list, index: int) -> bool:
    """
    Comprova que dos llistes tinguin el mateix nom en el mateix index.
    :param list_files_from_labels: llista de text
    :param list_files_from_images: llist d'imatges
    :param index: index de la llista
    :return: bool
    """
    pattern = '^.*(?=.txt|.png)'
    if re.findall(pattern,
                  list_files_from_labels[index]) == re.findall(pattern,
                                                               list_files_from_images[index]):
        return True
    return False


def read_files(full_path_name_file: str, title: list, delimiter: str) -> pd.DataFrame:
    """
    Retorna a DataFrame un arxiu txt o csv ubicat quelcom lloc indicat.
    :param full_path_name_file:
    :param title:
    :param delimiter:
    :return:
    """
    df_file = pd.read_csv(full_path_name_file, names=title, sep=delimiter, header=None, engine='python')
    return df_file


def grouped_count_df(df: pd.DataFrame, list_column: list, action: str, sorting: bool = False, asc: bool = False,
                     ign_idx: bool = True):
    df_grouped = df.groupby(list_column).size().reset_index(name=action)
    if sorting:
        return sort_df(df_grouped, action, asc, ign_idx)
    return df.groupby(list_column).size().reset_index(name=action)


def sort_df(df, action: str, asc: bool = False, ign_idx: bool = True):
    return df.sort_values(ascending=asc, by=action, ignore_index=ign_idx)


def get_dict_object_populars_byImage(df: pd.DataFrame, column_object: str) -> dict:
    df_group = grouped_count_df(df, ['name_image', column_object], 'count', True)
    dictObject = dict()
    for val_name_img in list(set(df['name_image'])):
        list_key = get_list_index_popular_key(df_group, 'name_image', 'count', column_object, val_name_img)
        for key in list_key:
            if df_group[column_object].iloc[key] in dictObject:
                dictObject[df_group[column_object].iloc[key]] += 1
            else:
                dictObject[df_group[column_object].iloc[key]] = 1
    return dict(sorted(dictObject.items(), key=lambda item: item[1], reverse=True))


def get_list_index_popular_key(df: pd.DataFrame, col1: str, col_agg: str, col_obj: str, value_name_imag: str) -> str:
    df_filter = df[df[col1] == value_name_imag]
    # comentar que el DF està agrupat i, per tant, no pot haber valors duplicats a la columna objecte ('name' o 'id')
    if len(list(df_filter[col_obj])) <= 3:
        return df_filter[col_obj].index.tolist()
    else:
        return get_list_index_popular_freq(df_filter, col_agg)


def get_list_index_popular_freq(df: pd.DataFrame, col_freq: str, need_sort: bool = False) -> list:
    if need_sort:
        df = df.sort_values(col_freq)
        position = 0
        max_pos = 0
        for i in df[col_freq]:
            if position == 1 and max(df[col_freq]) == df[col_freq].iloc[position - 1]:
                if df[col_freq].iloc[position] == df[col_freq].iloc[position + 1]:
                    max_pos = position
            if position == 2 and max(df[col_freq]) >= df[col_freq].iloc[position - 1] and max_pos == 0:
                if df[col_freq].iloc[position] > df[col_freq].iloc[position + 1]:
                    max_pos = position + 1
                if df[col_freq].iloc[position] == df[col_freq].iloc[position + 1]:
                    max_pos = position
            if i == max(df[col_freq]) and position > 2:
                max_pos = position + 1
            position = position + 1
        return df[col_freq].iloc[:max_pos].index.tolist()
    else:
        position = 0
        max_pos = 0
        for i in df[col_freq]:
            if position == 1 and max(df[col_freq]) == df[col_freq].iloc[position - 1]:
                if df[col_freq].iloc[position] == df[col_freq].iloc[position + 1]:
                    max_pos = position
            if position == 2 and max(df[col_freq]) >= df[col_freq].iloc[position - 1] and max_pos == 0:
                if df[col_freq].iloc[position] > df[col_freq].iloc[position + 1]:
                    max_pos = position + 1
                if df[col_freq].iloc[position] == df[col_freq].iloc[position + 1]:
                    max_pos = position
            if i == max(df[col_freq]) and position > 2:
                max_pos = position + 1
            position += 1
        return df[col_freq].iloc[:max_pos].index.tolist()


def replace_column(df: pd.DataFrame, column: str, pattern: str, sub: str, regex: bool = True) -> pd.DataFrame:
    return df.loc[:, column].str.replace(r'{0}'.format(pattern), r'{0}'.format(sub), regex=regex)


def save_to_csv(df: pd.DataFrame, path_to_save: str, name_csv: str, header: bool = True, index: bool = False) -> None:
    if exists(join_path(path_to_save, name_csv)):
        remove(join_path(path_to_save, name_csv))
    df.to_csv(join_path(path_to_save, name_csv), header=header, index=index)


def read_csv(name_csv, path_to_read) -> pd.DataFrame:
    return pd.read_csv(join_path(path_to_read, name_csv))

