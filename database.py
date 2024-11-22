from kivy.storage.jsonstore import JsonStore

# Inicializa las bases de datos para recordatorios y listas
store_recordatorios = JsonStore('recordatorios.json')
store_listas = JsonStore('listas.json')

# Función para agregar un recordatorio
def agregar_recordatorio(clave, titulo, descripcion, fecha, hora):
    """Agrega un nuevo recordatorio a la base de datos."""
    store_recordatorios.put(clave, titulo=titulo, descripcion=descripcion, fecha=fecha, hora=hora)

# Función para obtener todos los recordatorios
def obtener_todos_recordatorios():
    """Obtiene todos los recordatorios desde la base de datos."""
    return [(key, store_recordatorios.get(key)) for key in store_recordatorios.keys()]

# Función para eliminar un recordatorio
def eliminar_recordatorio(clave):
    """Elimina un recordatorio por su clave."""
    if store_recordatorios.exists(clave):  # Verifica si la clave existe
        store_recordatorios.delete(clave)
        return True
    return False

# Función para agregar una lista
def agregar_lista(clave, titulo, descripcion):
    """Agrega una nueva lista a la base de datos."""
    store_listas.put(clave, titulo=titulo, descripcion=descripcion)

# Función para obtener todas las listas
def obtener_todas_listas():
    """Obtiene todas las listas desde la base de datos."""
    return [(key, store_listas.get(key)) for key in store_listas.keys()]

# Función para eliminar una lista
def eliminar_lista(clave):
    """Elimina una lista por su clave."""
    if store_listas.exists(clave):  # Verifica si la clave existe
        store_listas.delete(clave)
        return True
    return False
