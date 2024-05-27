from kivy.config import Config
import re

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
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

class TelaPerfil(BoxLayout):
    def __init__(self, email, **kwargs):
        super(TelaPerfil, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10  
        self.padding = 20
        
        self.add_widget(Label(text=f"Bem-vindo, {email}\nVersão beta do App!\nTela de Verificação de usuário =).", color=(0, 0, 0.2, 1), bold=True, font_size=16))
        
        botao_layout = BoxLayout(padding=8)
        self.add_widget(botao_layout)
        
        self.deslogar = Button(text="Deslogar", background_color=get_color_from_hex('#ff0000'))
        self.deslogar.bind(on_press=self.Deslogar)
        botao_layout.add_widget(self.deslogar)
        
    def Deslogar(self, instance):
        App.get_running_app().change_screen("login")

class Telalogin(BoxLayout):
    def __init__(self, **kwargs):
        super(Telalogin, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10  
        self.padding = 20

        self.add_widget(AsyncImage(source=''))
        
        self.add_widget(Label(text="Nome Completo", color=(0, 0, 0.2, 1), bold=True, font_size=26, size_hint_y=None, height=40))
        self.Nome = TextInput(hint_text="Digite seu nome completo", multiline=False, width=410, size_hint=(None, None), height=40)
        self.add_widget(self.Nome)
        
        self.add_widget(Label(text="CPF", color=(0, 0, 0.2, 1), bold=True, font_size=26, size_hint_y=None, height=40))
        self.CPF = TextInput(hint_text="Digite seu CPF", multiline=False, width=410, size_hint=(None, None), height=40)
        self.add_widget(self.CPF)
        
        self.add_widget(Label(text="Endereço", color=(0, 0, 0.2, 1), bold=True, font_size=26, size_hint_y=None, height=40))
        self.Endereco = TextInput(hint_text="Digite seu endereço", multiline=False, width=410, size_hint=(None, None), height=40)
        self.add_widget(self.Endereco)
        
        self.add_widget(Label(text="Insira o seu E-mail", color=(0, 0, 0.2, 1), bold=True, font_size=26, size_hint_y=None, height=40))
        self.Email = TextInput(hint_text="Digite o seu e-mail", multiline=False, width=410, size_hint=(None, None), height=40)
        self.add_widget(self.Email)
        
        self.add_widget(Label(text="Insira sua Senha:", color=(0, 0, 0.2, 1), bold=True, font_size=26, size_hint_y=None, height=40))
        self.Senha = TextInput(hint_text="Digite sua senha", password=True, multiline=False, width=410, size_hint=(None, None), height=40)
        self.add_widget(self.Senha)
        
        botao_layout = BoxLayout(padding=8, size_hint_y=None, height=50)
        self.add_widget(botao_layout)
        
        self.enviar = Button(text="Cadastrar", background_color=get_color_from_hex('#3498db'), size_hint=(None, None), width=200, height=30)
        self.enviar.bind(on_press=self.Cadastra)
        botao_layout.add_widget(self.enviar)
        
        self.login = Button(text="Login", background_color=get_color_from_hex('#ff0000'), size_hint=(None, None), width=200, height=30)
        self.login.bind(on_press=self.Login)
        botao_layout.add_widget(self.login)

        self.esquecisenha = Button(text="Esqueceu a senha ?", color=(0, 0, 0.2, 1), bold=True, font_size=16, background_color=(1, 1, 1, 0), size_hint_y=None, height=50)
        self.esquecisenha.bind(on_press=self.reset_senha)
        self.add_widget(self.esquecisenha)
        
    def validate_email(self, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        return False

    def Cadastra(self, instance):
        nome = self.Nome.text
        cpf = self.CPF.text
        endereco = self.Endereco.text
        email = self.Email.text
        senha = self.Senha.text
        if email.strip() == "" or senha.strip() == "" or nome.strip() == "" or cpf.strip() == "" or endereco.strip() == "":
            print("Por favor, preencha todos os campos.")
            return
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, senha)
            db = firebase.database()
            data = {
                "nome": nome,
                "cpf": cpf,
                "endereco": endereco,
                "email": email
            }
            db.child("users").child(user["localId"]).set(data)
            print("Usuário registrado com sucesso.")
        except Exception as e:
            print("Erro ao registrar o usuário:", e)
    
    def Login(self, instance):
        email = self.Email.text
        senha = self.Senha.text
        if email.strip() == "" or senha.strip() == "":
            print("Por favor, preencha todos os campos.")
            return
        if not self.validate_email(email):
            print("E-mail inválido. Por favor, insira um e-mail válido.")
            return
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            user = auth.sign_in_with_email_and_password(email, senha)
            App.get_running_app().change_screen("perfil")
        except Exception as e:
            print("Erro ao verificar login:", e)

    def reset_senha(self, instance):
        email = self.Email.text
        if email.strip() == "":
            print("Por favor, insira seu e-mail.")
            return
        if not self.validate_email(email):
            print("E-mail inválido. Por favor, insira um e-mail válido.")
            return
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            auth.send_password_reset_email(email)
            print("E-mail para redefinição de senha enviado.")
        except Exception as e:
            print("Erro ao enviar e-mail de redefinição de senha:", e)

class Umatela(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.login_screen = Telalogin()
        return self.login_screen

    def change_screen(self, screen_name):
        if screen_name == "perfil":
            self.profile_screen = TelaPerfil(email=self.login_screen.Email.text)
            self.root.clear_widgets()
            self.root.add_widget(self.profile_screen)
        elif screen_name == "login":
            self.login_screen = Telalogin()
            self.root.clear_widgets()
            self.root.add_widget(self.login_screen)

if __name__ == '__main__':
    Umatela().run()