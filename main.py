from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

class MainApp(MDApp):
    def build(self):
        # Configuración del tema
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        return Builder.load_file('design.kv')

    def start_app(self):
        print("Iniciando la app...")
        # Aquí puedes agregar la lógica para cambiar de pantalla o iniciar funciones adicionales

if __name__ == "__main__":
    MainApp().run()
