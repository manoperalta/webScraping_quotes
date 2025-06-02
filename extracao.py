from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium import webdriver
import pandas as pd
import json
import csv
import os
import time


def screenShot(link, data_inicio=None):
    os.makedirs("screenshot", exist_ok=True)
    nome_arquivo = f"screenshot_{data_inicio}.png" if data_inicio else "screenshot.png"
    caminho = os.path.join("screenshot", nome_arquivo)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(link)
    driver.save_screenshot(caminho)
    driver.quit()


import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def scanPage(link_inicial, max_paginas=10):
    link_atual = link_inicial
    pagina = 1
    resultados = []
    inicio_execucao = time.time()
    data_inicio = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    while pagina <= max_paginas and link_atual:
        response = requests.get(link_atual)
        site_parser = BeautifulSoup(response.text, 'html.parser')
        quotes = site_parser.find_all("div", class_="quote")

        status = response.status_code
        print(f"[Página {pagina}] Status: {status} - {response.reason}")

        if status != 200:
            print(f"Erro no request: {status}")
            break

        
        if pagina == 1:
            screenShot(link_atual, data_inicio=data_inicio)

        for quote in quotes:
            citacao = quote.find("span", class_="text").get_text()
            autor = quote.find("small", class_="author").get_text()
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            duracao_execucao = round(time.time() - inicio_execucao, 2)

            print(f"Citação: {citacao}")
            print(f"Autor: {autor}")
            print(f"Tags: {', '.join(tags)}")
            print("-" * 50)

            resultados.append({
                "pagina": pagina,
                "time": duracao_execucao,
                "citacao": citacao,
                "autor": autor,
                "tags": ", ".join(tags)
            })

        proximo = site_parser.find("li", class_="next")
        if proximo:
            proximo_href = proximo.find("a")["href"]
            link_atual = urljoin(link_atual, proximo_href)
            pagina += 1
        else:
            break  

    
    df = pd.DataFrame(resultados)
    duracao_total = round(time.time() - inicio_execucao, 2)

    print(f"Execução iniciada em: {data_inicio}")
    print(f"Duração total: {duracao_total} segundos")
    print(f"Páginas varridas: {pagina}")

    link_slug = link_inicial.replace("http://", "").replace("/", "_")
    nome_base = f"resultado_scan_{link_slug}_{data_inicio}"

    os.makedirs("resultados", exist_ok=True)
    caminho_csv = os.path.join("resultados", f"{nome_base}.csv")
    caminho_json = os.path.join("resultados", f"{nome_base}.json")

    df.to_csv(caminho_csv, index=False)
    df.to_json(caminho_json, orient="records", force_ascii=False, indent=4)

    print(f"Arquivos salvos:\n {caminho_csv}\n {caminho_json}")




def findAutor(link, autor_busca=None):
    
    inicio_execucao = time.time()
    data_inicio = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    response = requests.get(link)
    print(f"Status: {response.status_code} - {response.reason}")

    if response.status_code != 200:
        print(f"Erro ao acessar a página: {response.status_code}")
        return
    else:
        screenShot(link,data_inicio=data_inicio)
        soup = BeautifulSoup(response.text, "html.parser")
        blocos_citacoes = soup.find_all("div", class_="quote")

        resultados = []

        for bloco in blocos_citacoes:
            citacao = bloco.find("span", class_="text").get_text()
            autor = bloco.find("small", class_="author").get_text()
            tags = [tag.text for tag in bloco.find_all("a", class_="tag")]

            if autor_busca and autor.lower() != autor_busca.lower():
                continue

            resultados.append({
                "citacao": citacao,
                "autor": autor,
                "tags": ", ".join(tags)
            })

            print(f"Citação: {citacao}")
            print(f"Autor: {autor}")
            print(f"Tags: {', '.join(tags)}")
            print("-" * 50)

        
        df = pd.DataFrame(resultados)

        
        duracao_execucao = round(time.time() - inicio_execucao, 2)
        print(f"Execução iniciada em: {data_inicio}")
        print(f"Duração total: {duracao_execucao} segundos")

        nome_autor = autor_busca.replace(" ", "_") if autor_busca else "todos"
        nome_base = f"resultado_{nome_autor}_{data_inicio}"

        os.makedirs("resultados", exist_ok=True)
        caminho_csv = os.path.join("resultados", f"{nome_base}.csv")
        caminho_json = os.path.join("resultados", f"{nome_base}.json")
        df.to_csv(caminho_csv, index=False)
        df.to_json(caminho_json, orient="records", force_ascii=False, indent=4)
        print(f"Arquivos salvos:\n {caminho_csv}\n {caminho_json}")


def findTags(link, tag_busca=None):
    inicio_execucao = time.time()
    data_inicio = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    response = requests.get(link)
    print(f"Status: {response.status_code} - {response.reason}")

    if response.status_code != 200:
        print(f"Erro ao acessar a página: {response.status_code}")
        return
    else:
        screenShot(link, data_inicio=data_inicio)
        soup = BeautifulSoup(response.text, "html.parser")
        blocos_citacoes = soup.find_all("div", class_="quote")

        resultados = []

        for bloco in blocos_citacoes:
            citacao = bloco.find("span", class_="text").get_text()
            autor = bloco.find("small", class_="author").get_text()
            tags = [tag.text for tag in bloco.find_all("a", class_="tag")]

           
            if tag_busca and tag_busca.lower() not in [t.lower() for t in tags]:
                continue

            resultados.append({
                "citacao": citacao,
                "autor": autor,
                "tags": ", ".join(tags)
            })

            print(f"Citação: {citacao}")
            print(f"Autor: {autor}")
            print(f"Tags: {', '.join(tags)}")
            print("-" * 50)

        
        df = pd.DataFrame(resultados)

        duracao_execucao = round(time.time() - inicio_execucao, 2)
        print(f"Execução iniciada em: {data_inicio}")
        print(f"Duração total: {duracao_execucao} segundos")

        nome_tag = tag_busca.replace(" ", "_") if tag_busca else "todas"
        nome_base = f"resultado_tag_{nome_tag}_{data_inicio}"

        os.makedirs("resultados", exist_ok=True)
        caminho_csv = os.path.join("resultados", f"{nome_base}.csv")
        caminho_json = os.path.join("resultados", f"{nome_base}.json")

        df.to_csv(caminho_csv, index=False)
        df.to_json(caminho_json, orient="records", force_ascii=False, indent=4)

        print(f"Arquivos salvos:\n {caminho_csv}\n {caminho_json}")
        

scanPage("http://quotes.toscrape.com", max_paginas=10)
findAutor("http://quotes.toscrape.com/", autor_busca="Albert Einstein")
findTags("http://quotes.toscrape.com/", tag_busca="humor")

