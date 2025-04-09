### EMAIL ###
from botcity.plugins.email import BotEmailPlugin
from src.getters import get_current_day

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
    files = [rf'C:\Users\Carlos_Souza\Documents\projects\bot_issue_inss\logging\{CURRENT_DAY}\{CURRENT_DAY} - log_operacao.txt']

    email.send_message(subject, body, to, attachments=files, use_html=False)
    email.disconnect()
