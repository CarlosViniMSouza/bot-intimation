### GETTERS ###
import logging
from datetime import date
from botcity.web import By
from src.config import bot
#from src.files import register_log

logging.basicConfig(
    filename='templateProjudi.log',
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

### GETTERS ###

def get_field(selector, by=By.ID, property=''):
    global element

    try:
        attempts = 20
        found = False

        while not found and attempts > 0:
            element = bot.find_element(selector, by, ensure_clickable=True)

            if element:
                found = True
            else:
                attempts -= 1

        if property == '':
            return element
        else:
            return element.get_property(property)

    except Exception as err:
        logging.error(f'Erro ao obter {selector}! {err}')

def get_elements(selector, by=By.XPATH, property=''):
    try:
        found = False
        attempts = 20

        while not found and attempts > 0:
            elements = bot.find_elements(selector, by)

            if elements:
                found = True
            else:
                attempts -= 1

        if property == '':
            return elements
        else:
            elements_property = []

            for element in elements:
                value = element.get_property(property)

                if type(value) is str:
                    value = value.strip()

                elements_property.append(value)

            return elements_property

    except Exception as err:
        logging.error(f'Erro ao buscar os elementos! {err}')
        exit()

def get_content(element, property='textContent'):
    try:
        value = element.get_property(property)
        return value.strip()

    except Exception as err:
        logging.error(f'Erro ao obter {property} do elemento {element}: {err}')
        exit()

def get_capacity(index):
    try:
        capacity = get_field(f"//div[@id='listaAreaAtuacaovara']//li[{index}]//a", By.XPATH)
        number_capacity = capacity.get_property('title')
        capacity.click()

        return number_capacity

    except Exception as err:
        logging.error(f'Erro ao obter lotação: {err}')
        exit()

def get_current_day():
    return str(date.today())

def get_directory():
    day = get_current_day()
    return './logging/' + day
