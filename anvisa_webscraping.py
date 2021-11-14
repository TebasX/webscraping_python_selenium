import time
import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://consultas.anvisa.gov.br/#/saneantes/produtos/q/?cnpj=03049181000139"

driver = webdriver.Chrome(executable_path="D:\projetos\codigos\webscraping_anvisa\chromedriver.exe")
driver.get(url)
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[3]/div[1]/form/div/div[2]/div/div/div/div/button[3]").click()

time.sleep(1)
all_rows = []

for n in range(5):
    if n > 0:
        driver.find_element_by_xpath("/html/body/div[3]/div[1]/form/div/div[2]/div/div/div/ul/li[7]/a").click()
        time.sleep(1) 

    element = driver.find_element_by_xpath("/html/body/div[3]/div[1]/form/div/div[2]/table/tbody")

    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    tbody=soup.find('tbody')
    body=tbody.find_all('tr')

    rows = body[1:]
    for row_num in range(len(rows)):
        row = []
        for row_item in rows[row_num].find_all('td'):
            aa = (row_item.text).strip()
            row.append(aa)
        all_rows.append(row)

head = body[0]
headings = []

for item in head.find_all('th'):
    item = (item.text).rstrip("\n")
    headings.append(item)

df = pd.DataFrame(data=all_rows,columns=headings)
df = df.drop("",axis=1)
df.to_json("D:\projetos\codigos\webscraping_anvisa\produtos.json", orient="records")

driver.quit()

g = open("D:\projetos\codigos\webscraping_anvisa\produtos.json")
f = open("D:\projetos\codigos\webscraping_anvisa\listaatual.json")

data_orig = json.load(f)
data_new = json.load(g)

f.close()
g.close()

is_diferent = 0

for i in range(len(data_new)):
    if data_new[i] not in data_orig:
        print("o produto " + data_new[i]['Nome do Produto'] + " foi adicionado \n")
        is_diferent = is_diferent + 1

print(is_diferent)

if is_diferent > 0:
    os.remove("D:\projetos\codigos\webscraping_anvisa\listaatual.json")
    old_name = "D:\projetos\codigos\webscraping_anvisa\produtos.json"
    new_name = "D:\projetos\codigos\webscraping_anvisa\listaatual.json"
    os.rename(old_name, new_name)

else:
    print("não há produtos novos")
    os.remove("D:\projetos\codigos\webscraping_anvisa\produtos.json")
