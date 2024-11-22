from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivymd.uix.button import MDIconButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import uuid  # Para generar claves únicas
import math
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
        # Tarjeta principal
        card = MDCard(
            orientation="vertical",
            size_hint=(0.95, None),
            height="140dp",  # Altura inicial
            pos_hint={"center_x": 0.5},
            elevation=2,
            md_bg_color=(235 / 255, 208 / 255, 215 / 255, 1)
        )

        # Layout principal vertical (contiene todo el contenido)
        container_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),  # Tamaño relativo horizontal y altura dinámica
            spacing="10dp",
            padding="10dp",
        )

        # Layout horizontal para el contenido principal
        main_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),  # Ocupa todo el ancho del contenedor
            height="100dp",  # Altura inicial adecuada para el contenido principal
            padding="10dp",
            spacing=8,
        )

         # Función que se llama cuando cambia el estado del checkbox
        def on_checkbox_complete(checkbox, value, key):
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

        # Conectar el cambio de estado del checkbox a la función on checkbox_complete
        checkbox_complete.bind(active=lambda instance, value: on_checkbox_complete(instance, value, key))

        # Agregar el checkbox al layout
        main_layout.add_widget(checkbox_complete)

        # Layout de información del recordatorio
        info_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.75, 1),
            spacing="4dp",
        )
        info_layout.add_widget(
            Label(
                text=titulo,
                font_size="25sp",
                halign="center",
                font_name="assets/TittleRegular.otf",
                color=(0, 0, 0, 1),
                text_size=(None, None),
            )
        )
        info_layout.add_widget(
            MDLabel(
                text="Vence en: [b]" + f"{fecha}" + "[/b]\n      " + f"{hora}",
                halign="center",
                font_style="Subtitle1",
                font_size="18sp",
                markup=True
            )
        )

        # Añadir el layout de información al layout principal
        main_layout.add_widget(info_layout)

        # Layout para los botones de acción
        action_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width="40dp",
            spacing="5dp",
        )
        btn_edit = MDIconButton(
            icon="assets/edit.png",
            icon_size="38sp",
            on_release=lambda _: self.ir_a_editar(key),
        )
        action_layout.add_widget(btn_edit)

        # Checkbox para los detalles
        checkbox_details = CheckBox(
            size_hint=(None, None),
            size=("50dp", "50dp"),
            pos_hint={"center_y": 0.5},
            active=False,
        )

        # Asignar imágenes personalizadas
        checkbox_details.background_checkbox_normal = 'assets/details.png'
        checkbox_details.background_checkbox_down = 'assets/details2.png'

        # Conectar el cambio de estado al layout de detalles
        checkbox_details.bind(
            active=lambda instance, value: self.toggle_details(details_layout, descripcion, card, value)
        )
        action_layout.add_widget(checkbox_details)

        # Añadir los botones de acción al layout principal
        main_layout.add_widget(action_layout)

        # Añadir el layout principal horizontal al contenedor vertical
        container_layout.add_widget(main_layout)

        # Layout para los detalles (inicialmente oculto)
        details_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),  # Tamaño relativo horizontal y altura dinámica
            height=0  # Altura inicial cero para que no desplace otros elementos
        )
        container_layout.add_widget(details_layout)

        # Añadir el contenedor completo a la tarjeta
        card.add_widget(container_layout)

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
    
     # Función que se llama cuando cambia el estado del checkbox para detalles
    def on_checkbox_details(self,checkbox, value, key, card, descripcion):
        """Activa o desactiva los detalles según el estado del checkbox."""
        if value:  # Si el checkbox está marcado
            print(f"Detalles activados para {key}")
            self.toggle_details(card, descripcion, activar=True)
        else:  # Si el checkbox está desmarcado
            print(f"Detalles desactivados para {key}")
            self.toggle_details(card, descripcion, activar=False)
    # Función para mostrar u ocultar los detalles
    def toggle_details(self, details_layout, descripcion, card, activar=True):
        """Muestra u oculta la descripción completa del recordatorio."""
        if activar:  # Mostrar los detalles
            if not details_layout.children:  # Solo agregar si no están visibles
                detalles_label = MDLabel(
                    text=f"[b]Detalles:[/b] {descripcion}",
                    halign="left",
                    font_style="Subtitle1",
                    markup=True,
                    size_hint_y=None,
                )
                # Ajustar la altura del layout y la tarjeta en función del texto
                self._adjust_card_height(details_layout, card, detalles_label, descripcion)

                # Añadir la etiqueta de detalles al layout
                details_layout.add_widget(detalles_label)
                
        else:  # Ocultar los detalles
            if details_layout.children:
                detalles_label = details_layout.children[0]
                card.height -= detalles_label.height
                details_layout.clear_widgets()
                details_layout.height = 0

    def _adjust_card_height(self, details_layout, card, detalles_label, size):
        """Ajusta dinámicamente la altura de la tarjeta según la longitud del texto y el número de líneas necesarias."""
        # Contar los caracteres del texto
        texto = detalles_label.text

        # Dividir el texto en líneas de 43 caracteres
        num_lineas = math.ceil(len(texto) / 43)  # Divide el texto en líneas de 43 caracteres y redondea hacia arriba

        # Calcular la altura total basada en el número de líneas
        altura_linea = 20  # Cada línea aumenta 20dp de altura
        altura_total = num_lineas * altura_linea  # Total de la altura a agregar

        # Ajustar la altura del detalles_label (la altura es proporcional al número de líneas)
        detalles_label.height = altura_total

        # Ajustar la altura del layout que contiene los detalles
        details_layout.height = detalles_label.height

        # Ajustar la altura total de la tarjeta
        card.height += detalles_label.height

    def ir_a_editar(self, key):
        """Navega a la pantalla de edición para el recordatorio."""
        self.manager.current = "editar_tarea"
        recordatorio = next((r[1] for r in obtener_todos_recordatorios() if r[0] == key), None)
        if not recordatorio:
            print(f"Recordatorio con clave {key} no encontrado")
            return

        if recordatorio:
            editar_screen = self.manager.get_screen("editar_tarea")
            editar_screen.ids.editar_titulo.text = recordatorio.get("titulo", "Sin título")
            editar_screen.ids.editar_descripcion.text = recordatorio.get("descripcion", "")
            editar_screen.ids.editar_fecha.text = recordatorio.get("fecha", "")
            editar_screen.ids.editar_hora.text = recordatorio.get("hora", "")
            editar_screen.recordatorio_id = key
