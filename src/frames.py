from botcity.web import By
from src.config import bot
from src.getters import get_field

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