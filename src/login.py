import logging
from os import environ

from botcity.web import By

from src.actions import click_element
from src.frames import enter_frame, quit_frame

def error_login(bot):
    try:
        bot.find_element('errorMessages', By.ID, waiting_time=2000).click()
        logging.error('Erro ao efetuar login!')
    
        return True
    
    except Exception as err:
        logging.info('Login efetuado com sucesso!')
        print(err)

        return False

def login(bot):
    try:
        enter_frame(bot)
        click_element(bot, 'login')

        bot.paste(environ["user"])
        bot.tab()
        bot.paste(environ["password"])
        bot.enter()

        if error_login(bot):
            exit()

        quit_frame(bot)

    except Exception as err:
        logging.error(f'Erro ao efetuar login! {err}')
        exit()
