### ADDITIONAL (It is not being used) ###
import logging
from config import bot
from os import environ

from botcity.web import By
from botcity.plugins.gmail import BotGmailPlugin

from src.files import register_log
from src.actions import click_element
from src.frames import enter_frame, enter_iframe, quit_frame

### ADDITIONAL (It is not being used) ###

def search_process(process):
    quit_frame()
    enter_frame()
    enter_iframe()

    click_element('processoBusca')
    print(f"Robô atuando no processo {process}")
    logging.info(f"Robô atuando no processo {process}")

    bot.paste(process)
    bot.enter()
    bot.enter()

    # Check if the process was found
    error = bot.find_element('errorMessages', By.ID, waiting_time=2000)

    if error:
        register_log(f"Erro ao pesquisar o processo: {process}")
        print(f"Erro ao pesquisar o processo: {process}")

        return False

    # verifica se existe pendência no processo
    pending = check_pending()

    if pending:
        register_log(f"Pendência no processo: {process}")
        print(f"Pendência no processo: {process}")

        return False

    return True

def check_pending():
    click_element('quadroFilas')
    return bot.find_element('//label[contains(text(), "Restrição à Movimentação:")]', By.XPATH, waiting_time=1000)

def start_procedures():
    quit_frame()
    enter_frame()

    """
    If you need to access the system menu, 
    insert the code before calling the enter_iframe() method.
    """

    enter_iframe()

def send_log_email():
    credentials = './gmail.json'
    gmail = BotGmailPlugin(credentials, environ['sender'])
    bcc = get_Bcc()
    to = get_Cc()

    subject = "Teste e-mail"
    body = "Teste de e-mail!\nFavor não responder."
    files = []
    gmail.send_message(subject, body, to, bcc_addrs=bcc, attachments=files, use_html=False)

def get_Bcc():
    QUANT_COURTS = environ['quant_courts']
    QUANT_COURTS = int(QUANT_COURTS)
    bcc = []

    for i in range(1, QUANT_COURTS + 1):
        index = f'bcc{i}'
        bcc.append(environ[index])

    return bcc

def get_Cc():
    cc = []

    for i in range(1, 3):
        index = f'cc{i}'
        cc.append(environ[index])

    return cc
