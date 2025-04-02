import logging
from botcity.web import By

from src.frames import enter_frame, enter_iframe, enter_iframeId, quit_frame
from src.files import register_log

from src.config import config_botweb

bot = config_botweb()
logging.basicConfig(
    filename='templateProjudi.log', 
    encoding='utf-8', 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def open_projudi(bot):
    HML = "http://10.47.76.126:8082/projudi/"
    #HML = "http://10.47.60.136:8082/projudi/"
    #PROD = "https://projudi.tjam.jus.br/projudi/"

    bot.browse(HML)
    bot.maximize_window()

def click_element(bot, seletor, by=By.ID):
    try:
        attempts = 20
        found = False

        while not found and attempts > 0:
            element = bot.find_element(seletor, by, ensure_clickable=True)
            
            if element:
                element.click()
                found = True
            else:
                attempts -= 1

    except Exception as err:
        logging.error(f'Erro ao clicar no elemento {seletor}! {err}')
        exit()

def swith_capacities():
    try:
        quit_frame()
        enter_frame()
        enter_iframe()
        click_element('alterarAreaAtuacao')
        enter_iframeId()

    except Exception as err:
        logging.error(f'Erro ao alternar lotação! {err}')
        exit()

def search_process(processo):
    quit_frame()
    enter_frame()
    enter_iframe()
    click_element('processoBusca')

    print(f"Robô atuando no processo {processo}")
    logging.info(f"Robô atuando no processo {processo}")

    bot.paste(processo)
    bot.enter()
    bot.enter()

    # verifica se o processo foi encontrado
    error = bot.find_element('errorMessages', By.ID, waiting_time=2000)
    
    if error:
        register_log(f"Erro ao pesquisar o processo: {processo}")
        print(f"Erro ao pesquisar o processo: {processo}")

        return False
    
    # verifica se existe pendência no processo
    pending = verify_pending()

    if pending:
        register_log(f"Pendência no processo: {processo}")
        print(f"Pendência no processo: {processo}")

        return False
    
    return True

def verify_pending():
    click_element('quadroFilas')
    return bot.find_element('//label[contains(text(), "Restrição à Movimentação:")]', By.XPATH, waiting_time=1000)