from botcity.web import WebBot, Browser, By
from botcity.plugins.email import BotEmailPlugin
from botcity.web.util import element_as_select
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import logging, re, os, shutil
from os import makedirs, listdir, rename, environ, path, remove
from os.path import isdir
from dotenv import load_dotenv
from datetime import date

bot = WebBot()
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
            element = bot.find_element(
                selector,
                by,
                ensure_clickable=True
            )

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
    global elements
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

            for obj in elements:
                value = obj.get_property(property)

                if type(value) is str:
                    value = value.strip()

                elements_property.append(value)

            return elements_property

    except Exception as err:
        logging.error(f'Erro ao buscar os elementos! {err}')
        exit()

def get_content(obj, property='textContent'):
    try:
        value = obj.get_property(property)
        return value.strip()

    except Exception as err:
        logging.error(f'Erro ao obter {property} do element {obj}! {err}')
        exit()

def get_capacity(index):
    try:
        capacity = get_field(
            f"//div[@id='listaAreaAtuacaovara']//li[{index}]//a",
            By.XPATH
        )
        number_capacity = capacity.get_property('title')
        capacity.click()

        return number_capacity

    except Exception as err:
        logging.error(f'Erro ao obter lotação! {err}')
        exit()

def get_current_day():
    return str(date.today())

def get_directory():
    data = get_current_day()
    return './logging/' + data

### FRAMES ###

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

### FILES ###

def register_log(msg):
    CURRENT_DAY = get_current_day()
    FILE = CURRENT_DAY + ' - log_operacao.txt'

    with open(FILE, "a") as file:
        print(msg, file=file)

def create_directory():
    try:
        DIRECTORY = get_directory()

        if not isdir(DIRECTORY):
            makedirs(DIRECTORY)

        enter_frame()

    except Exception as err:
        logging.error(f'Erro ao criar diretório do arquivo de saída para o usuário! {err}')
        exit()

def move_files():
    DIRECTORY = get_directory()
    CURRENT_DAY = get_current_day()

    list_files = listdir('./')
    file_log = CURRENT_DAY + ' - log_operacao.txt'

    for file in list_files:
        if ".pdf" in file:
            rename(f"./{file}", f"{DIRECTORY}/{file}")

        if file_log in file:
            rename(f"./{file}", f"{DIRECTORY}/{file}")

def remove_downloads():
    try:
        files = listdir('./')

        if len(files) == 0:
            logging.warning('Não há arquivos para excluir!')
        else:
            for file in files:
                if file.endswith('.pdf'):
                    path_file = path.join('./', file)

                    if path.isfile(path_file):
                        remove(path_file)

            logging.info('Arquivos excluídos com sucesso!')

    except Exception as err:
        logging.error(f'Erro ao excluir arquivos! {err}')
        exit()

def delete_files():
    CURRENT_DAY = get_current_day()
    FILE = CURRENT_DAY + ' - log_operacao.txt'

    if os.path.exists(r".\templateProjudi.log"):
        os.remove(r".\templateProjudi.log")

    else:
        print("The file does not exist")

    if os.path.exists(rf".\{FILE}"):
        os.remove(rf".\{FILE}")

    else:
        print("The file does not exist")

    shutil.rmtree(r".\logging")

### ACTIONS ###

def open_projudi():
    HML = "http://10.47.76.126:8082/projudi/"
    # HML = "http://10.47.60.136:8082/projudi/"
    # PROD = "https://projudi.tjam.jus.br/projudi/"

    bot.headless = False
    bot.browser = Browser.EDGE
    bot.driver_path = EdgeChromiumDriverManager().install()
    bot.browse(HML)
    bot.maximize_window()

def click_element(selector, by=By.ID):
    try:
        attempts = 20
        found = False

        while not found and attempts > 0:
            obj = bot.find_element(
                selector,
                by,
                ensure_clickable=True
            )

            if obj:
                obj.click()
                found = True
            else:
                attempts -= 1

    except Exception as err:
        logging.error(f'Erro ao clicar no elemento {selector}! {err}')
        exit()

def swith_capacities():
    try:
        quit_frame()
        enter_frame()
        enter_iframe()

        click_element('alterarAreaAtuacao')
        enter_iframeId()

    except Exception as err:
        logging.error(f'Erro ao alternar lotação! {err}')
        exit()

### LOGIN ###

def login():
    try:
        enter_frame()
        click_element('login')

        bot.paste(environ["user"])
        bot.tab()
        bot.paste(environ["password"])
        bot.enter()

        if error_login():
            exit()

        quit_frame()

    except Exception as err:
        logging.error(f'Erro ao efetuar login! {err}')
        register_log(f'Erro ao efetuar login! {err}')

        exit()

