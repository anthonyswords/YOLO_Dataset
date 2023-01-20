"""
El programa principal on executem tots els mòduls.

Autor: Antoni Espadas Navarro

"""

from utils import *
from plots import rectangle_YOLO, plot_barplot, plot_den_hist, plot_sns


def main(main_project_path=None):
    print("######################### Exercici 1.1 + 1.2 #########################\n")
    path_class_name, path_image, path_label = get_path_files(main_project_path)
    list_files_from_labels = sorted(get_list_names_files_from_path(path_label))
    list_files_from_images = sorted(get_list_names_files_from_path(path_image))
    list_files_from_dataset = sorted(get_list_names_files_from_path(path_class_name))
    name_class_file = list_files_from_dataset[list_files_from_dataset.index("class_name.txt")]
    list_df_labelfiles: list = []
    title = ['id', 'coordenades_x_c', 'coordenades_y_c', 'coordenades_w', 'coordenades_h', 'prob_encertar']
    for index in range(len(list_files_from_labels)):
        if check_match_fileImage_fileLabel(list_files_from_labels, list_files_from_images, index):
            df_file = read_files(join_path(path_label, list_files_from_labels[index]), title, delimiter=' ')
            df_file['name_image'] = str(list_files_from_images[index])
            df_file['index_sorted'] = index
            list_df_labelfiles.append(df_file)
    df_labels = concat_list_df(list_df_labelfiles)
    class_df = read_files(join_path(path_class_name, name_class_file), title=['id', 'name'], delimiter=r"(?<=\d\s)")
    df_merged_ex1 = merge_df(df_labels, class_df, 'id')
    print(df_merged_ex1.head())
    print("\n[+] Resposta: en cas que tinguéssim milers d'arxius amb més d’un Gb cada arxiu "
          "hauriem de prescendir de la llibreria pandas i utilitzar un procediment "
          "de multiprocessament amb l'ús d'open() i utilitzar regex com patterns.")

    print("[+] Nota: en aquesta pràctica s'havia fet ús de multiprocessament, però degut a un error "
          "vaig d'haver canviar el codi.\n"
          "L'error en qüestió no solucionat: Unknown sequence number while processing queue")

    print("\n######################### Exercici 2 #########################\n")
    count = 0
    for i in range(len(list_files_from_labels)):
        if not check_yolo(join_path(path_label, list_files_from_labels[i])):
            count += 1
            df_merged_ex1.drop(df_merged_ex1[df_merged_ex1['index_sorted'] == i].index)
    if not count:
        print("Tots els fitxers compleixen amb el format YOLO")
    df_yolo_ex2 = df_merged_ex1.copy()

    print("\n######################### Exercici 3 #########################\n")
    for i in range(3):
        rectangle_YOLO(join_path(path_image, list_files_from_images[i]),
                       df_merged_ex1[df_merged_ex1['index_sorted'] == i],
                       join_path(path_class_name, 'Ex3_Fig{0}.png'.format(i)))
        print_image(join_path(path_class_name, 'Ex3_Fig{0}.png'.format(i)))

    print("[!] S'han obert les 3 primeres imatges (ordenades alfabèticament) amb els seu respectius rectangles\n")

    print("\n######################### Exercici 4 #########################\n")
    df_ex4 = df_yolo_ex2[df_yolo_ex2['prob_encertar'] > 0.4]
    print("[!] S'han escollit els objectes que tinguin una confiança major a 0.4 i són candidats YOLO.\n")

    print("\n######################### Exercici 4.1 #########################\n")
    df_grouped_id = grouped_count_df(df_ex4, ['id'], 'count', True)
    df_grouped_name = grouped_count_df(df_ex4, ['name'], 'count', True)
    print(df_grouped_id.head(5), "\n")
    print(df_grouped_name.head(5))
    plot_barplot(df_grouped_name, 'name', 'count', "Número total d'objectes de cada clase",
                 join_path(path_class_name, 'Ex4_1Fig{0}.png'.format(1)))
    print_image(join_path(path_class_name, 'Ex4_1Fig{0}.png'.format(1)))
    print("\n[!] S'ha obert una gràfica de tipus barres amb el número total d'objectes de cada clase\n")

    print("\n######################### Exercici 4.2 #########################\n")
    top_5 = df_ex4[df_ex4.name.isin(list(df_grouped_name['name'].head(5)))]
    plot_den_hist(top_5[['name', 'name_image']], "name", join_path(path_class_name, 'Ex4_2Fig{0}.png'.format(1)))
    print_image(join_path(path_class_name, 'Ex4_2Fig{0}.png'.format(1)))
    print("[!] S'ha obert un histograma normalitzat de tipus barres per veure les distribucions per objecte\n")

    print("\n######################### Exercici 4.3 #########################\n")
    df_grouped_name['mean_obj_imatges'] = df_grouped_name['count'] / len(set(df_ex4['index_sorted']))
    print("[+] Resposta: En aquest exercici, hem agafat el número d'ocurrències total de cada objecte i "
          "l'hem dividit entre el nombre total d'imatges existents úniques, per tant, tenim el següent resultat: "
          "\n{0}\nAixò vol dir que, per exemple, "
          "l'objecte 'car' apareixerà ~7 vegades per imatge".format(df_grouped_name))

    print("\n######################### Exercici 4.4 #########################\n")
    print(".a) Crear una funció que donat el dataframe us retorni un diccionari ordenat segons popularitat "
          "de l'objecte on com a claus tinguem tots els possibles labels o objectes que apareixen "
          "al dataset amb el que hem treballat des de l'exercici 3.\n")
    print(get_dict_object_populars_byImage(df_ex4, 'name'))
    print(df_grouped_name.head(5))

    print("\n.b) Coincideixen els tres elements més populars per imatge amb els més populars dins del dataset?\n")
    print("[+] Resposta: Sí, ens ha sortit els 3 elements més populars per imatge amb els més populars del dataset.\n"
          "Un exemple d'un possible cas on això no passaria rau en una distribució més uniforme on no hi hauria un\n"
          "desequilibri/desbalanceig en el nombre de mostres en la resta de variables que tenen poc pes.\n"
          "De fet, si ens fixem en traffic_light, trucj i bicycle hi ha diferenciació, ja que són variables\n"
          "amb nombre de mostres semblants i dona lloc al fet que certes imatges no sigui objecte de popularitat.\n")

    print("\n######################### Exercici 5 #########################\n")
    df_ex5 = df_ex4.copy()
    df_ex5['year'] = replace_column(df_ex5, 'name_image', r'(\w+_\d+_\w+-\d+-)|(.png|.txt)', '')
    df_ex5['city'] = replace_column(df_ex5, 'name_image', '([_].*$)', '')
    df_ex5_group = grouped_count_df(df_ex5, ['year', 'city', 'name'], 'count', True)
    df_ex5_group_filter = df_ex5_group[df_ex5_group['name'] == 'car']
    print(df_ex5_group_filter)
    tit_ex5 = 'El número de cotxes per any, per cada ciutat'
    plot_sns(df_ex5_group_filter, 'year', 'count', 'city', 'bar', tit_ex5, join_path(path_class_name, 'Ex5Fig.png'))
    print_image(join_path(path_class_name, 'Ex5Fig.png'))
    print("[!] S'ha obert un plot de tipus barres de seaborn per veure el número de cotxes per any, per cada ciutat\n")

    print("\n######################### Exercici 6 #########################\n")
    df_ex6 = df_ex4.copy()
    df_ex6['city'] = replace_column(df_ex6, 'name_image', '([_].*$)', '')
    list_possible_fraud = grouped_count_df(df_ex6, ['name'], 'count', True).query('count<5')['name'].tolist()
    df_frauds = df_ex6[df_ex6['name'].isin(list_possible_fraud)]
    df_frauds_filter = df_frauds[df_frauds['city'] == 'zurich'].loc[:, ['name', 'name_image', 'city']]
    print("\n [+] Resposta: He fet un mètode senzill a causa del temps de planificació per l'entrega de la PAC.\n"
          "Primerament, hem fet modificacions per cercar nom de les ciutats dels arxius.\n"
          "Seguidament, hem filtrat per un nombre petit (5) gràcies a la seva distribució analitzada anteriorment.\n"
          "Observem resultats i raonem que cobri sentit, per exemple, surt a la vista que una imatge\n"
          "contingui una girafa 4 cops únicament és motiu d'exclusió sumat de la poca popularitat, entre d'altres.\n"
          "Pot ser que, en la llista d'infiltrats, hagi de ser exclosa d'aquesta, però és una minoria que\n"
          "no afectaria gran escala al nostre model futur a predir."
          "Una altra opció podria ser observar el tamany de les imatges i treure'n conclusions.\n")
    list_frauds = df_frauds_filter['name_image'].tolist()

    print("\n######################### Exercici 7 #########################\n")
    df_ex7 = df_ex4.copy()
    df_ex7['city'] = replace_column(df_ex7, 'name_image', '([_].*$)', '')
    df_ex7['year'] = replace_column(df_ex7, 'name_image', r'(\w+_\d+_\w+-\d+-)|(.png|.txt)', '')
    df_ex7['is_city'] = True
    list_filter_object = ['car', 'traffic light', 'person']
    df_filter_object = df_ex7[df_ex7['name'].isin(list_filter_object)]
    df_filter_object.loc[df_filter_object['name_image'].isin(list_frauds), 'is_city'] = False
    df_csv = (grouped_count_df(df_filter_object, ['name_image',
                                                  'city',
                                                  'year',
                                                  'is_city',
                                                  'name'], 'count', True).sort_values('name_image'))
    save_to_csv(df_csv, path_class_name, 'dataset_cities.csv')
    df_show = read_csv('dataset_cities.csv', path_class_name)
    print("[+]Finalment, desarem l'arxiu com 'dataset_cities.csv' a la ruta següent: {}\n".format(path_class_name))
    print("\n Previsualitzem l'arxiu en qüestió:")
    print("\nColumnes:{}\n".format(df_show.columns))
    print(df_show.head())


if __name__ == '__main__':
    main()
