from articleScraper import getElTiempoArticles

newArticles = getElTiempoArticles()

print("Title:\n%s\n" % newArticles[0]['title'])
print("Text:\n%s\n" % newArticles[0]['text'])
print("Summary:\n%s\n " % newArticles[0]['summary'])
