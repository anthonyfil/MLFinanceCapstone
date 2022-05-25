import csv
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty, StringProperty

class FileChoosePopup(Popup):
    load = ObjectProperty()

class tab(TabbedPanel):

    def __init__(self):
        super(tab, self).__init__()
        file_path = StringProperty("No file chosen")
        the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        print(self.file_path)

        # check for non-empty list i.e. file selected
        if self.file_path:
            self.ids.get_file.text = self.file_path
            quit()

Builder.load_file('GUI.kv')

class fileInputScreen(App):

    def build(self):
        return tab()

if __name__ == '__main__':
    fileInputScreen().run()

