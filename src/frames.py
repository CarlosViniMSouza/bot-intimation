from botcity.web import By

from src.getters import get_field
from src.config import config_botweb

bot = config_botweb()

def enter_frame():
    frame = get_field('mainFrame')
    bot.enter_iframe(frame)

def enter_iframe():
    iframe = get_field('userMainFrame', By.NAME)
    bot.enter_iframe(iframe)

def enter_iframeId():
    iframe = get_field('//iframe[contains(@name,"window")]', By.XPATH)
    bot.enter_iframe(iframe)

def quit_frame():
    bot.leave_iframe()

def start_procedures():
    # TO DO
    quit_frame()
    enter_frame()
    # se precisar acessar o menu do sistema, insera o código 
    # antes da chamar o método enter_iframe()
    enter_iframe()