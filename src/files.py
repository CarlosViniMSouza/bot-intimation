import logging

from os import makedirs, listdir, rename, remove, path
from os.path import isdir

from src.getters import get_directory, get_current_day
from src.frames import enter_frame

def register_log(msg):
    CURRENT_DAY = get_current_day()
    FILE = CURRENT_DAY + ' - log_operacao.txt'

    with open(FILE, "a") as file:
        print(msg, file=file)

def create_directory():
    try:
        DIRECTORY = get_directory()

        if not isdir(DIRECTORY):
            makedirs(DIRECTORY)
        
        enter_frame()
    
    except Exception as err:
        logging.error(f'Erro ao criar diretório do arquivo de saída para o usuário! {err}')
        exit()

def move_files():
    DIRECTORY = get_directory()
    CURRENT_DAY = get_current_day()

    list_files = listdir('./')
    file_log = CURRENT_DAY + ' - log_operacao.txt'

    for file in list_files:
        if (".pdf") in file:
            rename(f"./{file}", f"{DIRECTORY}/{file}")

        if file_log in file:
            rename(f"./{file}", f"{DIRECTORY}/{file}")

def remove_downloads():
    try:
        files = listdir('./')

        if len(files) == 0:
            logging.warning('Não há arquivos para excluir!')
        else:
            for file in files:
                if file.endswith('.pdf'):
                    path_file = path.join('./', file)

                    if path.isfile(path_file):
                        remove(path_file)

            logging.info('Arquivos excluídos com sucesso!')

    except Exception as err:
        logging.error(f'Erro ao excluir arquivos! {err}')
        exit()