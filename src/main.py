from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
from kivy.uix.listview import ListItemButton

import threading

from articleScraper import EzArticle


class ArticleButton(ListItemButton):
    article = ObjectProperty()


class CurrentArticle(BoxLayout):
    title = StringProperty()
    summary = StringProperty()
    whole_text = StringProperty()
    date = StringProperty()
    link = StringProperty()


class MainForm(BoxLayout):
    articles_list = ObjectProperty()
    ezArticle = EzArticle()

    def get_last_articles_async(self):
        thread = threading.Thread(target=self.get_last_articles_sync)
        thread.start()
        print("get articles async")

    def get_last_articles_sync(self):
        last_articles = self.ezArticle.getElTiempoArticles()
        self.articles_list.adapter.data.clear()
        self.articles_list.adapter.data.extend(last_articles)
        self.articles_list._trigger_reset_populate()
        print("get articles sync")

    def args_converter(self, index , data_item):
        data_item['whole_text'] = data_item.pop('text')
        return {'article': data_item}


# BEGIN ROOTFORM
class RootForm(BoxLayout):
    main_form = ObjectProperty()
    current_article = ObjectProperty()

    def show_current_article(self, article=None):
        self.clear_widgets()
        if self.current_article is None:
            self.current_article = CurrentArticle()
        if article is not None:
            self.current_article.title = article['title']
            self.current_article.summary = article['summary']
            self.current_article.whole_text = article['whole_text']
            self.current_article.date = article['date']
            self.current_article.link = article['link']
        self.add_widget(self.current_article)

    def show_main_form(self):
        self.clear_widgets()
        if self.main_form is None:
            self.main_form = MainForm()
            self.main_form.get_last_articles_async()
        self.add_widget(self.main_form)
# END ROOTFORM
class ezReaderApp(App):
    def build(self):
        return RootForm()

if __name__ == '__main__':
    ezReaderApp().run()
