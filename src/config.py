from botcity.web import WebBot, Browser
from webdriver_manager.microsoft import EdgeChromiumDriverManager

bot = WebBot()
bot.headless = False
bot.browser = Browser.EDGE
bot.driver_path = EdgeChromiumDriverManager().install()
