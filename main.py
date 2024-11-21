from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from functools import partial
import uuid  # Para generar claves únicas
from database import (
    obtener_todos_recordatorios,
    agregar_recordatorio,
    eliminar_recordatorio,
)
from kivy.core.window import Window

# Ajuste para el tamaño de la ventana
Window.size = (414, 896)  # Ajustar tamaño de la ventana si es necesario

# O también puedes ajustar la escala en función de la densidad de píxeles
Window.minimum_width = 414
Window.minimum_height = 896


# --- Cargar el archivo KV --- #
Builder.load_file("design.kv")


# --- Pantallas de la aplicación --- #

# Pantalla del menú principal
class MenuScreen(Screen):
    def go_to_home(self):
        self.manager.current = "home"


# Pantalla de inicio
class HomeScreen(Screen):
    def go_to_calendar(self):
        self.manager.current = "calendar"

    def go_to_reminders(self):
        self.manager.current = "reminders"

    def go_to_pending(self):
        self.manager.current = "pending"

    def go_to_settings(self):
        self.manager.current = "settings"

# Pantalla de recordatorios
class RemindersScreen(Screen):
    def on_enter(self):
        self.load_recordatorios()

    def load_recordatorios(self):
        """Carga y muestra los recordatorios en la interfaz."""
        self.ids.recordatorios_list.clear_widgets()
        self.ids.recordatorios_list.spacing = "20dp"  # Separación entre tarjetas
        recordatorios = obtener_todos_recordatorios()

        for key, data in recordatorios:
            # Obtenemos los valores directamente sin necesidad de codificación
            titulo = data.get("titulo", "Sin título")
            descripcion = data.get("descripcion", "Sin descripción")
            fecha = data.get("fecha", "Sin fecha")
            hora = data.get("hora", "Sin hora")

            # Crear la tarjeta con los valores
            card = self.crear_tarjeta(key, titulo, descripcion, fecha, hora)
            self.ids.recordatorios_list.add_widget(card)

    def crear_tarjeta(self, key, titulo, descripcion, fecha, hora):
        """Crea una tarjeta con la información del recordatorio."""
        card = MDCard(
            orientation="vertical",
            size_hint=(0.95, None),  # Usamos un tamaño relativo
            height="140dp",  # O ajustamos esto con un valor proporcional
            pos_hint={"center_x": 0.5},
            elevation=3,
            md_bg_color=(235 / 255, 208 / 255, 215 / 255, 1)
        )

        # Layout principal
        main_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(0.95, None),  # Ocupa el 95% del ancho del contenedor padre, altura fija.
            height="140dp",  # Asegúrate de definir una altura adecuada.
            padding=[10, 10, 10, 10]  # Espaciado interno.
        )

        # Botón de completado
        btn_complete = MDIconButton(
            icon="assets/completed.png",  # Imagen inicial
            icon_size="50sp",  # Tamaño del ícono
            pos_hint={"center_y": 0.5},  # Asegura que el botón esté centrado verticalmente.
            on_release=lambda instance: self.marcar_completado(instance, card, key)
        )

        # Añadimos el botón a un BoxLayout para centrarlo verticalmente
        btn_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),  # No cambia el ancho; ocupa todo el alto del main_layout.
            width="60dp",  # Ancho fijo para el layout del botón.
        )
        btn_layout.add_widget(btn_complete)

        # Agregamos el layout del botón al layout principal
        main_layout.add_widget(btn_layout)

        # Información del recordatorio
        info_layout = BoxLayout(orientation="vertical", size_hint=(0.75, 1), padding="4dp", spacing="4dp")
        info_layout.add_widget(
            MDLabel(
                text=f"{titulo}", 
                font_style="H5",  # Titulo más grande
                halign="center", 
                font_name="assets/TittleRegular.otf"  # Usando la fuente personalizada
            )
        )
        info_layout.add_widget(
            MDLabel(
                text=f"Fecha: {fecha} | Hora: {hora}", 
                halign="center", 
                font_style="H6",
                font_size="15sp"  # Aumentar tamaño de fuente
            )
        )
        main_layout.add_widget(info_layout)

        # Botones de acción
        action_layout = BoxLayout(orientation="vertical", size_hint=(None, 1), width="40dp", padding="5dp", spacing="5dp")
        btn_edit = MDIconButton(
            icon="assets/edit.png",
            icon_size="38sp",  # Hacer los íconos más grandes
            on_release=lambda _: self.ir_a_editar(key),
        )
        btn_details = MDIconButton(
            icon="assets/details.png",
            icon_size="38sp",  # Hacer los íconos más grandes
            on_release=lambda _: self.toggle_details(card, descripcion),
        )
        action_layout.add_widget(btn_edit)
        action_layout.add_widget(btn_details)
        main_layout.add_widget(action_layout)

        # Añadimos el layout principal a la tarjeta
        card.add_widget(main_layout)
        
        return card




    def marcar_completado(self, instance, card, key):
        """Marca el recordatorio como completado, cambia el icono, elimina el recordatorio y recarga la lista."""
        
        # Cambiar la imagen del botón de completado
        instance.icon = "assets/completed2.png"  # Cambiar el icono a completado

        # Cargar y reproducir el sonido de campana
        sonido_completado = SoundLoader.load('assets/campana.wav')
        if sonido_completado:
            sonido_completado.play()  # Reproducir el sonido

        # Función para eliminar el recordatorio después de un pequeño retraso
        def eliminar_con_retraso(*args):
            # Eliminar el recordatorio de la base de datos
            print(f"Eliminando recordatorio con clave: {key}")
            if eliminar_recordatorio(key):  # Llamada a la función de eliminar en database.py
                print(f"Recordatorio {key} eliminado de la base de datos.")

            # Recargar los recordatorios después de la eliminación
            self.load_recordatorios()

        # Programar la ejecución de la función de eliminación con un retraso de 1 segundo
        Clock.schedule_once(eliminar_con_retraso, 1)  # 1 segundo de retraso
    
    def toggle_details(self, card, descripcion):
        """Muestra u oculta la descripción completa del recordatorio."""
        if "detalles" in [w.text for w in card.children if isinstance(w, MDLabel)]:
            card.size = ("400dp", "110dp")
            for widget in card.children:
                if isinstance(widget, MDLabel) and widget.text.startswith("Detalles:"):
                    card.remove_widget(widget)
        else:
            card.size = ("400dp", "180dp")
            card.add_widget(
                MDLabel(text=f"Detalles: {descripcion}", halign="left", font_style="Caption")
            )

    def ir_a_editar(self, key):
        """Navega a la pantalla de edición para el recordatorio."""
        self.manager.current = "editar_tarea"
        recordatorio = next((r[1] for r in obtener_todos_recordatorios() if r[0] == key), None)

        if recordatorio:
            editar_screen = self.manager.get_screen("editar_tarea")
            editar_screen.ids.editar_titulo.text = recordatorio.get("titulo", "Sin título")
            editar_screen.ids.editar_descripcion.text = recordatorio.get("descripcion", "")
            editar_screen.ids.editar_fecha.text = recordatorio.get("fecha", "")
            editar_screen.ids.editar_hora.text = recordatorio.get("hora", "")
            editar_screen.recordatorio_id = key


