import unittest
from plots import (
    rectangle_YOLO,
    plot_barplot,
    plot_sns,
    plot_image,
    sns_plot_norm
)

import pandas as pd
from utils import (
    get_path_files,
    join_path,
    get_list_names_files_from_path,
    check_match_fileImage_fileLabel,
    read_files,
    concat_list_df,
    merge_df
)

class TestPlot(unittest.TestCase):
    """Test the behavior of the plotting module."""
    main_project_path = None
    path_class_name, path_image, path_label = get_path_files(main_project_path)
    exe_img = 'berlin_000000_000019_leftImg8bit_20-10-2018.png'

    @classmethod
    def setUpClass(cls):
        print("\n############################################## Test utils.py ##############################################")
        print("\n[!] Carreguem únicament dataset ex1 per fer un test del plot rectangle YOLO:\n")
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

    def test_plot(self):
        """Tests the behavior of the plot function in case the inputted variable is as expected."""
        df = pd.DataFrame(
            {
                "Year": ["2000", "2005", "2015", "2020"],
                "Benefici total": [100, 150, 55, 75],
                "CEO": ['Jhon', 'Paul', 'Jhon', 'Jhon']

            }
        )
        plot_barplot(df, 'Year', 'Benefici total', "Benefits(M €)", join_path(self.path_class_name, 'Test_barplt.png'))
        sns_plot_norm(df.groupby(['CEO']).value_counts().reset_index(name='counts'), 'counts', 'CEO', 'Freq.CEO normalitzat',
                      join_path(self.path_class_name, 'Test_denplt.png'))
        plot_sns(df, 'Year', 'Benefici total', 'CEO', 'bar', 'Benefici total',
                 join_path(self.path_class_name, 'Test_snsplt.png'))
        rectangle_YOLO(join_path(self.path_image, self.exe_img),
                       self.df_merged_ex1[self.df_merged_ex1['name_image'] == self.exe_img],
                       join_path(self.path_class_name, 'Testrectangle.png'))
        plot_image(join_path(self.path_class_name, 'Test_barplt.png'))
        plot_image(join_path(self.path_class_name, 'Test_denplt.png'))
        plot_image(join_path(self.path_class_name, 'Test_snsplt.png'))
        plot_image(join_path(self.path_class_name, 'Testrectangle.png'))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlot)
    unittest.TextTestRunner(verbosity=2).run(suite)
