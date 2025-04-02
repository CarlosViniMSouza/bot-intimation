from botcity.web import WebBot, Browser, By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging

from os import environ

from src.actions import open_projudi, swith_capacities
from src.login import login
from src.files import create_directory, register_log, move_files
from src.getters import get_elements, get_capacity

bot_web = WebBot()
bot_web.headless = False
bot_web.browser = Browser.EDGE
bot_web.driver_path = EdgeChromiumDriverManager().install()

logging.basicConfig(
    filename='templateProjudi.log', 
    encoding='utf-8', 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def setup():
    logging.info('Iniciando execução!')

    try:
        open_projudi(bot=bot_web)

    except Exception as err:
        logging.error(f'Erro abrir o Projudi! {err}')
        exit()

    login(bot=bot_web)
    create_directory()

    try:
        capacity = get_elements('//div[@id="listaAreaAtuacaovara"]//li//a', By.XPATH)
        quantity_capacities = len(capacity)

    except Exception as err:
        logging.error(f'Erro ao carregar lotações! {err}')
        exit()

    start_from = environ["start_from"]
    start_from = int(start_from)

    for i in range(start_from, quantity_capacities+1):
        number_capacity = get_capacity(i)

        logging.info(f'Acessando lotação {number_capacity}!')
        register_log(f"Acessando lotação {number_capacity}!")

        # start_procedures() --> equivalent to the main() function
        
        logging.info(f'Encerrando acesso lotação {number_capacity}!')
        register_log(f"Encerrando acesso na lotação {number_capacity}")
        
        swith_capacities()
    
    # remove_downloads()
    # send_log_email()
    move_files()

    logging.info('Execução finalizada com sucesso!')
    bot_web.stop_browser()

setup()