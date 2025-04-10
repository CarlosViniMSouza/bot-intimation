import os
import logging
from os import environ
from dotenv import load_dotenv

from botcity.web import By

from src.config import bot
from src.files import move_files, delete_files
from src.files import register_log, create_directory

from src.login import login
from src.getters import get_elements, get_capacity
from src.actions import open_projudi, swith_capacities
from src.email import send_email_attachment

from src.operations import archivingForms, fillForms, config_forms
from src.operations import search_advanced_button, mark_all_citations
from src.operations import check_warning_board, no_records
from src.operations import extract_processes_text, uncheck_processes
from src.operations import error_continue, insert_files

def main():
    delete_files() # remove old files

    logging.info('Iniciando execução!')

    try:
        open_projudi()

    except Exception as err:
        logging.error(f'Erro ao abrir o Projudi: {err}')
        exit()

    login()
    create_directory()

    try:
        capacity = get_elements('//div[@id="listaAreaAtuacaovara"]//li//a', By.XPATH)
        quantity_capacities = len(capacity)

    except Exception as err:
        logging.error(f'Erro ao carregar lotações! {err}')
        exit()

    start_from = environ["start_from"]
    start_from = int(start_from)

    os.system('cls') # clean the dirt from the terminal

    for i in range(start_from, quantity_capacities + 1):
        number_capacity = get_capacity(i)

        logging.info(f"Acessando lotação {number_capacity}\n")
        register_log(f"Acessando lotação {number_capacity}\n")

        # Search Advanced button #
        search_advanced_button()

        # Configuration Forms #
        config_forms()

        no_record = no_records()

        if no_record == "Nenhum registro encontrado":
            logging.info("\nSem registros. Proxima Unidade!")
            register_log("\nSem registros. Proxima Unidade!")

        else:
            # mark all citations in the page #
            mark_all_citations()

            # extract ID processes from warning #
            warning = check_warning_board()

            if warning:
                ids = extract_processes_text()

                logging.info(f"\nProcessos restritos: {ids}")
                register_log(f"\nProcessos restritos: {ids}")

                uncheck_processes(list_id=ids)  # Search Process by Process

            # case for unmark all processes #
            text_error = check_warning_board()

            if text_error:
                error_continue(num_capacity=number_capacity)  # return to First Forms

            else:
                insert_files() # insert intimation file template
                fillForms()
                archivingForms()

        logging.info(f"\nEncerrando acesso lotação {number_capacity}!")
        register_log(f"\nEncerrando acesso lotação {number_capacity}!")

        swith_capacities() # Change Court
        # End RPA

    logging.info('\nExecução finalizada com sucesso!')
    bot.stop_browser()

    # remove_downloads()
    move_files()
    send_email_attachment()

if __name__ == '__main__':
    load_dotenv()
    main()