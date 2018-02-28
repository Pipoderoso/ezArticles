import requests
from bs4 import BeautifulSoup
from collections import namedtuple
from summa import summarizer
import time

class ezArticle():

	def __init__(self, sDate = None):
		self.sDate = sDate

	def getElTiempoArticles(self): #sDate string structure example: 19/02/18

		page = requests.get("http://www.eltiempo.com/politica")
		soup = BeautifulSoup(page.content, "html.parser")

		tempListArticlesInfo_html = soup.select(".notas-secundarias-bk .informacion") #!
		listArticlesInfo_html = list() #Articles with same date as sDate will be saved here
		listOfArticles = list() #Final list of articles

		# Saving only  article html files that correspond to the given date, if date is not given, then list articles from first page #

		if (self.sDate != None):

			stdDate = time.strptime(self.sDate, "%d/%m/%y")

			for numPage in range(3): #Search till page 2 of "more news"

				for i in range(len(tempListArticlesInfo_html)):
					articleDate = tempListArticlesInfo_html[i].select(".seccion-fecha meta[itemprop=datePublished]")[0]["content"] #format: yyyy-mm-dd
					stdArticleDate = time.strptime(articleDate, "%Y-%m-%d")

					if(stdArticleDate == stdDate):
						listArticlesInfo_html.append(tempListArticlesInfo_html[i])

				page = requests.get("http://www.eltiempo.com/category/latest/politica/" + str(numPage))        
				soup = BeautifulSoup(page.content, "html.parser")
				tempListArticlesInfo_html = soup.select(".listing .informacion") #!

		else: 

			listArticlesInfo_html = tempListArticlesInfo_html

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
testList = ezArticle("26/02/18")
maList = testList.getElTiempoArticles()
output = open('output.txt', 'w')
for item in maList:
	output.write("%s\n" % item)
output.close()
