from botcity.web import By, element_as_select

from src.frames import enter_frame, quit_frame, enter_iframe
from src.actions import click_element, search_process
from src.getters import get_field, get_elements

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

def copy_all_processes_id(bot):
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
    
def intimate_each_process(bot, listID):
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
