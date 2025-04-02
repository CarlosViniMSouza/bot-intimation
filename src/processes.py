import logging
from botcity.web import By

from src.actions import click_element
from src.files import register_log
from src.frames import enter_frame, enter_iframe, quit_frame

def search_process(bot, process):
    quit_frame()
    enter_frame()
    enter_iframe()
    click_element('processBusca')

    print(f"Robô atuando no process {process}")
    logging.info(f"Robô atuando no process {process}")

    bot.paste(process)
    bot.enter()
    bot.enter()

    # verifica se o process foi encontrado
    error = bot.find_element('errorMessages', By.ID, waiting_time=2000)
    
    if error:
        register_log(f"Erro ao pesquisar o process: {process}")
        print(f"Erro ao pesquisar o process: {process}")

        return False
    
    # verifica se existe pendência no process
    pending = verify_pending()

    if pending:
        register_log(f"Pendência no process: {process}")
        print(f"Pendência no process: {process}")

        return False
    
    return True

def verify_pending(bot):
    click_element('quadroFilas')
    return bot.find_element('//label[contains(text(), "Restrição à Movimentação:")]', By.XPATH, waiting_time=1000)