from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
import pyrebase

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

class HomeScreen(Screen):
    pass

class DisplayScreen(Screen):
    pass

class MyApp(MDApp):
    def publicar(self):
        Builder.load_file('main.kv')
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(HomeScreen(name="home"))
        self.screen_manager.add_widget(DisplayScreen(name="display"))
        return self.screen_manager

    def on_start(self):
        self.home_screen = self.root.get_screen('home')
        self.display_screen = self.root.get_screen('display')

        if hasattr(self.home_screen.ids, 'send_button'):
            self.home_screen.ids.send_button.bind(on_release=self.send_data)
        else:
            print("send_button não encontrado em HomeScreen")

        self.display_data()

    def send_data(self, instance):
        data = self.home_screen.ids.data_field.text
        database.child("data").push({'text': data})
        self.display_data()
        self.root.current = 'display'

    def display_data(self):
        data = database.child("data").get().val()
        self.display_screen.ids.data_list.clear_widgets()

        if data:
            for key, value in data.items():
                self.display_screen.ids.data_list.add_widget(MDLabel(text=value['text'], halign="center"))

if __name__ == '__main__':
    MyApp().run()

