from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from functools import partial
from database import (
    obtener_todos_recordatorios,
    agregar_recordatorio,
    eliminar_recordatorio,
)
import uuid  # Mejorar la generación de claves

# Cargar el archivo KV
Builder.load_file("design.kv")


# --- Pantallas de la aplicación --- #
class MenuScreen(Screen):
    def go_to_home(self):
        self.manager.current = "home"


class HomeScreen(Screen):
    def go_to_calendar(self):
        self.manager.current = "calendar"

    def go_to_reminders(self):
        self.manager.current = "reminders"

    def go_to_pending(self):
        self.manager.current = "pending"

    def go_to_settings(self):
        self.manager.current = "settings"


class RemindersScreen(Screen):
    def on_enter(self):
        """Cargar los recordatorios al entrar en la pantalla."""
        self.load_recordatorios()

    def load_recordatorios(self):
        """Carga y muestra los recordatorios en la interfaz."""
        self.ids.recordatorios_list.clear_widgets()
        recordatorios = obtener_todos_recordatorios()

        for key, data in recordatorios:
            titulo = data.get("titulo", "Sin título")
            descripcion = data.get("descripcion", "Sin descripción")
            fecha = data.get("fecha", "Sin fecha")
            hora = data.get("hora", "Sin hora")

            # Crear tarjeta
            card = MDCard(
                orientation="vertical",
                size_hint=(None, None),
                size=("280dp", "180dp"),
                pos_hint={"center_x": 0.5},
                elevation=5,
                padding="12dp",
            )

            # Añadir etiquetas
            card.add_widget(
                MDLabel(text=f"Título: {titulo}", font_style="H6", halign="left")
            )
            card.add_widget(MDLabel(text=f"Descripción: {descripcion}", halign="left"))
            card.add_widget(
                MDLabel(text=f"Fecha: {fecha} | Hora: {hora}", halign="left")
            )

            # Botón de eliminación
            btn_delete = MDRaisedButton(
                text="Eliminar",
                pos_hint={"center_x": 0.5},
                on_release=partial(self.eliminar_recordatorio, key),  # Usamos partial para pasar la clave
            )
            card.add_widget(btn_delete)

            # Añadir tarjeta al contenedor
            self.ids.recordatorios_list.add_widget(card)

    def eliminar_recordatorio(self, clave, touch=None):
        """Elimina el recordatorio y recarga la lista."""
        print(f"Eliminando recordatorio con clave: {clave}")  # Agregar esta línea
        if eliminar_recordatorio(clave):
            self.load_recordatorios()



class AddRecordatorioScreen(Screen):
    def agregar_recordatorio(self):
        """Agrega un nuevo recordatorio."""
        titulo = self.ids.titulo.text
        descripcion = self.ids.descripcion.text
        fecha = self.ids.fecha.text
        hora = self.ids.hora.text

        if not titulo or not descripcion or not fecha or not hora:
            print("Todos los campos son obligatorios.")
            return

        # Generar una clave única para cada recordatorio
        clave = str(uuid.uuid4())

        # Usar la función de database.py para agregar el recordatorio
        agregar_recordatorio(clave, titulo, descripcion, fecha, hora)

        # Limpiar los campos después de agregar el recordatorio
        self.ids.titulo.text = ""
        self.ids.descripcion.text = ""
        self.ids.fecha.text = ""
        self.ids.hora.text = ""

        # Cambiar de pantalla a la de recordatorios
        self.manager.current = "reminders"


class CalendarScreen(Screen):
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
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CalendarScreen(name="calendar"))
        sm.add_widget(RemindersScreen(name="reminders"))
        sm.add_widget(AddRecordatorioScreen(name="add_recordatorio"))
        sm.add_widget(PendingScreen(name="pending"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == "__main__":
    TestApp().run()
