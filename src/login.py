import logging
from os import environ

from botcity.web import By

from src.config import bot
from src.frames import enter_frame, quit_frame
from src.actions import click_element

logging.basicConfig(
    filename='templateProjudi.log',
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

### LOGIN ###

def login():
    try:
        enter_frame()
        click_element('login')

        bot.paste(environ["user"])
        bot.tab()
        bot.paste(environ["password"])
        bot.enter()

        if error_login():
            exit()

        quit_frame()

    except Exception as err:
        logging.error(f'Erro ao efetuar login: {err}')
        exit()

def error_login():
    try:
        bot.find_element('errorMessages', By.ID, waiting_time=2000).click()
        logging.error('Erro ao efetuar login!')

        return True

    except:
        logging.info('Login efetuado com sucesso!')
        return False
