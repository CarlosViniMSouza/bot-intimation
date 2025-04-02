from botcity.web import Browser, WebBot
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def config_botweb():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.EDGE
    bot.driver_path = EdgeChromiumDriverManager().install()

    return bot