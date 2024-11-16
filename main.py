from kivymd.app import MDApp  # Importar MDApp desde KivyMD
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Carga del archivo de diseño KV
Builder.load_file("design.kv")

# Declaración de las pantallas
class MenuScreen(Screen):
    def go_to_home(self):
        self.manager.current = 'home'  # Cambia a la pantalla de inicio

class HomeScreen(Screen):
    pass

# La clase principal de la app debe heredar de MDApp
class TestApp(MDApp):
    def build(self):
        # Crear el gestor de pantallas
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    TestApp().run()
