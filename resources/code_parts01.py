        # Copy all Processes ID #
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

        # Search Process by Process #
        enter_frame()
        enter_iframe()

        for id in range(0, len(list_ids)):
            process = search_process(list_ids[id])

            if process is False:
                print("Processo com Restrição. Próximo!")

            else:
                bot.scroll_down(clicks=4)
                click_element(
                    '/html/body/div[1]/div[2]/form/fieldset/table[3]/tbody/tr[2]/td/div/div/div/table/tbody/tr[1]/td[4]/b/a',
                    by=By.XPATH    
                )
                click_element('movimentarButton')
                click_element('//*[@id="movimentarProcessoForm"]/fieldset/table[2]/tbody/tr/td[1]/a[1]', By.XPATH)
                
        # Change Court