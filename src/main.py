from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

class MainForm(BoxLayout):
	articlesList = ObjectProperty()

# BEGIN ROOTFORM
class RootForm(BoxLayout):
	pass
# END ROOTFORM
class ezReaderApp(App):
	pass

if __name__ == '__main__':
	ezReaderApp().run()
