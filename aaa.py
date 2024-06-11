from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.core.window import Window
from kivy.metrics import dp
import os
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import BooleanProperty, StringProperty
from kivy.lang import Builder
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.uix.spinner import MDSpinner
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivy.properties import ObjectProperty
import pyrebase
from collections import OrderedDict
from kivy.uix.image import AsyncImage, Image
from kivy.utils import platform
from kivy.utils import escape_markup
import webbrowser
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window


firebaseConfig = {
    'apiKey': "AIzaSyA3gOHi9Q6aHQ5seN5S9bbNmQpPQFMGXFs",
    'authDomain': "magnus-c4b38.firebaseapp.com",
    'databaseURL': "https://magnus-c4b38-default-rtdb.firebaseio.com",
    'projectId': "magnus-c4b38",
    'storageBucket': "magnus-c4b38.appspot.com",
    'messagingSenderId': "458576341456",
    'appId': "1:458576341456:web:6117f4a9160b8667b8f1d5"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        
        Window.size = (360, 640)  # Definindo o tamanho da janela
        
        with self.canvas:
            self.bg = Rectangle(source='Telastest/MUDAR PARA (20) (1).png', pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.spinner = MDSpinner(size_hint=(None, None), size=(dp(36), dp(36)),
                            pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.add_widget(self.spinner)

    def update_bg(self, *args):
        window_ratio = Window.width / Window.height
        image_ratio = 360 / 640
        
        if window_ratio > image_ratio:
            # Tela mais larga que a proporção da imagem
            new_height = Window.height
            new_width = new_height * image_ratio
        else:
            # Tela mais alta que a proporção da imagem
            new_width = Window.width
            new_height = new_width / image_ratio
        
        self.bg.size = (new_width, new_height)
        self.bg.pos = ((Window.width - new_width) / 2, (Window.height - new_height) / 2)

    def on_enter(self):
        Clock.schedule_once(self.dismiss_screen, 1)

    def dismiss_screen(self, dt):
        self.manager.current = 'Entrar_login'