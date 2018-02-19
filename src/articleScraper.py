import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from summa import summarizer

def getElTiempoArticles():
    page = requests.get("http://www.eltiempo.com/politica")
    soup = BeautifulSoup(page.content, "html.parser")

    listArticlesInfo_html = soup.select(".notas-secundarias-bk .informacion")

    listOfArticles = list()

    for i in range(len(listArticlesInfo_html)):
        date = listArticlesInfo_html[i].select(".seccion-fecha meta[itemprop=datePublished]")[0]["content"]

        titulo_html = listArticlesInfo_html[i].find(class_="titulo")
        titulo = titulo_html.get_text(strip=True)
        link = 'http://www.eltiempo.com' + titulo_html.find('a')["href"]

        textPage = requests.get(link)
        textSoup = BeautifulSoup(textPage.content, "html.parser")
        text_html = textSoup.select(".articulo-contenido p.contenido")
        del text_html[-1] # delete last entry: Info about author
        text = ""
        for j in range(len(text_html)):
            text += "\n" +  text_html[j].get_text()


        article = {'date':date,'title':titulo,'link':link,'text':text,'summary':summarizer.summarize(text, language='spanish')}
        listOfArticles.append(article)

    return listOfArticles
