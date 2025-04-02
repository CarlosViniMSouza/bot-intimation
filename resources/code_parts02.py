# Select processID checkbox and movement button#
        enter_frame()
        enter_iframe()
        
        while True:
            checkbox_process = bot.find_element(selector="/html/body/div[1]/div[2]/form/table[2]/tbody/tr[1]/td[1]/input", by=By.XPATH, waiting_time=2000)

            if not checkbox_process:
                break # finished while loop

            click_element("/html/body/div[1]/div[2]/form/table[2]/tbody/tr[1]/td[1]/input", By.XPATH)
            click_element("movimentarEmLoteButton")
            
            dialog = bot.get_js_dialog()
            dialog.accept()

            quit_frame()

            bot.wait(2000)

            # Forms #
            enter_frame()
            enter_iframe()

            warning = verify_warning()

            if warning:
                print("Processo Fechado! Próxima citação!")
            else:
                click_element("nextButton") # Proximo Passo

                first_select = bot.find_element('//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/select', by=By.XPATH)
                first_select = element_as_select(first_select)
                first_select.select_by_index(index=2)

                checkbox = bot.find_element('//*[@id="idTipoPartesAdvogado0"]', by=By.XPATH)
                checkbox.click()

                number_days = 1
                bot.find_element('//*[@id="idTipoPartesAdvogado0"]', By.XPATH).send_keys(number_days)
                click_element("nextButton") # Proximo Passo

                second_select = bot.find_element('//*[@id="codLocalizador"]', by=By.XPATH)
                second_select = element_as_select(second_select)
                second_select.select_by_visible_text(text="Núcleo - RPV EXPEDIDO")
                click_element("nextButton") # Proximo Passo

                click_element('//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td/input[1]', By.XPATH)
                click_element('saveButton') # Botao Salvar

                ## Movimentação Múltipla (Arquivando) ##
                click_element("nextButton") # Proximo Passo

                first_select = bot.find_element('//*[@id="movimentacaoMultiplaForm"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/select', by=By.XPATH)
                first_select = element_as_select(first_select)
                first_select.select_by_index(index=4)

                click_element("arquivamentoDefinitivoS")

                click_element("nextButton") # Proximo Passo
                click_element("nextButton") # Proximo Passo
                click_element('saveButton') # Botao Salvar | Arquivamento Feito

                print("Intimação feita e processo arquivado! Voltado ao Forms da Busca Avançada!")

            quit_frame()