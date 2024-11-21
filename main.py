from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivymd.uix.button import MDIconButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
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

# Registrar la fuente personalizada
LabelBase.register(
    "TittleRegular",  # Nombre de la fuente
    "assets/TittleRegular.otf"  # Ruta a la fuente
)


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
        
        # Verificar si hay recordatorios y mostrar el mensaje si no hay ninguno
        if not recordatorios:
            self.mostrar_mensaje_sin_recordatorios()
            return
        
        # Si hay recordatorios, ocultar el mensaje
        if hasattr(self.ids, 'mensaje_sin_recordatorios'):
            self.ids.mensaje_sin_recordatorios.opacity = 0

        for key, data in recordatorios:
            # Obtenemos los valores directamente sin necesidad de codificación
            titulo = data.get("titulo", "Sin título")
            descripcion = data.get("descripcion", "Sin descripción")
            fecha = data.get("fecha", "Sin fecha")
            hora = data.get("hora", "Sin hora")

            # Crear la tarjeta con los valores
            card = self.crear_tarjeta(key, titulo, descripcion, fecha, hora)
            self.ids.recordatorios_list.add_widget(card)

    def mostrar_mensaje_sin_recordatorios(self):
        """Muestra el mensaje cuando no hay recordatorios."""
        if not hasattr(self.ids, 'mensaje_sin_recordatorios'):
            # Crear el label si no existe
            mensaje = MDLabel(
                text="¡Crea un nuevo recordatorio!",
                halign="center",
                font_style="H6",
                font_size="18sp",
                theme_text_color="Secondary",
                size_hint=(None, None),
                size=("280dp", "40dp"),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
            # Asegurarse de agregar el mensaje al layout correspondiente
            self.ids.recordatorios_list.add_widget(mensaje)
            self.ids.mensaje_sin_recordatorios = mensaje  # Guardamos el label en self.ids
        else:
            # Si ya existe, solo mostrarlo
            self.ids.mensaje_sin_recordatorios.opacity = 1


    def crear_tarjeta(self, key, titulo, descripcion, fecha, hora):
        """Crea una tarjeta con la información del recordatorio."""
        card = MDCard(
            orientation="vertical",
            size_hint=(0.95, None),  # Usamos un tamaño relativo
            height="140dp",  # O ajustamos esto con un valor proporcional
            pos_hint={"center_x": 0.5},
            elevation=2,
            md_bg_color=(235 / 255, 208 / 255, 215 / 255, 1)
        )

        # Layout principal
        main_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(0.95, None),  # Ocupa el 95% del ancho del contenedor padre
            height="140dp",  # Definir una altura adecuada
            padding=[10, 10, 10, 10],  # Espaciado interno
            spacing=10  # Espaciado entre los widgets
        )

        # Función que se llama cuando cambia el estado del checkbox
        def on_checkbox_active(checkbox, value, key):
            if value:  # Si el checkbox está marcado
                print(f"Recordatorio {key} marcado como completado")
                # Llamamos a marcar_completado
                self.marcar_completado(checkbox, value, key)
            else:  # Si el checkbox está desmarcado
                print(f"Recordatorio {key} desmarcado")
                # Puedes manejar la lógica para cuando el checkbox esté desmarcado

        # Crear el checkbox
        checkbox_complete = CheckBox(
            size_hint=(None, None),
            size=("60dp", "60dp"),
            pos_hint={"center_y": 0.5},
            active=False  # El checkbox comienza desmarcado
        )

        # Asignar imágenes personalizadas para los estados
        checkbox_complete.background_checkbox_normal = 'assets/inactivo.png'  # Imagen para estado desmarcado
        checkbox_complete.background_checkbox_down = 'assets/activo.png'  # Imagen para estado marcado

        # Conectar el cambio de estado del checkbox a la función on_checkbox_active
        checkbox_complete.bind(active=lambda instance, value: on_checkbox_active(instance, value, key))

        # Agregar el checkbox al layout
        main_layout.add_widget(checkbox_complete)


        # Información del recordatorio
        info_layout = BoxLayout(
            orientation="vertical", 
            size_hint=(0.75, 1),  # Ocupa el 75% del ancho del contenedor padre
            padding="4dp", 
            spacing="4dp"
        )
        info_layout.add_widget(
            Label(
                text=f"{titulo}", 
                font_size="25sp",
                halign="center", 
                font_name="assets/TittleRegular.otf",  # Usando la fuente personalizada
                color=(0, 0, 0, 1),
                text_size=(None, None),
            )
        )
        info_layout.add_widget(
            MDLabel(
                text=f"Fecha: {fecha} | Hora: {hora}", 
                halign="center", 
                font_style="Subtitle1",
                font_size="18sp"  # Aumentar tamaño de fuente

            )
        )

        # Añadimos el layout de información al layout principal
        main_layout.add_widget(info_layout)

        # Botones de acción
        action_layout = BoxLayout(
            orientation="vertical", 
            size_hint=(None, 1), 
            width="40dp", 
            padding="5dp", 
            spacing="5dp"
        )
        btn_edit = MDIconButton(
            icon="assets/edit.png",
            icon_size="38sp",  # Íconos más grandes
            on_release=lambda _: self.ir_a_editar(key),
        )
        btn_details = MDIconButton(
            icon="assets/details.png",
            icon_size="38sp",  # Íconos más grandes
            on_release=lambda _: self.toggle_details(card, descripcion),
        )
        action_layout.add_widget(btn_edit)
        action_layout.add_widget(btn_details)

        # Añadimos los botones al layout principal
        main_layout.add_widget(action_layout)

        # Añadimos el layout principal a la tarjeta
        card.add_widget(main_layout)

        
        return card

    # Definimos la función para marcar como completado o desmarcar
    def marcar_completado(self, instance, value, key):
        """Marca el recordatorio como completado o desmarcado, cambia el icono y elimina el recordatorio si es completado."""
        
        if value:  # Si el checkbox está marcado
            print(f"Recordatorio {key} marcado como completado")

            # Cargar y reproducir el sonido de campana
            sonido_completado = SoundLoader.load('assets/campana.wav')
            if sonido_completado:
                sonido_completado.play()  # Reproducir el sonido

            # Función para eliminar el recordatorio después de un pequeño retraso
            def eliminar_con_retraso(*args):
                # Eliminar el recordatorio de la base de datos
                if eliminar_recordatorio(key):
                    print(f"Recordatorio {key} eliminado de la base de datos.")
                
                # Recargar los recordatorios después de la eliminación y mostrar mensaje si no hay recordatorios
                self.load_recordatorios()

                # Comprobar si después de recargar hay recordatorios y mostrar el mensaje
                if not obtener_todos_recordatorios():  # Comprobar si no hay recordatorios
                    self.mostrar_mensaje_sin_recordatorios()  # Mostrar mensaje si no hay recordatorios
                else:
                    # Si hay recordatorios, asegurarse de que el mensaje esté oculto
                    if hasattr(self.ids, 'mensaje_sin_recordatorios'):
                        self.ids.mensaje_sin_recordatorios.opacity = 0

            # Programar la ejecución de la función de eliminación con un retraso de 1 segundo
            Clock.schedule_once(eliminar_con_retraso, 1)  # 1 segundo de retraso
        else:
            print(f"Recordatorio {key} desmarcado")
            # Aquí puedes manejar el caso en que se desmarque el checkbox si es necesario
    
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
