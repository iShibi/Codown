import os
os.system('cls')
os.environ['KIVY_NO_CONSOLELOG'] = '1'
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
import json
from pathlib import Path
Window.clearcolor = (0.6, 0.6, 0.6, 1)

dictionary = {
    'f_comic_url': None,
    'f_comic_name': None,
    'f_issue_number': None,
    'f_year': None,
    'f_browser': None,
    'f_mode': None,
    'f_quality': None,
    'f_delete_image': None
}

class MyGui(FloatLayout):

    f_comic_url = ObjectProperty(None)
    f_comic_name = ObjectProperty(None)
    f_issue_number = ObjectProperty(None)
    f_year = ObjectProperty(None)

    def browser_option(self, instance, value, browser):
        if value:
            dictionary.update({'f_browser': browser})
    
    def mode_option(self, instance, value, mode):
        if value:
            dictionary.update({'f_mode': mode})
    
    def quality_option(self, instance, value, quality):
        if value:
            dictionary.update({'f_quality': quality})
    
    def image_option(self, instance, value, delete_image):
        if value:
            dictionary.update({'f_delete_image': delete_image})

    def download_button_pressed(self, instance):
        dictionary.update({'f_comic_url': self.f_comic_url.text})
        dictionary.update({'f_comic_name': self.f_comic_name.text})
        dictionary.update({'f_issue_number': self.f_issue_number.text})
        dictionary.update({'f_year': self.f_year.text})
        
        json_object = json.dumps(dictionary, indent=6)

        with open('user_input.json', 'w') as outfile:
            outfile.write(json_object)

        os.system('python scraper.py')

        os.system('python downloader.py')


    
class MyApp(App):
    def build(self):
        self.title = 'Codown'
        icon_path = Path('media\icon.png').resolve()
        self.icon = str(icon_path)
        return MyGui()


if __name__ == "__main__":
    MyApp().run()