from botcity.web import WebBot, Browser, By
from botcity.plugins.email import BotEmailPlugin
from botcity.web.util import element_as_select
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import logging
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

def get_field(selector, by=By.ID, property = ''):
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

def get_elements(selector, by=By.XPATH, property = ''):
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
        logging.error(f'Erro ao obter {property} do element {element}! {err}')
        exit()

def get_capacity(index):
    try:
        capacity = get_field(f"//div[@id='listaAreaAtuacaovara']//li[{index}]//a", By.XPATH)
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

def start_procedures():
    # TO DO
    quit_frame()
    enter_frame()
    # build your logical reasoning #
    enter_iframe()

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
        if (".pdf") in file:
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

### ACTIONS ###

def open_projudi():
    HML = "http://10.47.76.126:8082/projudi/"
    #HML = "http://10.47.60.136:8082/projudi/"
    #PROD = "https://projudi.tjam.jus.br/projudi/"

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
            element = bot.find_element(selector, by, ensure_clickable=True)
            
            if element:
                element.click()
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

    # verifica se o processo foi encontrado
    error = bot.find_element('errorMessages', By.ID, waiting_time=2000)
    
    if error:
        register_log(f"Erro ao pesquisar o processo: {process}")
        print(f"Erro ao pesquisar o processo: {process}")

        return False
    
    # verifica se há o quadro de "ATENÇÃO"
    warning = verify_warning()

    if warning:
        register_log(f"Processo barrado: {process}")
        print(f"Processo barrado: {process}")

        return False
    
    # verifica se existe pendência no processo
    pending = verify_pending()

    if pending:
        register_log(f"Pendência no processo: {process}")
        print(f"Pendência no processo: {process}")

        return False
    
    return True

def verify_pending():
    click_element('quadroFilas')
    return bot.find_element('//label[contains(text(), "Restrição à Movimentação:")]', By.XPATH, waiting_time=2000)

def verify_warning():
    # click_element('warningMessages')
    return bot.find_element('warningMessages', By.ID, waiting_time=2000)

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
        exit()

def error_login():
    try:
        bot.find_element('errorMessages', By.ID, waiting_time=2000).click()
        logging.error('Erro ao efetuar login!')
    
        return True
    
    except Exception as err:
        logging.info('Login efetuado com sucesso!')
        print(err)

        return False

### EMAIL ###

def send_log_email():
    credentials = './gmail.json'
    gmail = BotEmailPlugin(credentials, environ["sender"])
    bcc = get_Bcc()
    to = get_Cc()

    subject = "Teste e-mail"
    body = "Teste de e-mail!\n\nFavor não responder."
    files = []

    gmail.send_message(
        subject, body, to, 
        bcc_addrs=bcc, 
        attachments=files, 
        use_html=False
    )

def get_Bcc():
    QUANT_COURTS = environ["quant_courts"]
    QUANT_COURTS = int(QUANT_COURTS)
    bcc = []

    for i in range(1, QUANT_COURTS+1):
        index = f'bcc{i}'
        bcc.append(environ[index])

    return bcc

def get_Cc():
    cc = []

    for i in range(1,3):
        index = f'cc{i}'
        cc.append(environ[index])

    return cc

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
    second_select.select_by_visible_text(text="ROBÔ - Aguardando Trânsito em Julgado")

    click_element("pesquisar")

    quit_frame()

def copy_all_processes_id():
    enter_frame()
    enter_iframe()

    ids = get_elements("em", by=By.TAG_NAME)
    list_ids = [element.text for element in ids]
    print(f"\nFirst 20 IDs: {list_ids}\n")

    while True:
        next_page = bot.find_element(selector='arrowNextOn', by=By.CLASS_NAME, waiting_time=2000)
        if not next_page:
            break # finished while loop
            
        else:
            next_page.click()
            
            ids = get_elements("em", by=By.TAG_NAME)
            new_ids = [element.text for element in ids]
            print(f'Inserting new processes ID: {new_ids}\n')
            
            list_ids.extend(new_ids)

    quit_frame()
    
    return list_ids
    

def intimate_each_process(listID):
    enter_frame()
    enter_iframe()

    for id in range(0, len(listID)):
        process = search_process(listID[id])

        if process is False:
            print("Processo com Restrição. Próximo!")

        else:
            bot.scroll_down(clicks=4)
            click_element(
                '/html/body/div[1]/div[2]/form/fieldset/table[3]/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[4]/b/a',
                by=By.XPATH    
            )

            # click_element('movimentarButton')
            # click_element('//*[@id="movimentarProcessoForm"]/fieldset/table[2]/tbody/tr/td[1]/a[1]', By.XPATH)

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

    for i in range(start_from, quantity_capacities+1):
        number_capacity = get_capacity(i)

        logging.info(f'Acessando lotação {number_capacity}!')
        register_log(f"Acessando lotação {number_capacity}!")

        # start_procedures() --> equivalent to the main() function

        # Search Advanced button #
        search_advanced_button()

        # Configuration Forms #
        config_forms()

        # Copy all Processes ID #
        list_ids = copy_all_processes_id()

        # Search Process by Process #
        intimate_each_process(listID=list_ids)
                
        del list_ids # "empty" the list content
        
        # Change Court
        logging.info(f'Encerrando acesso lotação {number_capacity}!')
        register_log(f"Encerrando acesso lotação {number_capacity}!")
        
        swith_capacities()
        # End RPA
        
    # remove_downloads()
    # send_log_email()
    move_files()

    logging.info('Execução finalizada com sucesso!')
    bot.stop_browser()

if __name__ == '__main__':
    load_dotenv()
    main()
