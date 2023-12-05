from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse as urlparse
from anticaptchaofficial.recaptchav2proxyless import *
from anticaptchaofficial.recaptchav3proxyless import *
from urllib.parse import parse_qs

def getOptions():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

url='https://www.tse.jus.br/eleitor/titulo-e-local-de-votacao/consulta-por-nome/'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=getOptions())
driver.get(url)

time.sleep(45)

dados_list = []
dados = {}

infoset = [{'cpf':'12811607684','dataNascimento':'24/07/1996','nomeMae':"Marilene de Carvalho Clemente Oliveira"}]

def runScrapper(p):
    
    try:
        aceitarButton = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/div[2]/button')
        aceitarButton.click()
    except:
        print("XPATH not found")
        pass
        
    cpfTextBox = driver.find_element(By.ID, "LV_NomeTituloCPF")
    cpfTextBox.send_keys(p['cpf'])

    dataNascimentoTextBox = driver.find_element(By.ID, "LV_DataNascimento")
    dataNascimentoTextBox.send_keys(p['dataNascimento'])

    dataNascimentoTextBox = driver.find_element(By.ID, "LV_NomeMae")
    dataNascimentoTextBox.send_keys(p['nomeMae'])

    dataNascimentoTextBox = driver.find_element(By.ID, "consultar-local-votacao-form-submit")
    dataNascimentoTextBox.click()
    time.sleep(30)

    ret = dict()
    
    zonaSecao = driver.find_element(By.XPATH, "/html/body/main/div/div/article/div/article/main/section/div[10]/p[5]")
    info = zonaSecao.text.split()
    ret["zona"] = info[1]
    ret["secao"] = info[3]

    local = driver.find_element(By.XPATH, "/html/body/main/div/div/article/div/article/main/section/div[10]/p[6]")
    coll = local.text.find(':')
    ret["local"] = local.text[coll + 1:]
    
    endereco = driver.find_element(By.XPATH, "/html/body/main/div/div/article/div/article/main/section/div[10]/p[7]")
    coll = endereco.text.find(':')
    ret["endereco"] = endereco.text[coll + 1:]

    municipio = driver.find_element(By.XPATH, "/html/body/main/div/div/article/div/article/main/section/div[10]/p[8]")
    coll = municipio.text.find(':')
    ret["municipio"] = municipio.text[coll + 1:]

    print(ret)
    return ret

runScrapper(infoset[0])