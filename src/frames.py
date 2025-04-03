from botcity.web import By

from src.getters import get_field

def enter_frame(bot):
    frame = get_field(bot, 'mainFrame')
    bot.enter_iframe(frame)

def enter_iframe(bot):
    iframe = get_field(bot, 'userMainFrame', By.NAME)
    bot.enter_iframe(iframe)

def enter_iframeId(bot):
    iframe = get_field(bot, '//iframe[contains(@name,"window")]', By.XPATH)
    bot.enter_iframe(iframe)

def quit_frame(bot):
    bot.leave_iframe()

def start_procedures():
    # TO DO
    quit_frame()
    enter_frame()
    # se precisar acessar o menu do sistema, insera o código 
    # antes da chamar o método enter_iframe()
    enter_iframe()