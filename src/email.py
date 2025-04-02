from os import environ
from botcity.plugins.email import BotEmailPlugin

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