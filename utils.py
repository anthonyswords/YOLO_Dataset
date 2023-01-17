from os import listdir, getcwd
from os.path import isfile, join
import pandas as pd
import re
pd.set_option('display.max_columns', 10)


def concat_list_df(list_df):
    return pd.concat(list_df, ignore_index=True)

def merge_df(df1, df2, on, how='left', sort=False):
    return df1.merge(df1.merge(df2, how='left', on='id', sort=False))

def check_yolo(full_path_name_file) -> bool:
    regex = re.compile("^([0-7][0-9]{1}|[0-9]{1}|80)\s\d.\d+\s\d.\d+\s\d.\d+\s\d.\d+\s\d.\d+$")
    exclude_file : list=[]
    with open(full_path_name_file) as f:
        for line in f:
            if not regex.search(line):
                print("L'arxiu %s trobem que no compleix amb el format YOLO: \n%s" % (nom_fitxer,line))
                return False
    return True

def get_path_files(main_project_path=None):
    if not main_project_path:
        return \
            getcwd()+'/dataset_cities/', \
            getcwd()+'/dataset_cities/images/', \
            getcwd()+'/dataset_cities/labels/'
    else:
        return \
            main_project_path+'/dataset_cities/class_name', \
            main_project_path+'/dataset_cities/images/', \
            main_project_path+'/dataset_cities/labels/'


def get_list_names_files_from_path(path_file=None) ->list:
    return sorted(filter(lambda x: isfile(join(path_file, x)),
                  listdir(path_file)))

def check_match_fileImage_fileLabel(list_files_from_labels, list_files_from_images, index) -> bool:
    pattern = '^.*(?=.txt|.png)'
    if re.findall(pattern,
                  list_files_from_labels[index]) == re.findall(pattern,
                                                               list_files_from_images[index]):
        return True
    return False



def read_files(full_path_name_file, title):
    df_file = pd.read_csv(full_path_name_file, sep=' ', names=title)
    return df_file



