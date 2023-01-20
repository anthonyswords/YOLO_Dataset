"""
Aquest mòdul és el programa principal on executem tots la resta de mòduls.
El codi està dissenyat a partir del dataset_cities originalment descarregat en la PAC 4.
No cal inserir cap argument per executar el codi
No obstant, opcionalment, podem inserir manualment la ruta, on es localitza el projecte, al argument main().

Activitat: PAC 4
Autor: Antoni Espadas Navarro
Data: 23/01/2023
"""

from utils import *
from plots import rectangle_YOLO, plot_barplot, plot_den_hist, plot_sns, plot_image


def main(main_project_path=None):
    print("######################### Exercici 1.1 #########################\n")
    print("[·] Mostreu per pantalla les primeres files del dataframe:\n")
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

    print("\n######################### Exercici 1.2 #########################\n")
    print("[·] En aquest cas tenim poques imatges, però en un cas realista es podrien tenir moltissimes imatges\n"
          "per analitzar. Si tinguessiu milers d'arxius amb més d’un Gb cada arxiu com ho farieu?:\n")
    print("[+] Resposta: en cas que tinguéssim milers d'arxius amb més d’un Gb cada arxiu "
          "hauriem de prescendir de la llibreria pandas. \nUtilitzaríem un procediment "
          "de multiprocessament(per agilitzar rendiment) amb l'ús de llibreria open() utilitzant regex com patterns.")
    print("[+] Nota: en aquesta pràctica s'havia fet ús de multiprocessament, però degut a un error "
          "vaig d'haver canviar el codi.\n"
          " <<L'error en qüestió no solucionat: Unknown sequence number while processing queue>>\n")

    print("\n\n######################### Exercici 2 #########################\n")
    print("[·] Mostreu per pantalla una llista del nom dels arxius que no segueixen el format,"
          "\n i si fos el cas mostrar missatge de que no se n'ha trobat cap:\n")
    count: int = 0
    for i in range(len(list_files_from_labels)):
        if not check_yolo(join_path(path_label, list_files_from_labels[i])):
            count += 1
            df_merged_ex1.drop(df_merged_ex1[df_merged_ex1['index_sorted'] == i].index)
    if not count:
        print("Tots els fitxers compleixen amb el format YOLO")
    df_yolo_ex2 = df_merged_ex1.copy()

    print("\n\n######################### Exercici 3 #########################\n")
    print("[·] Presenteu la visualització d'aquestes tres imatges amb els contorns dels objectes detectats:\n")
    for i in range(3):
        rectangle_YOLO(join_path(path_image, list_files_from_images[i]),
                       df_merged_ex1[df_merged_ex1['index_sorted'] == i],
                       join_path(path_class_name, 'Ex3_Fig{0}.png'.format(i)))
        plot_image(join_path(path_class_name, 'Ex3_Fig{0}.png'.format(i)))
    print("[!] S'han obert les 3 primeres imatges (ordenades alfabèticament) amb els seu respectius rectangles\n")

    print("\n\n######################### Exercici 4 #########################\n")
    df_ex4 = df_yolo_ex2[df_yolo_ex2['prob_encertar'] > 0.4]
    print("[!] S'han escollit els objectes que tinguin una confiança major a 0.4 i són candidats YOLO.\n")

    print("\n######################### Exercici 4.1 #########################\n")
    print("[·] Mostreu per pantalla els identificadors i noms dels 5 objectes que "
          "\napareixen més cops en tot el dataset i quants cops hi apareixen:\n")
    df_grouped_id = grouped_count_df(df_ex4, ['id'], 'count', True)
    df_grouped_name = grouped_count_df(df_ex4, ['name'], 'count', True)
    print(df_grouped_id.head(5), "\n")
    print(df_grouped_name.head(5))
    print("\n[·] Mostreu una gràfica de tipus barres amb el número total d'objectes de cada clase:\n")
    plot_barplot(df_grouped_name, 'name', 'count', "Número total d'objectes de cada clase",
                 join_path(path_class_name, 'Ex4_1Fig{0}.png'.format(1)))
    plot_image(join_path(path_class_name, 'Ex4_1Fig{0}.png'.format(1)))
    print("\n[!] S'ha obert una gràfica de tipus barres amb el número total d'objectes de cada clase\n")

    print("\n######################### Exercici 4.2 #########################\n")
    print("[·] Mostreu en un sol gráfic les distribucions per objecte trobades per tal de comparar-les (feu servir \n"
          "histogrames normalitzats):\n")
    top_5 = df_ex4[df_ex4.name.isin(list(df_grouped_name['name'].head(5)))]
    plot_den_hist(top_5[['name', 'name_image']], "name", join_path(path_class_name, 'Ex4_2Fig{0}.png'.format(1)))
    plot_image(join_path(path_class_name, 'Ex4_2Fig{0}.png'.format(1)))
    print("[!] S'ha obert un histograma normalitzat de tipus barres per veure les distribucions per objecte\n")

    print("\n######################### Exercici 4.3 #########################\n")
    print("[·] Quin és el nombre mig d'objectes totals per imatge?\n"
          "Mostrar per panalla el resultat degudament explicat i formatat:\n")
    df_grouped_name['mean_obj_imatges'] = df_grouped_name['count'] / len(set(df_ex4['index_sorted']))
    print("[+] Resposta: en aquest exercici, s'ha agafat el número d'ocurrències total de cada objecte i "
          "s'ha dividit entre el nombre total d'imatges existents úniques, per tant, tenim el següent resultat: "
          "\n{0}\nAixò vol dir que, per exemple, "
          "l'objecte 'car' apareixerà ~7 vegades per imatge".format(df_grouped_name))

    print("\n######################### Exercici 4.4 #########################\n")
    print("[·] Volem saber quins són els tres elements més populars per imatge.\n"
          "Per definir els elements més populars per imatge s'ha creat una casuística \n"
          "a seguir (que es detalla al final de l'enunciat). Us demanem:\n")
    print(".a) Crear una funció que donat el dataframe us retorni un diccionari ordenat segons popularitat \n"
          "de l'objecte on com a claus tinguem tots els possibles labels o objectes que apareixen |n"
          "al dataset amb el que s'ha treballat des de l'exercici 3.\n")
    print(get_dict_object_populars_byImage(df_ex4, 'name', 'name_image'))
    print(df_grouped_name.head(5))

    print("\n.b) Coincideixen els tres elements més populars per imatge amb els més populars dins del dataset?\n")
    print("[+] Resposta: Sí, ens ha sortit els 3 elements més populars per imatge amb els més populars del dataset.\n"
          "Un exemple d'un possible cas on això no passaria rau en una distribució més uniforme on no hi hauria un\n"
          "desequilibri/desbalanceig en el nombre de mostres en la resta de variables que tenen poc pes.\n"
          "De fet, si ens fixem en traffic_light, trucj i bicycle hi ha diferenciació, ja que són variables\n"
          "amb nombre de mostres semblants i dona lloc al fet que certes imatges no sigui objecte de popularitat.\n")

    print("\n\n######################### Exercici 5 #########################\n")
    print("[·] Representa gràficament i mostra per pantalla el número de cotxes per any, per cada ciutat.\n"
          "Representa-ho en una sola gràfica on apareguin els resultats de totes les ciutats. \n")
    df_ex5 = df_ex4.copy()
    df_ex5.loc[:, 'year'] = replace_column(df_ex5, 'name_image', r'(\w+_\d+_\w+-\d+-)|(.png|.txt)', '')
    df_ex5.loc[:, 'city'] = replace_column(df_ex5, 'name_image', '([_].*$)', '')
    df_ex5_group = grouped_count_df(df_ex5, ['year', 'city', 'name'], 'count', True)
    df_ex5_group_filter = df_ex5_group[df_ex5_group['name'] == 'car']
    print(df_ex5_group_filter)
    tit_ex5 = 'El número de cotxes per any, per cada ciutat'
    plot_sns(df_ex5_group_filter, 'year', 'count', 'city', 'bar', tit_ex5, join_path(path_class_name, 'Ex5Fig.png'))
    plot_image(join_path(path_class_name, 'Ex5Fig.png'))
    print("[!] S'ha obert un plot de tipus barres de seaborn per veure el número de cotxes per any, per cada ciutat\n")

    print("\n######################### Exercici 6 #########################\n")
    print("[·] Dissenya una funció que sigui capaç d'identificar les imatges que no pertanyin a la"
          " ciutat de la forma més automatitzada possible.\n"
          "Mostreu per pantalla, el nom del fitxer corresponent a les imatges detectades"
          " com intruses i què heu fet per trobar-les:\n")
    df_ex6 = df_ex4.copy()
    df_frauds_filter = df_img_obj_fraud(df_ex6, '([_].*$)', '', 5)
    list_frauds = df_frauds_filter['name_image'].tolist()
    print("[+] S'ha detectat, com imatges intruses, els fitxer següents:")
    for image_fraud in list_frauds:
        print(image_fraud)
    print("\n[+] Resposta: s'ha fet una funció amb un simple mètode a causa del temps per l'entrega de la PAC.\n"
          "Primerament, s'ha fet modificacions per cercar nom de les ciutats dels arxius.\n"
          "Seguidament, s'ha filtrat per un nombre petit (5) gràcies a la seva distribució analitzada anteriorment.\n"
          "Observem resultats i raonem que cobri sentit, per exemple, surt a la vista que una imatge\n"
          "contingui una girafa 4 cops únicament és motiu d'exclusió sumat de la poca popularitat, entre d'altres.\n"
          "Pot ser que, dintre d'aquesta llista d'infiltrats, hagi de ser exclos algún arxiu, però és una minoria que\n"
          "no afectaria significativament al nostre model de classificació futur a predir."
          "Una altra opció podria ser observar el tamany de les imatges i treure'n conclusions.\n")


    print("\n######################### Exercici 7 #########################\n")
    print("[·] Guarda tota la informació en un fitxer .csv amb capçalera nom imatge, número de cotxes, número de\n"
          " semàfors, número de persones, ciutat, any, i si pertany o no a una ciutat:\n")
    df_ex7 = df_ex4.copy()
    df_ex7.loc[:, 'city'] = replace_column(df_ex7, 'name_image', '([_].*$)', '')
    df_ex7.loc[:, 'year'] = replace_column(df_ex7, 'name_image', r'(\w+_\d+_\w+-\d+-)|(.png|.txt)', '')
    df_ex7.loc[:, 'is_city'] = True
    list_filter_object = ['car', 'traffic light', 'person']
    df_filter_object = df_ex7[df_ex7['name'].isin(list_filter_object)]
    df_filter_object.loc[df_filter_object['name_image'].isin(list_frauds), 'is_city'] = False
    df_csv = (grouped_count_df(df_filter_object, ['name_image',
                                                  'city',
                                                  'year',
                                                  'is_city',
                                                  'name'], 'count', True).sort_values('name_image'))
    save_to_csv(df_csv, path_class_name, 'dataset_cities.csv')
    df_show = read_files(join_path(path_class_name,'dataset_cities.csv'), header=0)
    print("[+] Previsualitzem l'arxiu en qüestió:")
    print("\nColumnes:{}\n".format(df_show.columns))
    print(df_show.head())


if __name__ == '__main__':
    main()
