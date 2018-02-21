import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from summa import summarizer
import time

def getElTiempoArticles(sDate): #sDate string structure example: 19/02/18
    stdDate = time.strptime(sDate, "%d/%m/%y")

    page = requests.get("http://www.eltiempo.com/politica")
    soup = BeautifulSoup(page.content, "html.parser")

    tempListArticlesInfo_html = soup.select(".notas-secundarias-bk .informacion") #!
    listArticlesInfo_html = list() #Articles with same date as sDate will be saved here
    listOfArticles = list() #Final list of articles

# Saving only  article html files that correspond to the given date #

    for numPage in range(3): #Search till page 2 of "more news"

        for i in range(len(tempListArticlesInfo_html)):
            articleDate = tempListArticlesInfo_html[i].select(".seccion-fecha meta[itemprop=datePublished]")[0]["content"] #format: yyyy-mm-dd
            stdArticleDate = time.strptime(articleDate, "%Y-%m-%d")

            if(stdArticleDate == stdDate):
                listArticlesInfo_html.append(tempListArticlesInfo_html[i]);
                
        page = requests.get("http://www.eltiempo.com/category/latest/politica/" + str(numPage))        
        soup = BeautifulSoup(page.content, "html.parser")
        tempListArticlesInfo_html = soup.select(".listing .informacion") #!

# Getting and saving formated data #

    for i in range(len(listArticlesInfo_html)):
        date = listArticlesInfo_html[i].select(".seccion-fecha meta[itemprop=datePublished]")[0]["content"]

        titulo_html = listArticlesInfo_html[i].find(class_="titulo")
        titulo = titulo_html.get_text(strip=True)
        link = 'http://www.eltiempo.com' + titulo_html.find('a')["href"]

        textPage = requests.get(link)
        textSoup = BeautifulSoup(textPage.content, "html.parser")
        text_html = textSoup.select(".articulo-contenido p.contenido")
        #del text_html[-1] # delete last entry: Info about author
        text = ""
        for j in range(len(text_html)):
            text += "\n" +  text_html[j].get_text()


        article = {'date':date,'title':titulo,'link':link,'text':text,'summary':summarizer.summarize(text, language='spanish')}
        listOfArticles.append(article)

    return listOfArticles

#TEST
#testList = getElTiempoArticles("19/02/18")
#print("l "+  str(len(testList)))
#print(testList[0]['title'])
#print(testList[0]['date'])
#print(testList[0]['text']+"\n")
#print(testList[0]['summary'])
