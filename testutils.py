import unittest
from utils import (
    get_path_files,
    get_list_names_files_from_path,
    read_files,
    concat_list_df,
    merge_df,
    check_yolo,
    join_path,
    check_match_fileImage_fileLabel,
    grouped_count_df,
    get_dict_object_populars_byImage,
    replace_column,
    df_img_obj_fraud,
    save_to_csv,
    search_pattern_yolo,
    get_list_index_popular_key
)
import pandas as pd


class TestUtils(unittest.TestCase):
    main_project_path = None

    @classmethod
    def setUpClass(cls):
        print("\n############################################## Testutils.py ##############################################")
        print("\n[!] Carreguem tots els datasets que tenim durant el codi d'un sol cop per fer tests posteriorment:\n")
        cls.path_class_name, cls.path_image, cls.path_label = get_path_files(cls.main_project_path)
        cls.list_files_from_labels = sorted(get_list_names_files_from_path(cls.path_label))
        cls.list_files_from_images = sorted(get_list_names_files_from_path(cls.path_image))
        cls.list_files_from_dataset = sorted(get_list_names_files_from_path(cls.path_class_name))
        cls.name_class_file = cls.list_files_from_dataset[cls.list_files_from_dataset.index("class_name.txt")]
        cls.list_df_labelfiles: list = []
        cls.title = ['id', 'coordenades_x_c', 'coordenades_y_c', 'coordenades_w', 'coordenades_h', 'prob_encertar']
        for index in range(len(cls.list_files_from_labels)):
            if check_match_fileImage_fileLabel(cls.list_files_from_labels, cls.list_files_from_images, index):
                cls.df_file = read_files(join_path(cls.path_label, cls.list_files_from_labels[index]), cls.title,
                                         delimiter=' ')
                cls.df_file['name_image'] = str(cls.list_files_from_images[index])
                cls.df_file['index_sorted'] = index
                cls.list_df_labelfiles.append(cls.df_file)
        cls.df_labels = concat_list_df(cls.list_df_labelfiles)
        cls.class_df = read_files(join_path(cls.path_class_name, cls.name_class_file), title=['id', 'name'],
                                  delimiter=r"(?<=\d\s)")
        cls.df_merged_ex1 = merge_df(cls.df_labels, cls.class_df, 'id')
        count: int = 0
        for i in range(len(cls.list_files_from_labels)):
            if not check_yolo(join_path(cls.path_label, cls.list_files_from_labels[i])):
                count += 1
                cls.df_merged_ex1.drop(cls.df_merged_ex1[cls.df_merged_ex1['index_sorted'] == i].index)
        if not count:
            print("Tots els fitxers compleixen amb el format YOLO")
        cls.df_yolo_ex2 = cls.df_merged_ex1.copy()
        cls.df_ex4 = cls.df_yolo_ex2[cls.df_yolo_ex2['prob_encertar'] > 0.4]
        cls.df_grouped_id = grouped_count_df(cls.df_ex4, ['id'], 'count', True)
        cls.df_grouped_name = grouped_count_df(cls.df_ex4, ['name'], 'count', True)
        cls.top_5 = cls.df_ex4[cls.df_ex4.name.isin(list(cls.df_grouped_name['name'].head(5)))]
        cls.df_ex5 = cls.df_ex4.copy()
        cls.df_ex5.loc[:, 'year'] = replace_column(cls.df_ex5, 'name_image', r'(\w+_\d+_\w+-\d+-)|(.png|.txt)', '')
        cls.df_ex5.loc[:, 'city'] = replace_column(cls.df_ex5, 'name_image', '([_].*$)', '')
        cls.df_ex5_group = grouped_count_df(cls.df_ex5, ['year', 'city', 'name'], 'count', True)
        cls.df_ex5_group_filter = cls.df_ex5_group[cls.df_ex5_group['name'] == 'car']
        cls.df_ex6 = cls.df_ex4.copy()
        cls.df_frauds_filter = df_img_obj_fraud(cls.df_ex6, '([_].*$)', '', 5)
        cls.list_frauds = cls.df_frauds_filter['name_image'].tolist()
        cls.df_ex7 = cls.df_ex4.copy()
        cls.df_ex7.loc[:, 'city'] = replace_column(cls.df_ex7, 'name_image', '([_].*$)', '')
        cls.df_ex7.loc[:, 'year'] = replace_column(cls.df_ex7, 'name_image', r'(\w+_\d+_\w+-\d+-)|(.png|.txt)', '')
        cls.df_ex7.loc[:, 'is_city'] = True
        cls.list_filter_object = ['car', 'traffic light', 'person']
        cls.df_filter_object = cls.df_ex7[cls.df_ex7['name'].isin(cls.list_filter_object)].copy()
        cls.df_filter_object.loc[cls.df_filter_object['name_image'].isin(cls.list_frauds), 'is_city'] = False
        cls.df_csv = (grouped_count_df(cls.df_filter_object, ['name_image',
                                                              'city',
                                                              'year',
                                                              'is_city',
                                                              'name'], 'count', True).sort_values('name_image'))
        save_to_csv(cls.df_csv, cls.path_class_name, 'dataset_cities.csv')
        cls.df_show = read_files(join_path(cls.path_class_name, 'dataset_cities.csv'), header=0)
        cls.df_group_name_naming = grouped_count_df(cls.df_ex4, ['name_image', 'name'], 'count', True)

    def test_outputs_types(self):
        self.assertIsInstance(get_list_index_popular_key(self.df_group_name_naming,
                                                         'name_image',
                                                         'count',
                                                         'name',
                                                         'berlin_000000_000019_leftImg8bit_20-10-2018.png'), list)
        self.assertIsInstance(get_dict_object_populars_byImage(self.df_ex4, 'name', 'name_image'), dict)
        self.assertIsInstance(grouped_count_df(self.df_ex4, ['id'], 'count', True), pd.DataFrame)
        self.assertIsInstance(read_files(join_path(self.path_class_name, self.name_class_file),
                                         title=['id', 'name'],
                                         delimiter=r"(?<=\d\s)"), pd.DataFrame)
        self.assertIsInstance(concat_list_df(self.list_df_labelfiles), pd.DataFrame)
        self.assertIsInstance(merge_df(self.df_labels, self.class_df, 'id'), pd.DataFrame)
        self.assertIsInstance(get_path_files(self.main_project_path), tuple)
        self.assertIsInstance(join_path(self.path_class_name, 'Ex5Fig.png'), str)
        self.assertIsInstance(get_list_names_files_from_path(self.path_class_name), list)
        self.assertIsInstance(df_img_obj_fraud(self.df_ex6, '([_].*$)', '', 5), pd.DataFrame)

    def test_outputs_bool(self):
        self.assertTrue(check_yolo(join_path(self.path_label, 'berlin_000000_000019_leftImg8bit_20-10-2018.txt')))
        self.assertFalse(search_pattern_yolo('2 0.986572 0.455078 -0.0268555 0.0820312 0.227208'))
        self.assertFalse(search_pattern_yolo('81 0.986572 0.455078 0.0268555 0.0820312 0.227208'))
        self.assertFalse(search_pattern_yolo('2 0.986572 0.455078   0.0268555    0.0820312 0.227208'))
        self.assertTrue(join_path(self.path_label, self.list_files_from_labels[0]))
        self.assertTrue(check_match_fileImage_fileLabel(['berlin_000000_000019_leftImg8bit_20-10-2018.png'],
                                                        ['berlin_000000_000019_leftImg8bit_20-10-2018.txt'], 0))
        self.assertFalse(check_match_fileImage_fileLabel(['zurich_000000_000019_leftImg8bit_20-10-2018.png'],
                                                         ['berlin_000000_000019_leftImg8bit_20-10-2018.txt'], 0))
        self.assertFalse(check_match_fileImage_fileLabel(['berlin_000000_000019_leftImg8bit_20-10-2018.HOLA'],
                                                         ['berlin_000000_000019_leftImg8bit_20-10-2018.txt'], 0))

    def test_outputs_equal(self):
        i = self.df_group_name_naming
        exe_4_4_1 = 'berlin_000418_000019_leftImg8bit_01-02-2016.png'
        exe_4_4_3_A = 'berlin_000312_000019_leftImg8bit_03-12-2015.png'
        exe_4_4_2_2 = 'berlin_000345_000019_leftImg8bit_05-10-2016.png'
        exe_4_4_2_3_1 = 'berlin_000227_000019_leftImg8bit_13-02-2015.png'
        exe_4_4_2_3_2 = 'berlin_000384_000019_leftImg8bit_06-07-2016.png'
        exe_4_4_2_3_3 = 'berlin_000336_000019_leftImg8bit_12-02-2015.png'
        i_filter_1 = i[i['name_image'] == exe_4_4_1]
        i_filter_3_A = i[i['name_image'] == exe_4_4_3_A]
        i_filter_2_2 = i[i['name_image'] == exe_4_4_2_2]
        i_filter_2_3_1 = i[i['name_image'] == exe_4_4_2_3_1]
        i_filter_2_3_2 = i[i['name_image'] == exe_4_4_2_3_2]
        i_filter_2_3_3 = i[i['name_image'] == exe_4_4_2_3_3]
        print("\n##################################### Test: Ex 4.4 - 1 ########################################")
        self.assertEqual(get_list_index_popular_key(i, 'name_image', 'count', 'name', exe_4_4_1), [0, 789, 937])
        print(i_filter_1)
        print("20 person, 3 car, 2 umbr -> Si en té menys de 3 objectes o exactament 3 objectes diferents \n"
              "agafarem com a populars tots aquells que apareixen: 20, 3, 2 on l'índex rau a [0, 789, 937]\n")
        print("##################################### Test: Ex 4.4 - 3.A ########################################")
        self.assertEqual(get_list_index_popular_key(i, 'name_image', 'count', 'name', exe_4_4_3_A),
                         [1835, 1836, 1837, 1838])
        print(i_filter_3_A)
        print("1 byc, 1 car, 1 mot, 1 person -> Si la freqüència més alta apareix en més de tres objectes, \n"
              "agafarem tots aquests objectes com a els més populars \n"
              "(en aquest cas podem agafar més de tres objectes). Això inclou el cas en que tots els\n"
              "objectes tinguin la mateixa popularitat: 1, 1, 1,1 on l'índex rau a [1835, 1836, 1837, 1838]\n")
        print("##################################### Test: Ex 4.4 - 2.2 ########################################")
        self.assertEqual(get_list_index_popular_key(i, 'name_image', 'count', 'name', exe_4_4_2_2),
                         [673, 713, 1139])
        print(i_filter_2_2)
        print("4 car, 3 person, 2 traffic, 1 byc -> Si no hi ha empat de popularitat entre el 3r i 4t objecte\n"
              " més popular agafarem els 3 objectes més populars de la imatge: 4,3,2 on l'índex és [673, 713, 1139]\n")
        print("##################################### Test: Ex 4.4 - 2.3.1 ########################################")
        self.assertEqual(get_list_index_popular_key(i, 'name_image', 'count', 'name', exe_4_4_2_3_1),
                         [867, 868, 869])
        print(i_filter_2_3_1)
        print("3 car, 3 person, 3 traffic, 1 byc, 1 bus -> Si tenim empats en popularitat entre els 3 més populars i\n"
              " Si no hi ha empat de popularitat entre el 3r i 4t objecte més popular agafarem\n"
              " els tres objectes més populars: 3,3,3 on l'índex és [867, 868, 869]\n")
        print("##################################### Test: Ex 4.4 - 2.3.2 ########################################")
        self.assertEqual(get_list_index_popular_key(i, 'name_image', 'count', 'name', exe_4_4_2_3_2),
                         [326, 744])
        print(i_filter_2_3_2)
        print("8 car, 3 person, 1 byc, 1 motor -> Si l'empat de popularitat es produeix entre el 3r i 4t més populars\n"
              " agafarem només els dos objectes més populars.: 8,3 on l'índex és [326, 744]\n")
        print("##################################### Test: Ex 4.4 - 2.3.3 ########################################")
        self.assertEqual(get_list_index_popular_key(i, 'name_image', 'count', 'name', exe_4_4_2_3_3),
                         [718])
        print(i_filter_2_3_3)
        print("3 car, 2 traffic, 2 pers, 1 backpack, 1 byc -> Si l'empat de popularitat es produeix entre el 2n i 3r\n"
              " més populars agafarem només l'objecte més popular: 3 on l'índex és [718]\n")

        self.assertEqual(len(get_list_names_files_from_path(self.path_image)),
                         len(get_list_names_files_from_path(self.path_label)))
        self.assertEqual(replace_column(pd.DataFrame([['berlin_000000_000019_leftImg8bit_20-10-2018.png']],
                                                     columns=['city']), 'city', '([_].*$)', '')[0],
                         'berlin')
        self.assertEqual(self.df_show.columns.tolist(),
                         ['name_image', 'city', 'year', 'is_city', 'name', 'count'])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)