# Pantalla para agregar recordatorios
class AddRecordatorioScreen(Screen):
    def agregar_recordatorio(self):
        titulo = self.ids.titulo.text
        descripcion = self.ids.descripcion.text
        fecha = self.ids.fecha.text
        hora = self.ids.hora.text

        if not all([titulo, descripcion, fecha, hora]):
            print("Todos los campos son obligatorios.")
            return

        clave = str(uuid.uuid4())
        agregar_recordatorio(clave, titulo, descripcion, fecha, hora)

        self.ids.titulo.text = ""
        self.ids.descripcion.text = ""
        self.ids.fecha.text = ""
        self.ids.hora.text = ""
        self.manager.current = "reminders"


# Pantalla para editar recordatorios
class EditarTareaScreen(Screen):
    recordatorio_id = None

    def actualizar_recordatorio(self):
        titulo = self.ids.editar_titulo.text
        descripcion = self.ids.editar_descripcion.text
        fecha = self.ids.editar_fecha.text
        hora = self.ids.editar_hora.text

        if not all([titulo, descripcion, fecha, hora]):
            print("Todos los campos son obligatorios.")
            return

        agregar_recordatorio(self.recordatorio_id, titulo, descripcion, fecha, hora)
        self.manager.current = "reminders"


# Pantallas adicionales
class CalendarScreen(Screen):
    pass


class PendingScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


# --- Clase principal de la aplicación --- #
class TestApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CalendarScreen(name="calendar"))
        sm.add_widget(RemindersScreen(name="reminders"))
        sm.add_widget(AddRecordatorioScreen(name="add_recordatorio"))
        sm.add_widget(EditarTareaScreen(name="editar_tarea"))
        sm.add_widget(PendingScreen(name="pending"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == "__main__":
    TestApp().run()
