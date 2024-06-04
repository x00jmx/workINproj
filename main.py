from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
import os
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
import pyrebase
from collections import OrderedDict

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
        self.image = Image(source='logo.png', size_hint=(0.9, 0.9),
        pos_hint={'center_x': 0.5, 'center_y': 0.55})
        self.add_widget(self.image)
    def on_enter(self):
        Clock.schedule_once(self.dismiss_screen, 8)
    def dismiss_screen(self, dt):
        self.manager.current = 'Entrar_login'  
class TelaEntrarLogin(Screen):
    def show_dialog_Errologin(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=lambda *args: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def Login(self):
        email = self.ids.email.text
        senha = self.ids.senha.text
        
        if not email or not senha:
            self.show_dialog_Errologin("Por favor, preencha todos os campos.")
            return
        
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            user = auth.sign_in_with_email_and_password(email, senha)
            App.user_uid = user['localId'] 
            print("Login realizado com sucesso.")
            self.manager.current = 'Menu'
            self.manager.get_screen('Menu').user_type = "physical" 
        except Exception as e:
            self.show_dialog_Errologin(f"Erro ao fazer login: {e}")

class TelaEntrarLoginJuridico(Screen):
    def show_dialog_ErroCadastro(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=lambda *args: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def show_dialog_Errologin(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=lambda *args: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def LoginJuridico(self):
        cnpj = self.ids.cnpj.text
        email = self.ids.email.text
        senha = self.ids.senha.text
        
        if not all([cnpj, email, senha]):
            self.show_dialog_Errologin("Por favor, preencha todos os campos.")
            return
        
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            user = auth.sign_in_with_email_and_password(email, senha)
            App.user_uid = user['localId']  
            print("Login realizado com sucesso.")
            self.manager.current = 'Menu'
            self.manager.get_screen('Menu').user_type = "juridical" 
        except Exception as e:
            self.show_dialog_Errologin(f"Erro ao fazer login: {e}")
            
class TelaCriarConta(Screen):
    def show_dialog_ErroCadastro(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=lambda *args: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def show_dialog_SuccessCadastro(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=self.on_success_dialog_close
                )
            ]
        )
        self.dialog.open()

    def on_success_dialog_close(self, *args):
        self.dialog.dismiss()
        self.manager.current = 'Entrar_login'
    
    def Cadastra(self):
        nome = self.ids.nome.text
        nome_social = self.ids.nome_social.text
        cpf = self.ids.cpf.text
        email = self.ids.email.text
        senha = self.ids.senha.text
        confirmar_senha = self.ids.confirmar_senha.text
        data_nascimento = self.ids.data_nascimento.text
        
        if not all([nome, cpf, email, senha, confirmar_senha, data_nascimento]):
            self.show_dialog_ErroCadastro("Por favor, preencha todos os campos.")
            return
        
        if senha != confirmar_senha:
            self.show_dialog_ErroCadastro("As senhas não coincidem.")
            return
        
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)                               
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, senha)
            db = firebase.database()
            uid = user['localId'] 
            data = {
                "nome": nome,
                "nome_social": nome_social,
                "cpf": cpf,
                "email": email,
                "data_nascimento": data_nascimento,
                "uid": uid,
                "type": "physical"
            }
            db.child("users").child(uid).set(data) 
            self.show_dialog_SuccessCadastro("Usuário registrado com sucesso.")
        except Exception as e:
            self.show_dialog_ErroCadastro(f"Erro ao registrar o usuário: {e}")

class TelaCriarContaJuridico(Screen):
    def show_dialog_ErroCadastro(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=lambda *args: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def show_dialog_SuccessCadastro(self, message):
        self.dialog = MDDialog(
            text=message,
            buttons=[
                MDFlatButton(
                    text="Fechar",
                    on_release=self.on_success_dialog_close
                )
            ]
        )
        self.dialog.open()

    def on_success_dialog_close(self, *args):
        self.dialog.dismiss()
        self.manager.current = 'Entrar_Login_jurídico' 
    
    def CadastrarJuridico(self):
        nome_empresa = self.ids.nome_empresa.text
        email = self.ids.email.text
        senha = self.ids.senha.text
        telefone = self.ids.telefone.text
        cnpj = self.ids.cnpj.text
        
        if not all([nome_empresa, email, senha, telefone, cnpj]):
            self.show_dialog_ErroCadastro("Por favor, preencha todos os campos.")
            return
        
        try:
            firebase = pyrebase.initialize_app(firebaseConfig)
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, senha)
            db = firebase.database()
            data = {
                "nome_empresa": nome_empresa,
                "email": email,
                "telefone": telefone,
                "cnpj": cnpj,
                "type": "juridical"
            }
            db.child("users_juridicos").child(user["localId"]).set(data)
            self.show_dialog_SuccessCadastro("Conta jurídica registrada com sucesso.")
        except Exception as e:
            self.show_dialog_ErroCadastro(f"Erro ao registrar a conta jurídica: {e}")

