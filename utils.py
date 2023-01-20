from os import listdir, getcwd, path, remove
from os.path import exists, join, isfile
import pandas as pd
import re

pd.set_option('display.max_columns', 10)


def read_files(full_path_name_file: str, title: list = None, delimiter: str = None, header: int = None) -> pd.DataFrame:
    """
    Retorna a DataFrame un arxiu txt o csv ubicat quelcom lloc indicat.
    :param full_path_name_file: string de l'ubicació i nom de l'arxiu inclòs
    :param title: llista amb els noms dels títols de les columnes (default=None)
    :param delimiter: string del separador/delimitadors (s'admet regex) (default=None)
    :param header: Número(s) de fila a utilitzar com a noms de columnes i l'inici de les dades. (default=None)
    :return: DataFrame
    """
    return pd.read_csv(full_path_name_file, names=title, sep=delimiter, header=header, engine='python')


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
    r = re.compile(r"^([0-7][0-9]{1}|[0-9]{1}|80)"
                   r"\s[0-1]{1}.\d+\s[0-1]{1}.\d+\s[0-1]{1}.\d+\s[0-1]{1}.\d+\s[0-1]{1}.\d+$")
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


def grouped_count_df(df: pd.DataFrame, list_column: list, action: str, sorting: bool = False, asc: bool = False,
                     ign_idx: bool = True) -> pd.DataFrame:
    """
    Retorna un df agrupat en funció de la llista de columnes. Es pot ordenar.
    :param df: DataFrame
    :param list_column: llista de columnes del fg
    :param action: columna nova agregada (Ex: 'count')
    :param sorting: si es vol ordenar (default=False)
    :param asc: si es vol de manera ascendent (default=False)
    :param ign_idx: si es vol ignorar index(default=True)
    :return: pd.DataFrame
    """
    df_grouped = df.groupby(list_column).size().reset_index(name=action)
    if sorting:
        return sort_df(df_grouped, action, asc, ign_idx)
    return df.groupby(list_column).size().reset_index(name=action)


def sort_df(df, by_col: str, asc: bool = False, ign_idx: bool = True):
    """
    Retorna un df ordenat segons els paràmetres
    :param df: DataFrame
    :param by_col: columna predominant
    :param asc: ascendent? (default=False)
    :param ign_idx: es vol ignorar el nou index després d'ordenar? (default=True)
    :return: pd.DataFrame
    """
    return df.sort_values(ascending=asc, by=by_col, ignore_index=ign_idx)


def get_dict_object_populars_byImage(df: pd.DataFrame, column_object: str, column_img: str) -> dict:
    """
    Retorna un diccionari del recompte dels valors populars de la columna i df objectes d'estudi passats com argument.
    El df en qüestió estará agrupat amb la columna noms d'imatge que ha d'incorporar el df i la columna object.
    Farem un recompte amb els valors únics atenent als criteris de popularitat mitjançant la columna agregada 'count'.
    :param df: DataFrame
    :param column_object: str de la columna on farem recompte dels seu valors segons la seva popularitat a cada imatge
    :param column_img: string de la columna del nom del fitxer imatge
    :return: diccionari
    Ex: {cars:5, truck:2} - Expl:'cars' ha sigut popular en 5 imatges i 'truck' en 2 imatges.
    """
    df_group = grouped_count_df(df, [column_img, column_object], 'count', True)
    dictObject = dict()
    for val_name_img in list(set(df[column_img])):
        list_key = get_list_index_popular_key(df_group, column_img, 'count', column_object, val_name_img)
        for key in list_key:
            if df_group[column_object].iloc[key] in dictObject:
                dictObject[df_group[column_object].iloc[key]] += 1
            else:
                dictObject[df_group[column_object].iloc[key]] = 1
    return dict(sorted(dictObject.items(), key=lambda item: item[1], reverse=True))


def get_list_index_popular_key(df: pd.DataFrame, col_img: str, col_agg: str, col_obj: str, value_name_img: str) -> list:
    """
    Obtenim una llista d'índex dels valors, que ha sigut popular en una imatge, de la columna d'objecte d'estudi del df.
    En aquesta funció s'implementa els criteris de popularitat.
    :param df: DataFrame
    :param col_img: columna dels noms de les imatges (Ex: name_image' )
    :param col_agg: columna de valors agregats (Ex: (str) 'count')
    :param col_obj: columna d'objecte d'estudi per fer recompte de la seva popularitat (Ex: (str) 'name' o 'id')
    :param value_name_img: String del nom de la imatge a analitzar (Ex: (str) berlin_xx_xx.jpg)
    :return: list
    Ex: ['124', '129'] on 124 és el 'car' i 129 és el truck: objectes populars a l'imatge berlin_xx_xx.jpg
    """
    df_filter = df[df[col_img] == value_name_img]
    # Recordar que el df està agrupat i, per tant, no pot haber valors duplicats a la columna objecte ('name' o 'id')
    if len(list(df_filter[col_obj])) <= 3:
        return df_filter[col_obj].index.tolist()
    else:
        return get_list_index_popular_freq(df_filter, col_agg)


