import flet as ft
import os
import re
import subprocess
import json
import threading
import time
from appledl.appledl import create_config, load_config, authenticate

# Función para cargar la configuración desde config.json
def load_config():
    user_windows = os.environ["USERNAME"]
    config_directory = f"C://Users//{user_windows}//Apple"
    config_file = f"{config_directory}//config.json"

    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    return None

# Función para extraer el nombre de la app desde la URL
def extract_app_name(url):
    match = re.search(r"/app/([^/]+)/id\d+", url)
    if match:
        return match.group(1)
    return None

# Función para ejecutar el comando ipatool search y parsear la salida como texto
def search_app_by_name(route, app_name):
    user_windows = os.environ["USERNAME"]
    config_directory = f"C://Users//{user_windows}//Apple"
    config_file = f"{config_directory}//config.json"

    # Cargar configuración
    config = load_config()
    if not config:
        route = './assets/ipatool.exe'
        user = search_term.value
        password = "password"  # Sustituir con la contraseña desde una fuente segura
        create_config(user, password, route)
        config = load_config()

    if config:
        user = config.get('user')
        password = config.get('password')
        route = config.get('route')

        authenticate(config, user, password)

    command = f'{route} search --limit 10 {app_name} --non-interactive --keychain-passphrase 0000'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = result.stdout

    # Usar expresiones regulares para extraer los datos
    apps = []
    matches = re.findall(r'\"bundleID\":\"(.*?)\".*?\"id\":\d+.*?\"name\":\"(.*?)\".*?\"version\":\"(.*?)\"', output)
    for match in matches:
        bundle_id, name, version = match
        apps.append({"bundleID": bundle_id, "name": name, "version": version})

    return apps

# Función para ejecutar el comando ipatool download
def download_app_by_bundle_id(route, bundle_id):
    command = f'{route} download -b "{bundle_id}" --non-interactive --keychain-passphrase 0000'
    subprocess.run(command, shell=True)

# Función para mostrar la animación de puntos
def show_downloading_animation(page):
    global downloading
    dots = ["", ".", "..", "...", "...."]
    while downloading:
        for dot in dots:
            if not downloading:
                status_message.value = ""
                page.update()
                return
            status_message.value = f"Downloading{dot}"
            page.update()
            time.sleep(0.5)
    status_message.value = ""
    page.update()

# Función para actualizar la interfaz con la lista de apps
def update_app_list(page, apps, route):
    app_list.controls.clear()
    for app in apps:
        app_name = app['name']
        app_version = app['version']
        app_bundle_id = app['bundleID']

        download_button = ft.IconButton(
            icon=ft.icons.DOWNLOAD,
            style=ft.ButtonStyle(
                color="#ffffff",
                bgcolor="#5B0098",
                overlay_color="#5B0098",
                shape=ft.RoundedRectangleBorder(radius=5),
                shadow_color="#5B0098",
                elevation=5,
            ),
            on_click=lambda e, b_id=app_bundle_id: start_download(page, route, b_id)
        )
        
        app_list.controls.append(
            ft.Row(
                controls=[
                    ft.Text(f"{app_name}", weight="bold"),
                    ft.Text(f"v{app_version}"),
                    download_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
    page.update()

# Función para iniciar la descarga y mostrar la animación
def start_download(page, route, bundle_id):
    global downloading
    downloading = True
    
    # Asegúrate de que el mensaje de "Downloading" se actualice antes de comenzar la descarga
    status_message.value = "Downloading"
    page.update()

    # Iniciar la animación de puntos en un hilo separado
    threading.Thread(target=show_downloading_animation, args=(page,), daemon=True).start()

    # Ejecutar la descarga
    download_app_by_bundle_id(route, bundle_id)
    
    # Detener la animación de puntos
    downloading = False
    status_message.value = "Download complete"
    page.update()
    time.sleep(1)  # Mostrar el mensaje de "Download complete" por un segundo
    status_message.value = ""
    page.update()

# Función para buscar la app y actualizar la interfaz
def search_and_update(e):
    url = search_term.value
    app_name = extract_app_name(url)

    config = load_config()
    if config:
        route = config.get('route')
        
        if app_name and route:
            apps = search_app_by_name(route, app_name)
            if apps:
                update_app_list(e.page, apps, route)
            else:
                status_message.value = "No apps found"
                e.page.update()
        else:
            status_message.value = "Invalid URL, app not found, or invalid configuration"
            e.page.update()
    else:
        status_message.value = "Configuration file not found"
        e.page.update()

# Controles de la interfaz
search_term = ft.TextField(
    hint_text="App URL",
    width=350,
    height=50,
    bgcolor='#343434',
    border=ft.InputBorder.NONE,
    border_radius=30,
    cursor_height=20,
    cursor_color='#5B0098',
    text_style=ft.TextStyle(
        font_family='nunito',
        size=15,
    ),
)

status_message = ft.Text("")

search_button = ft.ElevatedButton(
    "Search",
    style=ft.ButtonStyle(
        color="#ffffff",
        bgcolor="#5B0098",
        overlay_color="#5B0098",
        shape=ft.RoundedRectangleBorder(radius=5),
        shadow_color="#5B0098",
        elevation=5,
    ),
    on_click=search_and_update,
)

# Contenedor de la lista de aplicaciones con desplazamiento
app_list = ft.ListView(
    width=681,
    height=300,  # Ajusta la altura según sea necesario
    spacing=10,  # Espacio entre los elementos
    padding=10,  # Espacio interno del ListView
)

home_page = ft.Stack(
    [
        ft.Container(
            content=ft.Column(
                controls=[search_term, search_button, status_message, app_list],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
    ],
    width=681,
    height=478,
)

# Variable global para controlar la animación de descarga
downloading = False