# Pantalla para agregar recordatorios
class AddRecordatorioScreen(MDScreen):
    def agregar_recordatorio(self):
        # Obtiene los valores de los campos
        titulo = self.ids.titulo.text
        descripcion = self.ids.descripcion.text
        fecha = self.ids.fecha.text
        hora = self.ids.hora.text

        # Valida que todos los campos estén llenos
        if not all([titulo, descripcion, fecha, hora]):
            print("Todos los campos son obligatorios.")
            return

        # Genera una clave única
        clave = str(uuid.uuid4())

        # Guarda el recordatorio en la base de datos
        try:
            agregar_recordatorio(clave, titulo, descripcion, fecha, hora)  # Llama a la función de base de datos
            print(f"Recordatorio guardado correctamente: {clave}, {titulo}, {descripcion}, {fecha}, {hora}")
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
            return

        # Limpia los campos y regresa a la pantalla anterior
        self.ids.titulo.text = ""
        self.ids.descripcion.text = ""
        self.ids.fecha.text = ""
        self.ids.hora.text = ""
        self.manager.current = "reminders"

    def on_date_selected(self, instance, value, date_range):
        """Asigna la fecha seleccionada al campo de texto."""
        if value:
            try:
                self.ids.fecha.text = value.strftime("%d/%m/%Y")
            except Exception as e:
                print(f"Error al actualizar el campo de texto: {e}")
        else:
            print("No se seleccionó ninguna fecha.")

    def on_time_selected(self, instance, time):
        """Asigna la hora seleccionada al campo de texto."""
        if time:
            try:
                self.ids.hora.text = time.strftime("%H:%M")  # Formato de 24 horas
            except Exception as e:
                print(f"Error al actualizar el campo de texto: {e}")
        else:
            print("No se seleccionó ninguna hora.")

    def show_date_picker(self, focus):
        """Muestra el selector de fecha si el campo tiene el foco."""
        if not focus:
            return
        try:
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_date_selected)
            date_dialog.open()
        except Exception as e:
            print(f"Error al abrir el DatePicker: {e}")

    def show_time_picker(self, focus):
        """Muestra el selector de hora si el campo tiene el foco."""
        if not focus:
            return
        try:
            time_dialog = MDTimePicker()
            time_dialog.bind(on_save=self.on_time_selected)
            time_dialog.open()
        except Exception as e:
            print(f"Error al abrir el TimePicker: {e}") 
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

    def on_date_selected(self, instance, value, date_range):
        """Asigna la fecha seleccionada al campo de texto."""
        if value:
            try:
                # Ajuste correcto del ID del campo de texto
                self.ids.editar_fecha.text = value.strftime("%d/%m/%Y")
            except Exception as e:
                print(f"Error al actualizar el campo de texto: {e}")
        else:
            print("No se seleccionó ninguna fecha.")

    def on_time_selected(self, instance, time):
        """Asigna la hora seleccionada al campo de texto."""
        if time:
            try:
                # Ajuste correcto del ID del campo de texto
                self.ids.editar_hora.text = time.strftime("%H:%M")  # Formato de 24 horas
            except Exception as e:
                print(f"Error al actualizar el campo de texto: {e}")
        else:
            print("No se seleccionó ninguna hora.")

    def show_date_picker(self, focus):
        """Muestra el selector de fecha si el campo tiene el foco."""
        if not focus:
            return
        try:
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_date_selected)
            date_dialog.open()
        except Exception as e:
            print(f"Error al abrir el DatePicker: {e}")

    def show_time_picker(self, focus):
        """Muestra el selector de hora si el campo tiene el foco."""
        if not focus:
            return
        try:
            time_dialog = MDTimePicker()
            time_dialog.bind(on_save=self.on_time_selected)
            time_dialog.open()
        except Exception as e:
            print(f"Error al abrir el TimePicker: {e}")

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
