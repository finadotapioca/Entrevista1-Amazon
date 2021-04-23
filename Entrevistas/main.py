from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os



def write_csv(ads):
    with open('Iphone-Amazon.csv','w',newline='', encoding = 'utf-8') as f:

        fields= ['Titulo','Preco']
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';',quoting=csv.QUOTE_MINIMAL)
        
        for ad in ads:
            writer.writerow(ad)
           

def converttoxlsx():
        df = pd.read_csv("Iphone-Amazon.csv",sep=';',index_col=False)
        df.to_excel("Iphone-Amazon.xlsx",header=["Titulo","Preco"], index=False)
        os.remove('Iphone-Amazon.csv')


def get_html(url):
    options = Options()
    options.headless = True
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(url)
    return browser.page_source


    

    


def scrape_data(card):
    try:
        h2 = card.h2
    except:
        title = ''
    else:
        title = h2.text.strip()

    try:       
        price = card.find('span', class_='a-offscreen').text
    except:
        price = ''
    else:
        price = card.find('span', class_='a-offscreen').text
    

    data = {'Titulo':title,  'Preco': price}

    return data


def main():
        url = 'https://www.amazon.com.br/s?k=iphone'
        html = get_html(url)

        soup = BeautifulSoup(html,'lxml')

        cards = soup.find_all('div', {'data-asin':True, 'data-component-type': 's-search-result'})
        
        ads_data = []
        for card in cards:
            data = scrape_data(card)
            ads_data.append(data)
        
        write_csv(ads_data)
        converttoxlsx()

      


if __name__ == '__main__':
    main()