def error_login():
    try:
        bot.find_element(
            'errorMessages',
            By.ID,
            waiting_time=2000
        ).click()

        logging.error('Erro ao efetuar login!')
        register_log('Erro ao efetuar login!')

        return True

    except Exception as err:
        print(err)

        logging.info(f'Login efetuado com sucesso!')
        register_log(f'Login efetuado com sucesso!')

        return False

### EMAIL ###

def send_email_attachment():
    email = BotEmailPlugin()

    email.configure_imap("imap.gmail.com", 993)
    email.configure_smtp(host_address="smtp.gmail.com", port=587)
    email.login(email="botcityifam@gmail.com", password="licp pjdk zdet japu")

    # DIRECTORY = get_directory()
    CURRENT_DAY = get_current_day()

    # list_files = listdir(f'./logging/')
    # file_log = CURRENT_DAY + ' - log_operacao.txt'

    to = ["2021002252@ifam.edu.br"]
    subject = f"Send Log Bot in {CURRENT_DAY}"
    body = "This email is send automaticly when the automation finished!"
    files = [rf'C:\Users\Carlos_Souza\Documents\projects\bot_intimation_inss\logging\{CURRENT_DAY}\{CURRENT_DAY} - log_operacao.txt']

    email.send_message(subject, body, to, attachments=files, use_html=False)
    email.disconnect()

    logging.info(f"Email enviado para {to}.")
    register_log(f"Email enviado para {to}.")

### FUNCTIONS TO USE IN main() ###

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
    second_select.select_by_visible_text("Núcleo - Ag. expedição de Alvará")
    # second_select.select_by_visible_text(text="ROBÔ - Aguardando Trânsito em Julgado")

    click_element("pesquisar")

    quit_frame()

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

    logging.info("Marcado todos os processos da página!")
    register_log("Marcado todos os processos da página!")

    dialog = bot.get_js_dialog()
    dialog.accept()

    quit_frame()

def extract_processes_text():
    enter_frame()
    enter_iframe()

    try:
        text_warning = bot.find_element(
            '//*[@id="errorMessages"]/div[3]/div/ul/li',
            By.XPATH
        ).text

        # Extract the ID processes after the word 'processo(s)'
        process_ids = re.findall(
            r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',
            text_warning
        )

        # Create a list with all IDs caught
        process_ids_list = list(process_ids)

        logging.info(f"Processos desmarcados: {process_ids_list}")
        register_log(f"Processos desmarcados: {process_ids_list}")

        quit_frame()

        return process_ids_list

    except Exception as ex:
        print(f"Text not Found! {ex}")

def no_records():
    try:
        enter_frame()
        enter_iframe()

        without_register = bot.find_element(
            '//*[@id="processoBuscaForm"]/table[2]/tbody/tr/td',
            By.XPATH
        ).text

        logging.info('Sem registros/processos na Unidade.')
        register_log('Sem registros/processos na Unidade.')

        quit_frame()

        return without_register

    except Exception as ex:
        print(ex)

def check_warning_board():
    enter_frame()
    enter_iframe()

    text_warning = bot.find_element(
        '//*[@id="errorMessages"]',
        By.XPATH,
        waiting_time=2000
    )

    quit_frame()
    logging.info('Quadro de Erros encontrado!')
    register_log('Quadro de Erros encontrado!')

    return text_warning

def uncheck_processes(listID):
    enter_frame()
    enter_iframe()

    try:
        table = bot.find_element(
            '//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody',
            By.XPATH
        )

        # Count <tr> tags in table
        tr_tags = table.find_elements_by_tag_name("tr")
        length_table = len(tr_tags)

        for i in range(1, length_table, 2):
            temp_text = bot.find_element(
                f'/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[4]/a/em',
                By.XPATH
            ).text

            if temp_text is None:
                break  # There are no more processes to uncheck

            print(f"Vendo {i}° processo: {temp_text}")

            for processId in listID:
                if temp_text == processId:
                    click_element(
                        f'/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[1]/input',
                        By.XPATH
                    )

            print(f"Processo {temp_text} desmarcado")
            logging.info(f"Processo {temp_text} desmarcado")
            register_log(f"Processo {temp_text} desmarcado")

        while True:
            next_page = bot.find_element(
                selector='arrowNextOn',
                by=By.CLASS_NAME,
                waiting_time=2000
            )

            if next_page is None:
                break
            else:
                next_page.click()

                table = bot.find_element(
                    '//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody',
                    By.XPATH
                )

                # Count <tr> tags in table
                tr_tags = table.find_elements_by_tag_name("tr")
                length_table = len(tr_tags)

                bot.wait(2000)

                for i in range(1, length_table, 2):
                    temp_text = bot.find_element(
                        f'/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[4]/a/em',
                        By.XPATH
                    ).text

                    if temp_text is None:
                        break  # There are no more processes to uncheck

                    print(f"Vendo {i}° processo: {temp_text}")

                    for processId in listID:
                        if temp_text == processId:
                            click_element(
                                f'/html/body/div[1]/div[2]/form/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[{i}]/td[1]/input',
                                By.XPATH
                            )

                    print(f"Processo {temp_text} desmarcado")
                    logging.info(f"Processo {temp_text} desmarcado")
                    register_log(f"Processo {temp_text} desmarcado")

            click_element('nextButton')
            quit_frame()  # finish Input forms

    except Exception as ex:
        print(ex)

        click_element('nextButton')
        quit_frame()  # finish Input forms