class TelaMenu(Screen):
    user_type = StringProperty()
    publicacao_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_enter = self.carregar_dados  # Chame uma única função para carregar os dados

    def carregar_dados(self):
        """Carrega as vagas e publicações."""
        self.carregar_vagas()
        self.carregar_publicacoes()

    def carregar_publicacoes(self):
        """Carrega as publicações do Firebase e as exibe na tela."""
        try:
            if self.user_type == "physical":
                user_info = database.child("users").child(App.user_uid).get().val()
            elif self.user_type == "juridical":
                user_info = database.child("users_juridicos").child(App.user_uid).get().val()
            else:
                print("Erro: Tipo de usuário desconhecido.")
                return

            if user_info is None:
                print("Erro: Dados do usuário não encontrados.")
                return

            publicacoes = database.child("publicacoes").get().val()
            print("Publicações do Firebase:", publicacoes)

            self.ids.publicacoes_box.clear_widgets()

            if publicacoes:
                for key, publicacao in publicacoes.items():
                    self.ids.publicacoes_box.add_widget(
                        PublicacaoCard(
                            user_name=publicacao.get('user_name', 'Nome do usuário não encontrado'),
                            texto_publicacao=publicacao.get('text', '')
                        )
                    )
            else:
                print("Nenhuma publicação encontrada.")

        except Exception as e:
            print("Erro ao carregar publicações:", e)
    def carregar_vagas(self):
        print(f"App.user_uid: {App.user_uid}")
        try:
            if self.user_type == "physical":
                user_info = database.child("users").child(App.user_uid).get().val()
            elif self.user_type == "juridical":
                user_info = database.child("users_juridicos").child(App.user_uid).get().val()
            else:
                print("Erro: Tipo de usuário desconhecido.")
                return

            print(f"user_info: {user_info}")

            if user_info is None:
                print("Erro: Dados do usuário não encontrados.")
                return

            vagas = database.child("posts").get().val()
            self.ids.vagas_box.clear_widgets()
            if vagas:
                for key, vaga in vagas.items():
                    self.ids.vagas_box.add_widget(
                        VagaCard(
                            especificacao=vaga.get('especificacao', 'N/A'),
                            cargo=vaga.get('cargo', 'N/A'),
                            local_de_trabalho=vaga.get('local_de_trabalho', 'N/A'),
                            localidade=vaga.get('localidade', 'N/A'),
                            tipo_de_vaga=vaga.get('tipo_de_vaga', 'N/A'),
                            sobre_vaga=vaga.get('sobre_vaga', 'N/A'),
                            user_name=vaga.get('user_name', 'Nome do usuário não encontrado'),
                            on_press=lambda x: self.mostrar_detalhes_vaga(key)
                        )
                    )
            else:
                print("Nenhuma vaga encontrada.")
        except Exception as e:
            print("Erro ao carregar vagas:", e)


    def mostrar_detalhes_vaga(self, key):   
        vaga = database.child("posts").child(key).get().val()
        self.manager.current = 'DetalhesVaga' 
        self.manager.get_screen('DetalhesVaga').set_vaga(vaga)  

    def show_dialog_need_juridical(self):
        self.dialog = MDDialog(
            text="Você precisa ser uma conta jurídica para criar vagas.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def criar_vaga(self):
        if self.user_type == "juridical":
            self.manager.current = 'CriarVaga'
        else:
            self.show_dialog_need_juridical()
    
    def update_publicacoes(self):
        """Atualiza a lista de publicações na tela Menu."""
        self.carregar_publicacoes()  # Chame a função existente para carregar as publicações

class PublicacaoCard(MDCard):
    user_name = StringProperty()
    texto_publicacao = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.size_hint_y = None
        self.height = self.minimum_height
        user_label = MDLabel(
            text=f"{self.user_name}:",
            font_style="Subtitle1"
        )
        super().add_widget(user_label) 

        texto_label = MDLabel(
            text=self.texto_publicacao
        )
        super().add_widget(texto_label)  
        
class VagaCard(MDCard):
    especificacao = StringProperty()
    cargo = StringProperty()
    local_de_trabalho = StringProperty()
    localidade = StringProperty()
    tipo_de_vaga = StringProperty()
    sobre_vaga = StringProperty()
    user_name = StringProperty()
    vaga_id = StringProperty() 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)
        self.height = dp(180)
        self.adaptive_height = True
        self.pos_hint = {"center_x": 0.5}
        self.padding = dp(10)
        self.spacing = dp(30)

        self.add_widget(MDLabel(text=f"Usuário: {self.user_name}"))
        self.add_widget(MDLabel(text=f"Especificação: {self.especificacao}"))
        self.add_widget(MDLabel(text=f"Cargo: {self.cargo}"))
        self.add_widget(MDLabel(text=f"Local de Trabalho: {self.local_de_trabalho}"))
        self.add_widget(MDLabel(text=f"Localidade: {self.localidade}"))
        self.add_widget(MDLabel(text=f"Tipo de Vaga: {self.tipo_de_vaga}"))

        sobre_card = MDCard(
            orientation='vertical',
            padding=dp(10),
            size_hint_y=None,
            height=dp(60),
            pos_hint={'center_x': 0.5}
        )
        sobre_card.add_widget(MDLabel(text=f"Sobre: {self.sobre_vaga}"))
        self.add_widget(sobre_card)

        candidatura_button = MDRaisedButton(
            text="Enviar Candidatura",
            pos_hint={'center_x': 0.5},
            size_hint_x=None,
            width=dp(200),
            on_press=lambda x: self.enviar_candidatura()
        )
        self.add_widget(candidatura_button)

    def enviar_candidatura(self):
        dialog = MDDialog(
            title="Candidatura Enviada",
            text=f"Candidatura enviada para a vaga: {self.user_name}",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

class Telacriarvaga(Screen):
    especificacao = [
        'Administração e Escritório',
        'Tecnologia da Informação',
        'Marketing e Vendas',
        'Recursos Humanos',
        'Finanças',
        'Engenharia',
        'Saúde',
        'Educação',
        'Design e Criação',
        'Logística e Transporte',
        'Jurídico',
        'Atendimento ao Cliente',
        'Operações e Produção',
        'Cargos de Nível Executivo'
    ]
    cargo = [
        'Operacionais e de Suporte',
        'Técnico e Especializado',
        'Supervisão e Coordenação',
        'Gerência',
        'Chefia e Direção',
        'Executivos'
    ]
    local_de_trabalho = [
        'Presencial',
        'Híbrido',
        'Remoto'
    ]
    localidade  = [
        'AL - Arapiraca',
        'AL - Campo Alegre',
        'AL - Coruripe',
        'AL - Delmiro Gouveia',
        'AL - Maceió',
        'AL - Palmeira dos Índios',
        'AL - Penedo',
        'AL - Rio Largo',
        'AL - São Miguel dos Campos',
        'AL - União dos Palmares',
        'BA - Camaçari',
        'BA - Feira de Santana',
        'BA - Ilhéus',
        'BA - Itabuna',
        'BA - Jequié',
        'BA - Juazeiro',
        'BA - Lauro de Freitas',
        'BA - Salvador',
        'BA - Teixeira de Freitas',
        'BA - Vitória da Conquista',
        'CE - Caucaia',
        'CE - Crato',
        'CE - Fortaleza',
        'CE - Iguatu',
        'CE - Itapipoca',
        'CE - Juazeiro do Norte',
        'CE - Maracanaú',
        'CE - Maranguape',
        'CE - Quixadá',
        'CE - Sobral',
        'MA - Açailândia',
        'MA - Bacabal',
        'MA - Caxias',
        'MA - Codó',
        'MA - Imperatriz',
        'MA - Paço do Lumiar',
        'MA - Pinheiro',
        'MA - Santa Inês',
        'MA - São Luís',
        'MA - Timon',
        'PB - Bayeux',
        'PB - Cabedelo',
        'PB - Cajazeiras',
        'PB - Campina Grande',
        'PB - Guarabira',
        'PB - João Pessoa',
        'PB - Patos',
        'PB - Pombal',
        'PB - Santa Rita',
        'PB - Sousa',
        'PE - Cabo de Santo Agostinho',
        'PE - Camaragibe',
        'PE - Caruaru',
        'PE - Garanhuns',
        'PE - Jaboatão dos Guararapes',
        'PE - Olinda',
        'PE - Paulista',
        'PE - Petrolina',
        'PE - Recife',
        'PE - Vitória de Santo Antão',
        'PI - Altos',
        'PI - Barras',
        'PI - Campo Maior',
        'PI - Floriano',
        'PI - José de Freitas',
        'PI - Parnaíba',
        'PI - Picos',
        'PI - Piripiri',
        'PI - Teresina',
        'PI - União',
        'RN - Apodi',
        'RN - Caicó',
        'RN - Ceará-Mirim',
        'RN - Currais Novos',
        'RN - Macaíba',
        'RN - Mossoró',
        'RN - Natal',
        'RN - Parnamirim',
        'RN - Santa Cruz',
        'RN - São Gonçalo do Amarante',
        'SE - Aracaju',
        'SE - Estância',
        'SE - Itabaiana',
        'SE - Itaporanga DAjuda',
        'SE - Lagarto',
        'SE - Nossa Senhora do Socorro',
        'SE - Propriá',
        'SE - São Cristóvão',
        'SE - Simão Dias',
        'SE - Tobias Barreto'
    ]
    tipo_de_vaga = [
        'Tempo integral',
        'Meio período',
        'Contrato',
        'Temporário',
        'Outro',
        'Voluntário',
        'Estágio'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_especificacao = None
        self.selected_cargo = None
        self.selected_local_de_trabalho = None
        self.selected_localidade = None
        self.selected_tipo_de_vaga = None

    def show_especificacao(self, main_button):
        dropdown = DropDown()
        for option in self.especificacao:
            btn = Button(text=option, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda btn: self.select_option(dropdown, btn.text, main_button, 'especificacao'))
            btn.background_color = (1, 1, 1, 1)
            btn.color = (0, 0, 0, 1)
            dropdown.add_widget(btn)
        dropdown.open(main_button)

    def show_cargo(self, main_button):
        dropdown = DropDown()
        for option in self.cargo:
            btn = Button(text=option, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda btn: self.select_option(dropdown, btn.text, main_button, 'cargo'))
            btn.background_color = (1, 1, 1, 1)
            btn.color = (0, 0, 0, 1)
            dropdown.add_widget(btn)
        dropdown.open(main_button)

    def show_local_de_trabalho(self, main_button):
        dropdown = DropDown()
        for option in self.local_de_trabalho:
            btn = Button(text=option, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda btn: self.select_option(dropdown, btn.text, main_button, 'local_de_trabalho'))
            btn.background_color = (1, 1, 1, 1)
            btn.color = (0, 0, 0, 1)
            dropdown.add_widget(btn)
        dropdown.open(main_button)

    def show_localidade(self, main_button):
        dropdown = DropDown()
        for option in self.localidade:
            btn = Button(text=option, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda btn: self.select_option(dropdown, btn.text, main_button, 'localidade'))
            btn.background_color = (1, 1, 1, 1)
            btn.color = (0, 0, 0, 1)
            dropdown.add_widget(btn)
        dropdown.open(main_button)
    
    def show_tipo_de_vaga(self, main_button):
        dropdown = DropDown()
        for option in self.tipo_de_vaga:
            btn = Button(text=option, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda btn: self.select_option(dropdown, btn.text, main_button, 'tipo_de_vaga'))
            btn.background_color = (1, 1, 1, 1)
            btn.color = (0, 0, 0, 1)
            dropdown.add_widget(btn)
        dropdown.open(main_button)

    def select_option(self, dropdown, text, main_button, option_type):
        main_button.text = text
        dropdown.dismiss()
        main_button.size_hint_x = None
        main_button.width = dp(200)

        if option_type == 'especificacao':
            self.selected_especificacao = text
        elif option_type == 'cargo':
            self.selected_cargo = text
        elif option_type == 'local_de_trabalho':
            self.selected_local_de_trabalho = text
        elif option_type == 'localidade':
            self.selected_localidade = text
        elif option_type == 'tipo_de_vaga':
            self.selected_tipo_de_vaga = text

    def salvar_vaga(self):
        if not all([self.selected_especificacao, self.selected_cargo, self.selected_local_de_trabalho, self.selected_localidade, self.selected_tipo_de_vaga]):
            print("Por favor, preencha todos os campos.")
            return
        
        sobre_vaga = self.ids.sobre_vaga.text

        if not hasattr(App, 'user_uid'):
            print("Erro: Usuário não está logado.")
            return

        try:
            if self.manager.get_screen('Menu').user_type == "physical":
                user_info = database.child("users").child(App.user_uid).get().val()
            elif self.manager.get_screen('Menu').user_type == "juridical":
                user_info = database.child("users_juridicos").child(App.user_uid).get().val()
            else:
                print("Erro: Tipo de usuário desconhecido.")
                return

            print(f"App.user_uid: {App.user_uid}")
            print(f"user_info: {user_info}") 

            if user_info is None:
                print("Erro: Dados do usuário não encontrados.")
                return

            user_name = user_info.get("nome", "Nome não encontrado")    

            data = {
                "especificacao": self.selected_especificacao,
                "cargo": self.selected_cargo,
                "local_de_trabalho": self.selected_local_de_trabalho,
                "localidade": self.selected_localidade,
                "tipo_de_vaga": self.selected_tipo_de_vaga,
                "sobre_vaga": sobre_vaga,
                "user_name": user_name  
            }

            if not database:
                print("Erro: Conexão com o banco de dados não configurada.")
                return

            database.child("posts").push(data)
            print("Vaga salva com sucesso.")
        except Exception as e:
            print("Erro ao salvar a vaga:", e)

class TelaPublicacoes(Screen):
    def publicar(self):
        """Salva a publicação no Firebase."""
        publicacao_text = self.ids.publicacao_text.text
        if not publicacao_text:
            return

        try:
            user_info = database.child("users").child(App.user_uid).get().val()
            user_name = user_info.get("nome", "Nome não encontrado")

            data = {
                "user_name": user_name,
                "text": publicacao_text,
                "timestamp": firebase.database().serverTimestamp()
            }

            database.child("publicacoes").push(data)
            print("Publicação salva com sucesso.")
            print(f"Dados da publicação: {data}")
            self.ids.publicacao_text.text = ""
        except Exception as e:
            print(f"Erro ao salvar a publicação: {e}")

        # Atualiza as publicações na tela Menu
        app = MDApp.get_running_app()
        app.root.get_screen('Menu').update_publicacoes()

        self.manager.current = 'Menu'

class Telaconfignotificacoes(Screen):
    vagas = BooleanProperty(False)
    contratacao = BooleanProperty(False)
    mensagens = BooleanProperty(False)
    mencoes = BooleanProperty(False)
    publicar_comentar = BooleanProperty(False)
    user_info = StringProperty('') 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_settings()

    def on_pre_enter(self, *args):
        self.load_settings()
        self.load_user_info()

    def load_settings(self):
        user_settings = database.child("users").child(App.user_uid).child("notification_settings").get().val()
        if user_settings:
            self.vagas = user_settings.get('vagas', False)
            self.contratacao = user_settings.get('contratacao', False)
            self.mensagens = user_settings.get('mensagens', False)
            self.mencoes = user_settings.get('mencoes', False)
            self.publicar_comentar = user_settings.get('publicar_comentar', False)
        else:

            self.save_settings() 

    def save_settings(self):
        settings = {
            'vagas': self.vagas,
            'contratacao': self.contratacao,
            'mensagens': self.mensagens,
            'mencoes': self.mencoes,
            'publicar_comentar': self.publicar_comentar,
        }
        database.child("users").child(App.user_uid).child("notification_settings").set(settings)

    def load_user_info(self):
        try:
            user_info = database.child("users").child(App.user_uid).get().val()
            if user_info is None:
                print("Erro: Dados do usuário não encontrados.")
                self.user_info = "Usuário não encontrado." 
                return

            self.user_info = f"Nome: {user_info.get('nome', 'N/A')}\n"
            self.user_info += f"CPF: {user_info.get('cpf', 'N/A')}\n"
            self.user_info += f"Data de Nascimento: {user_info.get('data_nascimento', 'N/A')}\n"
            self.user_info += f"Email: {user_info.get('email', 'N/A')}\n"
            self.user_info += f"Nome Social: {user_info.get('nome_social', 'N/A')}"
        except Exception as e:
            print("Erro ao carregar informações do usuário:", e)

    def update_notification_setting(self, key, value):
        setattr(self, key, value)
        self.save_settings()
class TelaconfigPrivacidadeDados(Screen):
    pass

class TelaconfigVisibilidade(Screen):
    pass

class TelaconfigSeguranca(Screen):
    pass

class TelaconfigPerfil(Screen):
    pass

class TelaSalvos(Screen):
    pass

class Telanotificacoes(Screen):
    def load_user_info(self):
        try:
            user_info = database.child("users").child(App.user_uid).get().val()
            if user_info is None:
                print("Erro: Dados do usuário não encontrados.")
                self.user_info = "Usuário não encontrado." 
                return

            self.user_info = f"Nome: {user_info.get('nome', 'N/A')}\n"
            self.user_info += f"CPF: {user_info.get('cpf', 'N/A')}\n"
            self.user_info += f"Data de Nascimento: {user_info.get('data_nascimento', 'N/A')}\n"
            self.user_info += f"Email: {user_info.get('email', 'N/A')}\n"
            self.user_info += f"Nome Social: {user_info.get('nome_social', 'N/A')}"

            self.ids.user_info_label.text = self.user_info
        except Exception as e:
            print("Erro ao carregar informações do usuário:", e)

class TelaChat(Screen):
    pass

class TelaInformacoesPerfil(Screen):
    pass

class TelaEnderecoemail(Screen):
    pass

class TelaTrocarSenha(Screen):
    pass

class Telanumerostelefone(Screen):
    pass

class ItemConfirm(OneLineIconListItem):
    pass

class ConfigItem(OneLineIconListItem):
    pass

class LimitedMDTextField(MDTextField):
    max_text_length = 500
    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_text_length:
            substring = substring[:self.max_text_length - len(self.text)]
        return super().insert_text(substring, from_undo=from_undo)

class App(MDApp):
    user_uid = None
    dialog = None

    data = {
        'Bloquear': 'block-helper',
    }

    def build(self):
        Window.size = (dp(360), dp(640))
        Window.clearcolor = (1, 1, 1, 1)
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Telaconfignotificacoes(name='config_notificacoes'))
        self.screen_manager.add_widget(TelaEntrarLogin(name='Entrar_login'))
        self.screen_manager.add_widget(TelaEntrarLoginJuridico(name='Entrar_Login_jurídico'))
        self.screen_manager.add_widget(TelaCriarConta(name='Criar_conta'))
        self.screen_manager.add_widget(TelaCriarContaJuridico(name='Criar_conta_Jurídica'))
        self.screen_manager.add_widget(TelaMenu(name='Menu'))
        self.screen_manager.add_widget(TelaPublicacoes(name='Publicacoes'))
        self.screen_manager.add_widget(TelaSalvos(name='Salvos'))
        self.screen_manager.add_widget(Telanotificacoes(name='Notificacoes'))
        self.screen_manager.add_widget(TelaChat(name='chat'))
        self.screen_manager.add_widget(TelaInformacoesPerfil(name='informações_adicionais'))
        self.screen_manager.add_widget(TelaEnderecoemail(name='Endereço_email'))
        self.screen_manager.add_widget(TelaTrocarSenha(name='Trocar_Senha'))
        self.screen_manager.add_widget(Telanumerostelefone(name='Números_telefone'))
        self.screen_manager.add_widget(Telacriarvaga(name='CriarVaga')) 
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file("main.kv")

    def show_logout_dialog(self):
        self.dialog = MDDialog(
            text="Deseja sair da conta?",
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_release=lambda *args: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Sim",
                    on_release=lambda *args: self.logout_and_dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def logout_and_dismiss(self):
        self.dialog.dismiss() 
        self.logout() 

    def logout(self):
        self.root.current = 'Entrar_login'

    def refresh_callback(self):
        print("Layout de atualização atualizado!")

    def switch_screen(self, screen_name):
        pass

    def menu_callback(self, instance):
        Snackbar(text=instance.text).open()

    def confirm_action(self, dialog):
        selected_item = dialog.item.ids.container.text
        self.menu_callback(instance=selected_item)

    def select_option(self, dropdown, text, main_button):
        main_button.text = text
        dropdown.dismiss()
        main_button.size_hint_x = None
        main_button.width = dp(150)
    
    def update_notification_setting(self, key, value):
        screen = self.screen_manager.get_screen('config_notificacoes')
        setattr(screen, key, value)
        screen.save_settings()

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    App().run()