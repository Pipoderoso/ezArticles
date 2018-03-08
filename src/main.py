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
    article = ObjectProperty()
    title = StringProperty()
    text_to_show = StringProperty()
    date = StringProperty()
    link = StringProperty()
    change_text_button_title = StringProperty()

    def __init__(self, article,**kwargs):
        super(CurrentArticle, self).__init__(**kwargs)
        self.article = article
        self.title = self.article['title']
        self.text_to_show = self.article['summary']
        self.date = self.article['date']
        self.link = self.article['link']
        self.change_text_button_title = "View Original"

    def toggle_text(self):
        if self.change_text_button_title == "View Original":
            self.change_text_button_title = "View Summary"
            self.text_to_show = self.article['whole_text']
        else:
            self.change_text_button_title = "View Original"
            self.text_to_show = self.article['summary']


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

    def __init__(self, **kwargs):
        super(RootForm, self).__init__(**kwargs)
        self.main_form = MainForm()
        self.add_widget(self.main_form)

    def show_current_article(self, article=None):
        self.clear_widgets()
        if self.current_article is None and article is not None:
            self.current_article = CurrentArticle(article=article)

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
