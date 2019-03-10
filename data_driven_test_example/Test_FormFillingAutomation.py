# -*- coding: utf-8 -*-
#! python3
#
# Este é um script de automação web que usa os conceitos data-driven testing e web scraping para gerar dinamicamente
# os dados de entrada, e interage com mais de uma aba no navegador de internet
#
# This is a web automation script that uses data-driven and web scraping concepts to generate dynamically the input
# data, and interacts with more than one tab on the web browser

__author__ = 'Harold Alvarez'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Condition
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import unittest
import random
import sys
import time

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://demo.automationtesting.in/Register.html")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.execute_script("window.open('https://www.4devs.com.br/');")

    def test_fill_registration_form(self):
        driver = self.driver
        self.resultado = {}
        self.resultado[0] = "Nome pessoa                        R. esperado   R. obtido"
        try:
            for n in range(self.quantity):
                dados_pessoa = self.web_scraping()
                # depois que o script coleta os dados na segunda aba, volta para a primeira
                driver.switch_to.window(driver.window_handles[0])
                if n > 0:   # se é maior que 0 já fez o primeiro cadastro, e precisa clicar novamente na opção "Register"
                    driver.find_element_by_link_text("Register").click()

                if dados_pessoa['Genero'] == 'H':
                    genero_selecionado = 'Male'
                else:
                    genero_selecionado = 'FeMale'

                lista_paises = Select(driver.find_element_by_id("countries")).options
                lista_paises2 = Select(driver.find_element_by_css_selector("select#country")).options
                lista_hobbies = driver.find_elements_by_class_name("checks")
                lista_skills = Select(driver.find_element_by_id("Skills")).options
                lista_idiomas = driver.find_elements_by_css_selector("a.ui-corner-all")
                # começa na posição 1 porque a posição 0 tem o valor inválido "Select Country"
                pais_selecionado = lista_paises[random.randrange(1,len(lista_paises))].text
                pais_selecionado2 = lista_paises2[random.randrange(1,len(lista_paises2))].text
                hobbie_selecionado = lista_hobbies[random.randrange(len(lista_hobbies))].text
                habilidade_selecionada = lista_skills[random.randrange(1,len(lista_skills))].text
                data_nascimento = datetime.strptime(dados_pessoa['Data Nascimento'],'%d/%m/%Y')
                ano_nascimento = dados_pessoa['Data Nascimento'][6:]
                mes_nascimento = data_nascimento.strftime('%B')
                dia_nascimento = str(int(dados_pessoa['Data Nascimento'][0:2]))     #tira o zero à esquerda, se houver
                nome_dividido = dados_pessoa['Nome'].split()
                nomes = nome_dividido[:-1]
                # verifica se o último nome da lista é parte de um sobrenome. Exemplo: da Silva, de Oliveira, etc.
                if nomes[-1] == "da" or nomes[-1] == "do" or nomes[-1] == "das" or nomes[-1] == "dos" or nomes[-1] == "de":
                    sobrenome = nomes.pop() + " " + nome_dividido[-1]
                else:
                    sobrenome = nome_dividido[-1]

                nome_formatado = ""
                for i in range(len(nomes)):
                    nome_formatado = nome_formatado + " " + nomes[i]

                # Se o número é par, o cadastro deve dar sucesso, caso contrário o cadastro falha
                if n % 2 == 0:
                    senha = dados_pessoa["Senha"] + str(random.randint(1,10))   # coloca um número na senha, porque às vezes não tem
                    self.resultado[n+1] = dados_pessoa["Nome"].ljust(35) + "Passar".ljust(14)
                else:
                    senha = ""  # senha em branco propositalmente, para o cadastro falhar
                    self.resultado[n+1] = dados_pessoa["Nome"].ljust(35) + "Falhar".ljust(14)

                driver.find_element_by_xpath("//input[@placeholder='First Name']").click()
                driver.find_element_by_xpath("//input[@placeholder='First Name']").clear()
                driver.find_element_by_xpath("//input[@placeholder='First Name']").send_keys(nome_formatado)
                driver.find_element_by_xpath("//input[@placeholder='Last Name']").click()
                driver.find_element_by_xpath("//input[@placeholder='Last Name']").clear()
                driver.find_element_by_xpath("//input[@placeholder='Last Name']").send_keys(sobrenome)
                driver.find_element_by_xpath("//*[@ng-model='Adress']").click()
                driver.find_element_by_xpath("//*[@ng-model='Adress']").clear()
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(dados_pessoa['Endereço'])
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(Keys.ENTER)
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(dados_pessoa['Número'])
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(Keys.ENTER)
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(dados_pessoa['Bairro'])
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(Keys.ENTER)
                driver.find_element_by_xpath("//*[@ng-model='Adress']").send_keys(dados_pessoa['Cidade'])
                driver.find_element_by_xpath("//*[@ng-model='EmailAdress']").click()
                driver.find_element_by_xpath("//*[@ng-model='EmailAdress']").clear()
                driver.find_element_by_xpath("//*[@ng-model='EmailAdress']").send_keys(dados_pessoa['Email'])
                driver.find_element_by_xpath("//*[@ng-model='Phone']").click()
                driver.find_element_by_xpath("//*[@ng-model='Phone']").clear()
                driver.find_element_by_xpath("//*[@ng-model='Phone']").send_keys(dados_pessoa['Telefone'])
                driver.find_element_by_xpath(f"//input[@type='radio' and @value= '{genero_selecionado}']").click()
                driver.find_element_by_xpath(f"//input[@type='checkbox' and @value= '{hobbie_selecionado}']").click()
                driver.find_element_by_id("msdd").click()
                for i in range(3):
                    idioma_selecionado = lista_idiomas[random.randrange(len(lista_idiomas))].text
                    driver.find_element_by_link_text(idioma_selecionado).click()

                driver.find_element_by_tag_name("body").click()
                driver.find_element_by_id("Skills").click()
                Select(driver.find_element_by_id("Skills")).select_by_value(habilidade_selecionada)
                driver.find_element_by_id("countries").click()
                Select(driver.find_element_by_id("countries")).select_by_visible_text(pais_selecionado)
                driver.find_element_by_css_selector("span.select2-selection__arrow").click()
                Select(driver.find_element_by_css_selector("select#country")).select_by_value(pais_selecionado2)
                driver.find_element_by_id("yearbox").click()
                Select(driver.find_element_by_id("yearbox")).select_by_visible_text(ano_nascimento)
                driver.find_element_by_xpath("//*[@ng-model='monthbox']").click()
                Select(driver.find_element_by_xpath("//*[@ng-model='monthbox']")).select_by_visible_text(mes_nascimento)
                driver.find_element_by_id("daybox").click()
                Select(driver.find_element_by_id("daybox")).select_by_visible_text(dia_nascimento)
                driver.find_element_by_id("firstpassword").click()
                driver.find_element_by_id("firstpassword").clear()
                driver.find_element_by_id("firstpassword").send_keys(senha)
                driver.find_element_by_id("secondpassword").clear()
                driver.find_element_by_id("secondpassword").send_keys(senha)
                driver.find_element_by_id("submitbtn").click()
                # se o registro foi feito com sucesso o sistema redireciona o usuário para a página °Web Table°
                time.sleep(5)
                if "Web Table" == driver.title:
                    self.resultado[n+1] = self.resultado[n+1] + " Passou"
                else:
                    self.resultado[n+1] = self.resultado[n+1] + " Falhou"

        except WebDriverException as excecao:
            raise excecao

    def web_scraping(self):
        driver = self.driver
        driver.switch_to.window(driver.window_handles[1])
        dados_pessoa = {}
        genero = ('H', 'M')
        genero_selecionado = random.choice(genero)
        WebDriverWait(driver, 10).until(Condition.element_to_be_clickable((By.LINK_TEXT, "Gerador de Pessoas")))
        driver.find_element_by_link_text("Gerador de Pessoas").click()
        driver.find_element_by_xpath(f"//input[@type='radio' and @value= '{genero_selecionado}']").click()
        idades = Select(driver.find_element_by_id("idade")).options
        idade_selecionada = idades[random.randrange(len(idades))].text
        driver.find_element_by_id("idade").click()
        Select(driver.find_element_by_id("idade")).select_by_value(idade_selecionada)
        lista_estados = Select(driver.find_element_by_id("cep_estado")).options
        estado_selecionado = lista_estados[random.randrange(1,len(lista_estados))].text
        driver.find_element_by_id("cep_estado").click()
        Select(driver.find_element_by_id("cep_estado")).select_by_value(estado_selecionado)
        driver.find_element_by_id("pontuacao_nao").click()
        while True:
            driver.find_element_by_id("bt_gerar_pessoa").click()
            # se algum dos campos a seguir estiver vazio, o script volta a clicar no botão "Gerar Pessoa"
            if not driver.find_element_by_id('nome').text or \
               not driver.find_element_by_id('data_nasc').text or \
               not driver.find_element_by_id('endereco').text or \
               not driver.find_element_by_id('email').text or \
               not driver.find_element_by_id('senha').text or \
               not driver.find_element_by_id('telefone_fixo').text:
                continue
            break

        driver.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
        WebDriverWait(driver, 5).until(Condition.element_to_be_clickable((By.ID, "nome")))
        dados_pessoa['Nome'] = driver.find_element_by_id('nome').text
        dados_pessoa['Data Nascimento'] = driver.find_element_by_id("data_nasc").text
        dados_pessoa['Genero'] = genero_selecionado
        dados_pessoa['Endereço'] = driver.find_element_by_id("endereco").text
        dados_pessoa['Número'] = driver.find_element_by_id("numero").text
        dados_pessoa['Bairro'] = driver.find_element_by_id("bairro").text
        dados_pessoa['Cidade'] = driver.find_element_by_id("cidade").text
        dados_pessoa['Email'] = driver.find_element_by_id("email").text
        dados_pessoa['Senha'] = driver.find_element_by_id("senha").text
        dados_pessoa['Telefone'] = driver.find_element_by_id("telefone_fixo").text
        return dados_pessoa

    def tearDown(self):
        self.driver.quit()
        for chave, valor in self.resultado.items():
            print(self.resultado[chave])


if __name__ == "__main__":
    if len(sys.argv) < 2:  # se é menor que 2, não foi passado nenhum argumento da quantidade de cadastros a fazer
        TestRegistration.quantity = 1
    else:
        TestRegistration.quantity = int(sys.argv.pop())  # tira o último item da lista e o move para a variável quantity

    unittest.main()
