from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Cargar el archivo KV
Builder.load_file("design.kv")

# Pantalla de inicio
class MenuScreen(Screen):
    def go_to_home(self):
        self.manager.current = 'home'

# Pantalla principal (Home)
class HomeScreen(Screen):
    def go_to_calendar(self):
        self.manager.current = 'calendar'

    def go_to_reminders(self):
        self.manager.current = 'reminders'

    def go_to_pending(self):
        self.manager.current = 'pending'

    def go_to_settings(self):
        self.manager.current = 'settings'

# Pantallas adicionales
class CalendarScreen(Screen):
    pass

class RemindersScreen(Screen):
    pass

class PendingScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

# Clase principal de la aplicación
class TestApp(MDApp):
    def build(self):
        # Crear el gestor de pantallas
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(RemindersScreen(name='reminders'))
        sm.add_widget(PendingScreen(name='pending'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    TestApp().run()
