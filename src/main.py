from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
from kivy.uix.listview import ListItemButton

import threading

from articleScraper import EzArticle


class ArticleButton(ListItemButton):
    pass


class MainForm(BoxLayout):
    articles_list = ObjectProperty()
    ezArticle = EzArticle()

    def get_last_articles_async(self):
        thread = threading.Thread(target=self.get_last_articles_sync)
        thread.start()
        print("get articles async")

    def get_last_articles_sync(self):
        last_articles = self.ezArticle.getElTiempoArticles()
        formated_list = [x['title'] for x in last_articles]
        self.articles_list.item_strings = formated_list
        self.articles_list.adapter.data.clear()
        self.articles_list.adapter.data.extend(formated_list)
        self.articles_list._trigger_reset_populate()
        print("get articles sync")


# BEGIN ROOTFORM
class RootForm(BoxLayout):

    def show_current_article(self, title):
        self.clear_widgets()
        current_article = Factory.CurrentArticle()
        current_article.title = title
        self.add_widget(current_article)

    def show_main_form(self):
        self.clear_widgets()
        self.add_widget(MainForm())
# END ROOTFORM
class ezReaderApp(App):
    pass

if __name__ == '__main__':
    ezReaderApp().run()
