"""
El programa principal on executem tots els mòduls.

Autor: Antoni Espadas Navarro

"""
from utils import *


def main(main_project_path=None):
    path_class_name, path_image , path_label = get_path_files(main_project_path)
    list_files_from_labels = get_list_names_files_from_path(path_label)
    list_files_from_images = get_list_names_files_from_path(path_image)
    name_class_file = get_list_names_files_from_path(path_class_name)[1]
    list_df_labelfiles: list = []
    title = ['id','coordenades_x_c','coordenades_y_c','coordenades_w','coordenades_h','prob_encertar']
    for index in range(len(list_files_from_labels)):
        if check_match_fileImage_fileLabel(list_files_from_labels, list_files_from_images, index):
            df_file = read_files(path_label+list_files_from_labels[index], title)
            df_file['name_image'] = str(list_files_from_images[index])
            df_file['index_sorted'] = index
            list_df_labelfiles.append(df_file)
    df_labels = concat_list_df(list_df_labelfiles)
    class_df = read_files(path_class_name + name_class_file, title=['id', 'class_name'])
    df_merged = merge_df(df_labels, class_df, 'id')
    print("######################### Exercici 1.1 + 1.2 #########################\n")
    print(df_merged.head())
    print("\nResposta: en cas que tinguéssim milers d'arxius amb més d’un Gb cada arxiu"
    " hauréem de prescendir de la llibreria pandas i utilitzar un procediment de"
          " multiprocessament amb l'ús d'open() i utilitzar regex com patterns")

    for i in range(len(set(df_merged['index_sorted']))):
        for indice_fila, fila in df_merged.query(f'index_sorted == {i}')[0:6].iterrows():
            print(fila)

    for index in range(len(list_files_from_labels)):
        if check_yolo(path_label+list_files_from_labels[index]):



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

