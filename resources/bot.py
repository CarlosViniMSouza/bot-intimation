from botcity.web import WebBot, Browser, By
from botcity.plugins.gmail import BotGmailPlugin # type: ignore
from webdriver_manager.firefox import GeckoDriverManager

import logging
from os import makedirs, listdir, rename, environ, path, remove
from os.path import isdir
from dotenv import load_dotenv
from datetime import date

bot = WebBot()
logging.basicConfig(filename='templateProjudi.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info('Iniciando execução!')

    try:
        abrirProjudi()
    except Exception as err:
        logging.error(f'Erro abrir o Projudi! {err}')
        exit()

    logar()
    criarDiretorio()

    try:
        lotacoes = obterElementos('//div[@id="listaAreaAtuacaovara"]//li//a', By.XPATH)
        qtdeLotacoes = len(lotacoes)
    except Exception as err:
        logging.error(f'Erro ao carregar lotações! {err}')
        exit()

    iniciarDe = environ["iniciarDe"]
    iniciarDe = int(iniciarDe)

    for i in range(iniciarDe, qtdeLotacoes+1):
        nmLotacao = obterLotacao(i)
        logging.info(f'Acessando lotação {nmLotacao}!')
        registrarLog(f"Acessando lotação {nmLotacao}")

        iniciarProcedimentos()

        logging.info(f'Encerrando acesso lotação {nmLotacao}!')
        registrarLog(f"Encerrando acesso na lotação {nmLotacao}")
        alternarLotacao()
    
    excluirBaixados()
    enviarLogEmail()
    moveArquivos()
    logging.info('Execução finalizada com sucesso!')
    bot.stop_browser()

def abrirProjudi():
    #HML = "http://10.47.60.136:8082/projudi/"
    HML = "http://10.47.76.126:8082/projudi/"
    #PROD = "https://projudi.tjam.jus.br/projudi/"
    bot.headless = False
    bot.browser = Browser.FIREFOX
    bot.driver_path = GeckoDriverManager().install()
    bot.browse(HML)
    bot.maximize_window()

def entrarFrame():
    frame = obterCampo('mainFrame')
    bot.enter_iframe(frame)

def entrarIframe():
    iframe = obterCampo('userMainFrame', By.NAME)
    bot.enter_iframe(iframe)

def entrarIframeId():
    iframe = obterCampo('//iframe[contains(@name,"window")]', By.XPATH)
    bot.enter_iframe(iframe)

def sairFrame():
    bot.leave_iframe()

def clickElement(seletor, by=By.ID):
    try:
        tentativas = 20
        achou = False
        while not achou and tentativas > 0:
            elemento = bot.find_element(seletor, by, ensure_clickable=True)
            if elemento:
                elemento.click()
                achou = True
            else:
                tentativas -= 1
    except Exception as err:
        logging.error(f'Erro ao clicar no elemento {seletor}! {err}')
        exit()

def obterCampo(seletor, by=By.ID, propriedade = ''):
    try:
        tentativas = 20
        achou = False
        while not achou and tentativas > 0:
            elemento = bot.find_element(seletor, by, ensure_clickable=True)
            if elemento:
                achou = True
            else:
                tentativas -= 1
            
        if propriedade == '':
            return elemento
        else:
            return elemento.get_property(propriedade)
    except Exception as err:
        logging.error(f'Erro ao obter {seletor}! {err}')

def obterElementos(seletor, by=By.XPATH, propriedade = ''):
    try:
        achou = False
        tentativas = 20
        while not achou and tentativas > 0:
            elementos = bot.find_elements(seletor, by)
            if elementos:
                achou = True
            else:
                tentativas -= 1
        
        if propriedade == '':
            return elementos
        else:
            elementosPropriedade = []
            for elemento in elementos:
                valor = elemento.get_property(propriedade)
                if type(valor) == str:  # noqa: E721
                    valor = valor.strip()
                elementosPropriedade.append(valor)
            return elementosPropriedade

    except Exception as err:
        logging.error(f'Erro ao buscar os elementos! {err}')
        exit()

def obterConteudo(elemento, propriedade='textContent'):
    try:
        valor = elemento.get_property(propriedade)
        return valor.strip()
    except Exception as err:
        logging.error(f'Erro ao obter {propriedade} do elemento {elemento}! {err}')
        exit()

def logar():
    try:
        entrarFrame()
        clickElement('login')
        bot.paste(environ["usuario"])
        bot.tab()
        bot.paste(environ["senha"])
        bot.enter()
        if erroLogin():
            exit()
        sairFrame()
    except Exception as err:
        logging.error(f'Erro ao efetuar login! {err}')
        exit()

def erroLogin():
    try:
        bot.find_element('errorMessages', By.ID, waiting_time=2000).click()
        logging.error('Erro ao efetuar login!')
        return True
    except:  # noqa: E722
        logging.info('Login efetuado com sucesso!')
        return False

def obterLotacao(index):
    try:
        lotacao = obterCampo(f"//div[@id='listaAreaAtuacaovara']//li[{index}]//a", By.XPATH)
        nmLotacao = lotacao.get_property('title')
        lotacao.click()
        return nmLotacao
    except Exception as err:
        logging.error(f'Erro ao obter lotação! {err}')
        exit()

def alternarLotacao():
    try:
        sairFrame()
        entrarFrame()
        entrarIframe()
        clickElement('alterarAreaAtuacao')
        entrarIframeId()
    except Exception as err:
        logging.error(f'Erro ao alternar lotação! {err}')
        exit()

def buscarProcesso(processo):
    sairFrame()
    entrarFrame()
    entrarIframe()
    clickElement('processoBusca')
    print(f"Robô atuando no processo {processo}")
    logging.info(f"Robô atuando no processo {processo}")
    bot.paste(processo)
    bot.enter()
    bot.enter()
    # verifica se o processo foi encontrado
    erro = bot.find_element('errorMessages', By.ID, waiting_time=2000)
    if erro:
        registrarLog(f"Erro ao pesquisar o processo: {processo}")
        print(f"Erro ao pesquisar o processo: {processo}")
        return False
    # verifica se existe pendência no processo
    pendencia = verificarPendencia()
    if pendencia:
        registrarLog(f"Pendência no processo: {processo}")
        print(f"Pendência no processo: {processo}")
        return False
    return True

def verificarPendencia():
    clickElement('quadroFilas')
    return bot.find_element('//label[contains(text(), "Restrição à Movimentação:")]', By.XPATH, waiting_time=1000)

def iniciarProcedimentos():
    # TO DO
    sairFrame()
    entrarFrame()
    # se precisar acessar menu do sistema, inserir o código antes da chamada do método entrarIframe()
    entrarIframe()

def criarDiretorio():
    try:
        DIRETORIO = getDiretorio()
        if not isdir(DIRETORIO):
            makedirs(DIRETORIO)
        entrarFrame()
    except Exception as err:
        logging.error(f'Erro ao criar diretório do arquivo de saída para o usuário! {err}')
        exit()

def getDataAtual():
    return str(date.today())

def getDiretorio():
    data = getDataAtual()
    return './logs/' + data

def registrarLog(msg):
    DATA_ATUAL = getDataAtual()
    ARQUIVO = DATA_ATUAL + ' - log_operacao.txt'
    with open(ARQUIVO, "a") as f:
        print(msg, file=f)

def excluirBaixados():
    try:
        arquivos = listdir('./')
        if len(arquivos) == 0:
            logging.warning('Não há arquivos para excluir!')
        else:
            for arquivo in arquivos:
                if arquivo.endswith('.pdf'):
                    caminho = path.join('./', arquivo)
                    if path.isfile(caminho):
                        remove(caminho)
            logging.info('Arquivos excluídos com sucesso!')
    except Exception as err:
        logging.error(f'Erro ao excluir arquivos! {err}')
        exit()

def moveArquivos():
    DIRETORIO = getDiretorio()
    DATA_ATUAL = getDataAtual()
    listaArquivos = listdir('./')
    arquivoLog = DATA_ATUAL + ' - log_operacao.txt'
    for arquivo in listaArquivos:
        if (".pdf") in arquivo:
            rename(f"./{arquivo}", f"{DIRETORIO}/{arquivo}")
        if arquivoLog in arquivo:
            rename(f"./{arquivo}", f"{DIRETORIO}/{arquivo}")

def enviarLogEmail():
    credentials = './gmail.json'
    gmail = BotGmailPlugin(credentials, environ['remetente'])
    bcc = obterBcc()
    to = obterCc()
    subject = "Teste e-mail"
    body = "Teste de e-mail!\n\nFavor não responder."
    files = []
    gmail.send_message(subject, body, to, bcc_addrs=bcc, attachments=files, use_html=False)

def obterBcc():
    QTDE_VARAS = environ['qtdeVaras']
    QTDE_VARAS = int(QTDE_VARAS)
    bcc = []
    for i in range(1,QTDE_VARAS+1):
        indice = f'bcc{i}'
        bcc.append(environ[indice])
    return bcc

def obterCc():
    cc = []
    for i in range(1,3):
        indice = f'cc{i}'
        cc.append(environ[indice])
    return cc

if __name__ == '__main__':
    load_dotenv()
    main()