def insert_files():
    quit_frame()
    enter_frame()
    enter_iframe()

    try:
        click_element('//*[@id="addButton"]')

    except Exception as ex:
        print(ex)

    quit_frame()

def fillForms():
    # quit_frame()
    enter_frame()
    enter_iframe()

    # click_element("nextButton") # follow File template forms

    # TODO insert_files() # insert intimation file template

    click_element("nextButton")  # follow Intimation forms
    # bot.wait(2000)

    first_select = bot.find_element(
        '//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/select',
        By.XPATH
    )
    first_select = element_as_select(first_select)
    first_select.select_by_index(index=2)

    # click_element("nextButton")  # follow Checkboxs forms
    click_element("idTipoPartesAdvogado0")  # click Checkbox lawyer

    num_days = 1
    bot.find_element('prazo0', By.ID).send_keys(num_days)
    click_element('nextButton')  # follow Locator Registration

    second_select = bot.find_element(
        'codLocalizador',
        By.ID
    )
    second_select = element_as_select(second_select)
    second_select.select_by_visible_text(text="Núcleo - RPV EXPEDIDO")

    click_element('nextButton')  # follow Confimation forms
    bot.scroll_down(6)

    click_element(
        '//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td/input[1]',
        By.XPATH
    )  # continue Moving processes
    click_element('saveButton')  # finish

    quit_frame()

def archivingForms():
    enter_frame()
    enter_iframe()

    click_element("nextButton")  # follow Archive forms

    first_select = bot.find_element(
        '//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/select',
        By.XPATH
    )
    first_select = element_as_select(first_select)
    first_select.select_by_index(index=4)

    click_element('arquivamentoDefinitivoS')  # input-radio for Definitive archiving
    click_element("nextButton")  # follow

    second_select = bot.find_element(
        '//*[@id="codLocalizador"]',
        By.XPATH
    )
    second_select = element_as_select(second_select)
    second_select.select_by_visible_text('Núcleo - Ag. expedição de Alvará')

    click_element("nextButton")  # follow the Final forms

    quit_frame()

def error_continue():
    try:
        enter_frame()
        enter_iframe()

        click_element('cancelButton')

        quit_frame()

    except Exception as ex:
        print(ex)

### PRINCIPAL FUNCTION ###

def main():
    logging.info('Iniciando execução!')

    try:
        open_projudi()

    except Exception as err:
        logging.error(f'Erro abrir o Projudi! {err}')
        exit()

    login()
    create_directory()

    try:
        capacity = get_elements('//div[@id="listaAreaAtuacaovara"]//li//a', By.XPATH)
        quantity_capacities = len(capacity)

    except Exception as err:
        logging.error(f'Erro ao carregar lotações! {err}')
        exit()

    start_from = environ["start_from"]
    start_from = int(start_from)

    for i in range(start_from, quantity_capacities + 1):
        number_capacity = get_capacity(i)

        logging.info(f'Acessando lotação {number_capacity}!')
        register_log(f"Acessando lotação {number_capacity}!")

        # start_procedures() --> equivalent to the main() function

        # Search Advanced button #
        search_advanced_button()

        # Configuration Forms #
        config_forms()

        no_record = no_records()

        if no_record == "Nenhum registro encontrado":
            print("Sem registros. Proxima Unidade!\n")

        else:
            # mark all citations in the page #
            mark_all_citations()

            # extract ID processes from warning #
            warning = check_warning_board()

            if warning:
                ids = extract_processes_text()
                print(f"Processos obtidos: {ids}")

                uncheck_processes(listID=ids)  # Search Process by Process

            else:
                print("Quadro de Aviso não Detectado!")

            # case for unmark all processes #
            text_error = check_warning_board()

            if text_error:
                error_continue()  # return to First Forms

            else:
                print("Sem problemas com os processos seleciondos!")

                fillForms()
                archivingForms()

        # Change Court
        logging.info(f"Encerrando acesso lotação {number_capacity}!")
        register_log(f"Encerrando acesso lotação {number_capacity}!")

        swith_capacities()
        # End RPA

    # remove_downloads()
    move_files()
    send_email_attachment()
    delete_files() # delete old files/folder

    logging.info('Execução finalizada com sucesso!')
    bot.stop_browser()

if __name__ == '__main__':
    load_dotenv()
    main()
