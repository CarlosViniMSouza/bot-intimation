### ACTIONS ###
import logging
from botcity.web import By
from src.config import bot
from src.frames import enter_frame, enter_iframe, enter_iframeId, quit_frame

logging.basicConfig(
    filename='templateProjudi.log',
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def open_projudi():
    HML = "http://10.47.76.126:8082/projudi/"
    # HML = "http://10.47.60.136:8082/projudi/"
    # PROD = "https://projudi.tjam.jus.br/projudi/"

    #bot.headless = False
    #bot.browser = Browser.EDGE
    #bot.driver_path = EdgeChromiumDriverManager().install()
    bot.browse(HML)
    bot.maximize_window()

def stopped_browser():
    bot.stop_browser()

def click_element(selector, by=By.ID):
    try:
        attempts = 20
        found = False

        while not found and attempts > 0:
            obj = bot.find_element(
                selector,
                by,
                ensure_clickable=True
            )

            if obj:
                obj.click()
                found = True
            else:
                attempts -= 1

    except Exception as err:
        logging.error(f'Erro ao clicar no elemento {selector}! {err}')
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