def get_list_index_popular_freq(df: pd.DataFrame, col_freq: str, need_sort: bool = False) -> list:
    """
    Obtenim una llista d'índex dels valors, que ha sigut popular en una imatge, de la columna d'objecte d'estudi del df.
    Però, no obstant, únicament d'aquella imatge que tingui més de 3 objectes.
    :param df: pd.DataFrame
    :param col_freq: número de freqüències, prové d'una columna agregada (Ex: (str) 'count')
    :param need_sort: es vol ordenar el df segons la columna de freqüències? (default=False)
    :return: list
    Ex:['124','125','126','129'] objectes més populars d'una imatge: car,person,traffic light i truck
    """
    if need_sort:
        df = df.sort_values(col_freq)
        position = 0  # en quina posició de l'array ens trobem
        max_pos = 0  # en quina posició de l'array hem finalitzat quan complim amb una de les condicions següents
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
        return df[col_freq].iloc[:max_pos].index.tolist()  # tots els valors de l'array d'inici fins on hem finalitzat
    else:
        position = 0  # en quina posició de l'array ens trobem
        max_pos = 0  # en quina posició de l'array hem finalitzat quan complim amb una de les condicions següents
        for i in df[col_freq]:
            if position == 1 and max(df[col_freq]) == df[col_freq].iloc[position - 1]:  # enunciat 2.3.3
                if df[col_freq].iloc[position] == df[col_freq].iloc[position + 1]:
                    max_pos = position
            if position == 2 and max(df[col_freq]) >= df[col_freq].iloc[position - 1] and max_pos == 0:  # 2.3)
                if df[col_freq].iloc[position] == df[col_freq].iloc[position + 1]:  # enunciat 2.3.2
                    max_pos = position
                if df[col_freq].iloc[position] > df[col_freq].iloc[position + 1]:  # enunciat 2.3.1
                    max_pos = position + 1
            if i == max(df[col_freq]) and position > 2:  # enunciat 3.A
                max_pos = position + 1
            position += 1
        return df[col_freq].iloc[:max_pos].index.tolist()  # tots els valors de l'array d'inici fins on hem finalitzat


def replace_column(df: pd.DataFrame, column: str, pattern: str, sub: str, regex: bool = True) -> pd.DataFrame:
    """
    Retorna una columna on es modifica els valors que coincideixen amb el patró de regex per altres valors indicats.
    :param df: DataFrame
    :param column: columna a modificar
    :param pattern: patró a trobar a cada valor de la columna per ser objecte de modificació
    :param sub: valor a substituir
    :param regex: el patró és regex? (default = True)
    :return: DataFrame
    """
    return df.loc[:, column].str.replace(r'{0}'.format(pattern), r'{0}'.format(sub), regex=regex)


def df_img_obj_fraud(df: pd.DataFrame, pattern: str, sub: str, query: int,
                     col_obj: str = 'name', col_img: str = 'name_image', city_filter: str = 'zurich',
                     name_city_col: str = 'city') -> pd.DataFrame:
    """

    :param df:
    :param pattern:
    :param sub:
    :param query:
    :param col_obj:
    :param col_img:
    :param city_filter:
    :param name_city_col:
    :return:
    """
    df.loc[:, name_city_col] = replace_column(df, col_img, pattern, sub)
    list_may_fraud = grouped_count_df(df, [col_obj], 'count', True).query('count<{0}'.format(query))[col_obj].tolist()
    df_frauds = df[df[col_obj].isin(list_may_fraud)]
    return df_frauds[df_frauds[name_city_col] == city_filter].loc[:, [col_obj, col_img, name_city_col]]


def save_to_csv(df: pd.DataFrame, path_to_save: str, name_csv: str, header: bool = True, index: bool = False) -> None:
    """
    Desa un df com arxiu csv a la ruta indicada
    :param df: DataFrame
    :param path_to_save: ruta on desar l'arxiu csv
    :param name_csv: nom de l'arxiu csv
    :param header: desem amb la capçalera del df? (default=True)
    :param index: desem index com columna? (default=False)
    :return: None
    """
    if exists(join_path(path_to_save, name_csv)):
        remove(join_path(path_to_save, name_csv))
    df.to_csv(join_path(path_to_save, name_csv), header=header, index=index)
    print(
        f"[+] S'ha desat el df com arxiu \'{name_csv}\' a la ruta següent: {join_path(path_to_save, name_csv)}\n")
