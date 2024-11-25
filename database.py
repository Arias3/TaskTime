from kivy.storage.jsonstore import JsonStore
import uuid

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
##
##---------------------------LISTAS------------------#
##

# Función para agregar una lista
def agregar_lista(clave, titulo, descripcion):
    """Agrega una nueva lista a la base de datos, con un campo 'items' vacío."""
    try:
        # Verifica si la clave ya existe para evitar sobrescribir
        if clave in store_listas:
            print("La lista con esa clave ya existe.")
            return
        
        # Agrega la nueva lista a la base de datos
        store_listas.put(clave, titulo=titulo, descripcion=descripcion, items=[])
        print(f"Lista '{titulo}' agregada correctamente.")
    
    except Exception as e:
        print(f"Error al agregar la lista: {e}")

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

# Función para agregar un ítem a una lista
def agregar_item_a_lista(clave_lista, texto_item, check=False):
    """Agrega un nuevo ítem a una lista existente."""
    try:
        lista = store_listas.get(clave_lista)
        if lista:
            nuevo_item_id = str(uuid.uuid4())  # Generar un nuevo UUID para el ítem
            item = {
                "id_item": nuevo_item_id,
                "texto": texto_item,
                "check": check
            }
            lista["items"].append(item)  # Agregar el nuevo ítem a la lista
            store_listas.put(clave_lista, **lista)  # Guardar la lista actualizada
            return True
        return False
    except Exception as e:
        print(f"Error al agregar el ítem: {e}")
        return False


def actualizar_check_item(clave_lista, id_item, nuevo_estado):
    """
    Actualiza el estado de check de un ítem en una lista en la base de datos.

    - clave_lista: Clave de la lista en la base de datos.
    - id_item: ID único del ítem.
    - nuevo_estado: Nuevo estado del checkbox (True/False).
    """
    # Obtener la lista desde la base de datos
    lista = store_listas.get(clave_lista)
    if lista:
        for item in lista["items"]:
            if item["id_item"] == id_item:
                item["check"] = nuevo_estado  # Actualizar el estado
                # Guardar la lista actualizada
                store_listas.put(clave_lista, **lista)
                return True
    return False

def actualizar_texto_item(clave_lista, id_item, nuevo_texto):
    """
    Actualiza el texto de un ítem en una lista en la base de datos.

    - clave_lista: Clave de la lista en la base de datos.
    - id_item: ID único del ítem.
    - nuevo_texto: Nuevo texto para el ítem.
    """
    # Obtener la lista desde la base de datos
    lista = store_listas.get(clave_lista)
    if lista:
        for item in lista["items"]:
            if item["id_item"] == id_item:
                item["texto"] = nuevo_texto  # Actualizar el texto
                # Guardar la lista actualizada
                store_listas[clave_lista] = lista  # Guardar los cambios en el diccionario
                return True
    return False

# Función para obtener los ítems de una lista
def obtener_items(clave_lista):
    """Obtiene todos los ítems de una lista (independientemente de su estado)."""
    lista = store_listas.get(clave_lista)
    if lista:
        return lista["items"]
    return []

def obtener_texto_item(clave_lista, item_id):
    """Obtiene el texto asociado a un ítem de una lista."""
    items = obtener_items(clave_lista)
    for item in items:
        if isinstance(item, dict):  # Asegurarse de que sea un diccionario
            if item.get("id_item") == item_id:  # Usar "id_item" en lugar de "id"
                return item.get("texto", "")  # Retorna el texto o una cadena vacía si no existe
        else:
            print(f"Elemento inválido encontrado en la lista: {item}")
    return ""  # Retorna una cadena vacía si no se encuentra el ítem

# Función para eliminar un ítem de una lista
def eliminar_item_de_lista(lista_id, item_id):
    """Elimina un ítem de una lista por su ID."""
    data = store_listas.get(lista_id)
    if not data:
        return False  # Si no existe la lista, retorna False

    # Buscar el ítem a eliminar
    item_to_remove = next((item for item in data["items"] if item["id_item"] == item_id), None)
    if item_to_remove:
        data["items"].remove(item_to_remove)  # Eliminar el ítem de la lista
        store_listas.put(lista_id, **data)  # Actualizar la lista en la base de datos
        return True
    return False

