# -*- coding: utf-8 -*-
#! python3
#
# Este é um script simples que aplica a automação web e desktop simultaeamente
#
# This is a simple script that applies simultaneously the web and desktop automation

__author__ = 'Harold Alvarez'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Condition
import unittest
import lackey
import keyboard
from datetime import datetime


class TestAutomation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.4devs.com.br/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_automate_program(self):
        dados_pessoa = self.collect_data()
        r = lackey.Screen(0)    # define que a região de trabalho da biblioteca Lackey será toda a tela
        keyboard.send("win+r")
        r.wait(lackey.Pattern('janela_executar.png'), 30)   # espera até 30 segundos para localizar a imagem na tela
        r.click(lackey.Pattern('janela_executar.png'))
        keyboard.send("ctrl+a")     # seleciona tudo o que estiver escrito na caixa de texto na janela de execução
        keyboard.send("del")    # apaga o que foi selecionado
        keyboard.write("wordpad")
        r.click('btn_ok.png')
        r.wait(lackey.Pattern('wordpad.png'), 60)
        for chave, valor in dados_pessoa.items():   # lê todos os elementos do dicionário que tem os dados pessoais
            keyboard.write(chave + ' : ' + valor)
            keyboard.send("enter")

        r.wait(lackey.Pattern('btn_gravar.png'), 30)
        r.click(lackey.Pattern('btn_gravar.png'))
        r.wait(lackey.Pattern('txt_nome_arquivo.png'), 30)
        data_hora_atual = datetime.now().strftime('%d-%m-%y %H-%M')
        keyboard.write("Teste automação " + data_hora_atual)  # o nome do arquivo terá a data e hora atual
        r.click('btn_salvar.png')
        r.wait(lackey.Pattern("opcao_arquivo.png"), 30)
        r.click("opcao_arquivo.png")
        r.wait(lackey.Pattern("opcao_sair.png"), 30)
        r.click("opcao_sair.png")

    def collect_data(self):
        driver = self.driver
        dados_pessoa = {}
        driver.find_element_by_link_text("Gerador de Pessoas").click()
        driver.find_element_by_id("cep_estado").click()
        Select(driver.find_element_by_id("cep_estado")).select_by_visible_text("SP")
        driver.find_element_by_id("pontuacao_nao").click()
        driver.find_element_by_id("bt_gerar_pessoa").click()
        driver.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
        WebDriverWait(driver, 5).until(Condition.element_to_be_clickable((By.ID, "nome")))
        dados_pessoa['Nome'] = driver.find_element_by_id('nome').text
        dados_pessoa['CPF'] = driver.find_element_by_id("cpf").text
        dados_pessoa['Data Nascimento'] = driver.find_element_by_id("data_nasc").text
        dados_pessoa['CEP'] = driver.find_element_by_id("cep").text
        dados_pessoa['Endereço'] = driver.find_element_by_id("endereco").text
        dados_pessoa['Número'] = driver.find_element_by_id("numero").text
        dados_pessoa['Bairro'] = driver.find_element_by_id("bairro").text
        dados_pessoa['Cidade'] = driver.find_element_by_id("cidade").text
        dados_pessoa['Celular'] = driver.find_element_by_id("celular").text
        return dados_pessoa

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()