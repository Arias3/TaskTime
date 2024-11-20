from kivy.storage.jsonstore import JsonStore

# Inicializa la base de datos
store = JsonStore('recordatorios.json')

def agregar_recordatorio(clave, titulo, descripcion, fecha, hora):
    store.put(clave, titulo=titulo, descripcion=descripcion, fecha=fecha, hora=hora)

def obtener_todos_recordatorios():
    return [(key, store.get(key)) for key in store.keys()]

def eliminar_recordatorio(clave):
    """Elimina un recordatorio por su clave."""
    if store.exists(clave):  # Verifica si la clave existe
        store.delete(clave)
        return True
    return False