from botcity.web import By
from botcity.web.util import element_as_select

import logging, re  # noqa: E401
from os import environ

from src.frames import enter_frame, enter_iframe, enter_iframeId, quit_frame
from src.getters import get_field
from src.files import register_log
from src.actions import click_element
from src.config import bot

logging.basicConfig(
    filename='templateProjudi.log',
    encoding='utf-8',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

### OPERATIONS (It is being used) ###

def search_advanced_button():
    quit_frame()
    enter_frame()

    click_element("Stm0p0i1eTX")
    click_element("Stm0p1i8TRR")
    click_element("Stm0p3i1TRR")

    quit_frame()

def config_forms():
    enter_frame()
    enter_iframe()

    first_select = get_field('codVara')
    first_select = element_as_select(first_select)
    first_select.select_by_index(index=1)

    second_select = get_field('idLocalizador')
    second_select = element_as_select(second_select)
    #second_select.select_by_visible_text("Núcleo - Ag. expedição de Alvará")
    second_select.select_by_visible_text("ROBÔ - Aguardando Trânsito em Julgado")

    click_element("pesquisar")

    quit_frame()

def no_records():
    enter_frame()
    enter_iframe()

    not_register = bot.find_element('//*[@id="processoBuscaForm"]/table[2]/tbody/tr/td', By.XPATH).text

    quit_frame()

    return not_register

def mark_all_citations():
    enter_frame()
    enter_iframe()

    click_element('//*[@id="processoBuscaForm"]/table[2]/thead/tr/th[1]/input', By.XPATH)

    while True:
        next_page = bot.find_element(selector='arrowNextOn', by=By.CLASS_NAME, waiting_time=2000)

        if not next_page:
            break  # finished while loop

        else:
            next_page.click()
            bot.wait(2000)  # loading <em> elements

            click_element('//*[@id="processoBuscaForm"]/table[2]/thead/tr/th[1]/input', By.XPATH)

    click_element('movimentarEmLoteButton')

    dialog = bot.get_js_dialog()
    dialog.accept()

    quit_frame()

def check_warning_board():
    enter_frame()
    enter_iframe()

    text_warning = bot.find_element('//*[@id="errorMessages"]', By.XPATH, waiting_time=2000)

    quit_frame()

    return text_warning

def extract_processes_text():
    enter_frame()
    enter_iframe()

    text_warning = bot.find_element('//*[@id="errorMessages"]/div[3]/div/ul/li', By.XPATH).text
    process_ids = re.findall(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', text_warning) # Extract the ID from 'warning board'
    process_ids_list = list(process_ids) # Create a list with all IDs caught

    quit_frame()

    return process_ids_list

def uncheck_processes(list_id):
    enter_frame()
    enter_iframe()

    table = bot.find_element('/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody', By.XPATH)
    tr_tags = table.find_elements_by_tag_name("tr")
    length_table = len(tr_tags)

    for i in range(1, length_table, 2):
        temp_text = bot.find_element(f'/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[4]/a/em', By.XPATH).text

        if temp_text is None:
            break # keep it by security

        for process_id in list_id:
            if process_id == temp_text:
                click_element(
                    f'/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[1]/input',
                    By.XPATH
                )

                logging.info(f"Processo {temp_text} não movimentado: Restringido")
                register_log(f"Processo {temp_text} não movimentado: Restringido")

    next_page = bot.find_element(selector='arrowNextOn', by=By.CLASS_NAME, waiting_time=2000)

    if next_page:
        next_page.click()
        quit_frame()

        return uncheck_processes(list_id)

    else:
        click_element('nextButton')
        quit_frame()

def insert_files():
    enter_frame()
    enter_iframe()

    click_element('addButton')
    enter_iframeId()

    first_select = get_field('codDescricao')
    first_select = element_as_select(first_select)
    first_select.select_by_visible_text("Intimação")

    model = "Carta de intimação - despacho/decisão"
    bot.find_element('descricaoModeloDocumento', By.ID).send_keys(model)
    bot.wait(1000)
    bot.enter()

    bot.wait(1000)
    bot.find_element('/html/body/div[1]/div[2]/form/div[2]/div[1]/fieldset/table/tbody/tr[6]/td[2]/input', By.XPATH).click()

    click_element('submitButton') # Button 'Continuar'
    click_element('editButton') # Button 'Concluir'

    click_element('senhaCertificado') # Field 'Senha do Certificado'
    bot.paste(environ["password"])

    click_element('assinarButton') # Button 'Assinar Arquivos'
    click_element('closeButton') # Button 'Confirmar Inclusão'
    bot.wait(1000)

    quit_frame()

def fillForms():
    enter_frame()
    enter_iframe()

    click_element("nextButton")  # follow Intimation forms
    bot.wait(1000)

    first_select = bot.find_element('//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/select', By.XPATH)
    first_select = element_as_select(first_select)
    first_select.select_by_visible_text("Intimar Partes")

    click_element("idTipoPartesAdvogado0")  # click Checkbox lawyer

    num_days = 1
    bot.find_element('prazo0', By.ID).send_keys(num_days)

    click_element('nextButton')  # follow Locator Registration
    click_element('nextButton')  # follow Confimation forms

    # continue Moving processes
    bot.find_element('/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[6]/td/input[1]', By.XPATH).click()
    click_element('saveButton')  # finish

    quit_frame()

def archivingForms():
    enter_frame()
    enter_iframe()

    click_element("nextButton")  # follow Archive forms

    first_select = bot.find_element('//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/select', By.XPATH)
    first_select = element_as_select(first_select)
    first_select.select_by_visible_text("Arquivar Processos")

    click_element("arquivamentoDefinitivoS")  # input-radio for Definitive archiving
    click_element("nextButton")  # follow the Locator Registerd
    click_element("nextButton") # follow the Final forms
    click_element("saveButton") # Button "Salvar"

    quit_frame()

def error_continue(num_capacity):
    enter_frame()
    enter_iframe()

    operation = "Intimação de Álvara"

    logging.info(f"\nErro! Cancelando {operation} na lotação {num_capacity}")
    register_log(f"\nErro! Cancelando {operation} na lotação {num_capacity}")

    click_element('cancelButton')
    quit_frame()
