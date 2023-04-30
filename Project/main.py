from lxml import etree
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import itertools

#Headers della richiesta URL via request
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#url di prova
mesi=["Giugno","Settembre","Maggio"]
luoghi=["Itri","Formia","Gaeta","Sperlonga"]
anni=list(range(1995,2023))



def get_combinations_of_search():
    mesi=["Giugno","Settembre","Maggio"]
    luoghi=["Itri","Formia","Gaeta","Sperlonga"]
    anni=list(range(1995,2023))
    a=[luoghi,anni,mesi]
    

    a=list(itertools.product(*a))
    
    return a

def get_cols(urls,xpath):
    colonne=[]
    for url_res in urls:
        url=url_res[0]
        res=url_res[1]
        if res==0:
            req=requests.get(url,headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            dom = etree.HTML(str(soup))
            table=dom.xpath(xpath)
            elements_colonne=list(table[0][0])
            colonne=[]
            for i in list(elements_colonne):
                colonne.append(i.text)
            break
        
    return colonne

            
def get_data(urls):

    xPath='//*[@id="table-meteo-archivio"]'
    columns=get_cols(urls,xPath)
    print(columns)
    

            

    '''
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    dom = etree.HTML(str(soup))

    #XPaths
    xPath_colonne='//*[@id="table-meteo-archivio"]'

    table=dom.xpath(xPath_colonne)
    #formato tabella->[indice tabella][indice riga][indice colonna]

    #COLONNE
    elements_colonne=list(table[0][0])
    colonne=[]
    for i in list(elements_colonne):
        colonne.append(i.text)

    print(colonne)

    #RIGHE
    numero_righe=len(list(table[0]))-1
    print("Numero di righe",numero_righe)
    #creazione righe
    rows=[]
    for i in range(1,numero_righe):
        elements_righe=list(table[0][i])
        row=[]
        
        for i in elements_righe:
            row.append(i.text)
        rows.append(row)


    data=pd.DataFrame(data=rows,columns=colonne)
    print(data.head(10))
    '''


def prep_URL(url,comb):
    urls=[]
    for i in comb:
        citta,anno,mese=i
        sing_url=url+citta+'/'+str(anno)+'/'+mese
        urls.append(sing_url)
    
    data=pd.DataFrame(data=urls,columns=['url'])
    return data
import time
def get_ok_urls(urls):
    url2res=[]
    for url in urls:
        if url!='url':
            print(url)
            req = requests.get(url, headers)
            status=req.status_code

            print("[REQUEST URL]",url)
            print("[RESPONSE]",status)
            if status==200:
                res=1
            else:
                res=0
            
            url2res.append([url,res])
            time.sleep(0)

    

    data=pd.DataFrame(data=url2res,columns=['url','stat'])
    data.to_csv('url2StateReq.csv',index=False)

def read_ok_urls(path):
    urls_ok=[]
    with open(path,'r') as f:
        for line in f.readlines():
            line=f.readline()
            urls_ok.append(line)
    return urls_ok
        
        


if __name__=="__main__":
    url_vero="https://www.ilmeteo.it/portale/archivio-meteo/Sperlonga/2009/Giugno"
    url_base="https://www.ilmeteo.it/portale/archivio-meteo/"
    

    #PREPARAZIONE

    #comb=get_combinations_of_search()
    #getURLS=prep_URL(url_base,comb)
    
    #getURLS.to_csv('urls.csv',index=False)
    get_links=pd.read_csv('urls.csv')

    print(get_links.head(10))
    

    

    ok_urls=get_ok_urls(get_links['url'])
    #devo filtrare i code non accessibili

    #ok_urls=read_ok_urls('fileok.txt')
    #print(getURLS)
    

    
    #get_data(getURLS)