from shutil import posix

import pandas as pd
import pathlib
import posixpath
import os
import pprint

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

START_of_nested_dirs = "/home/dream/PycharmProjects/Parser_INVENTARN/READ_FILES"

def folder_recursive_path_parts_list_maker(START_of_nested_dirs):
    """
    Функція рекурсивно дістає назву файлу з кожної директорії від вказаного
    початку директрій START_of_nested_dirs, і  екстрагує  зі  шляху  значення
    додаткових полів датафрейму, який потім буде створений з вихідного  файлу
    list_of_parts
    :param START_of_nested_dirs:
    :return:список списків [
                            [
                            тип_парсера_згідно_першої_папки_гнізда, #'Inventarny_opysy'
                            шлях,
                            назва_файлу_без_розширення,
                            [список значень полів (fk_id) що будуть додані зі шляху у датафрейм],
                             ]
                             ]
    """
    my_path_lib_obj = pathlib.Path(START_of_nested_dirs)
    list_of_not_empty_folders_paths = []

    for item in my_path_lib_obj.rglob("*"):
        if item.is_file():
            #print(type(item), '\n')
            #print('posixpath.dirname(item)=>', posixpath.dirname(item))

            # отримуємо список назв, з яких складається  шлях
            path_str = str(item)
            #p = pathlib.PurePath(str(item))# без проміжної змінної path_str чомусь не  працює...
            p = pathlib.PurePath(path_str)
            list_of_parts = list(p.parts)
            #print('list_of_parts =>',list_of_parts)

            filename_with_ext = posixpath.basename(item)
            #filename_with_ext = list_of_parts[-1]
            #print('filename_with_ext =>', filename_with_ext)

            filename_without_ext = filename_with_ext.split('.')[0]
            #print('filename_without_ext =>', filename_without_ext)

            zvd_no_nazva = list_of_parts[-2]
            #print('zvd_no_nazva=>', zvd_no_nazva)
            nazva_dilnytsi = list_of_parts[-3]
            #print('nazva_dilnytsi =>', nazva_dilnytsi)

            mvo_pib = list_of_parts[-4]
            #print('mvo_pib =>', mvo_pib)

            list_of_added_to_df_fields_of_fk_keys = []
            list_of_added_to_df_fields_of_fk_keys.extend([mvo_pib, nazva_dilnytsi])

            file_description = [zvd_no_nazva, path_str,filename_without_ext,list_of_added_to_df_fields_of_fk_keys]
            #print('file_description=>', file_description)
            list_of_not_empty_folders_paths.append(file_description)

    return list_of_not_empty_folders_paths

result_lst = folder_recursive_path_parts_list_maker(START_of_nested_dirs)
#pprint.pp(result_lst)


