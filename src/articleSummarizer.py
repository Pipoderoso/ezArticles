from articleScraper import getElTiempoArticles

newArticles = getElTiempoArticles() 

print(newArticles[0]['Title'])

print(newArticles[0]['Text'])
