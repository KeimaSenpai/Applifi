import flet as ft
import os
import json
from appledl.appledl import create_config, load_config, authenticate, search_app, download_app
import threading

title = ft.Text('Applifi')

search_term = ft.TextField(
    hint_text="App Name",
    width=250,
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

progress_bar = ft.ProgressBar(width=250, value=0)

def update_progress_bar(page, progress):
    progress_bar.value = progress
    page.update()

def actual_download_process(config, term, page):
    bundle_id, name, version = search_app(config, term)
    
    if bundle_id and name and version:
        download_app(config, bundle_id, name, version, lambda progress: update_progress_bar(page, progress))
    else:
        # Reset the progress bar if the app is not found
        update_progress_bar(page, 0)

def download_app_flet(e):
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
        
        # Inicializar la barra de progreso en 0 antes de empezar la descarga
        update_progress_bar(e.page, 0)
        
        # Buscar y descargar la aplicación en un hilo separado
        term = search_term.value
        threading.Thread(target=actual_download_process, args=(config, term, e.page)).start()

download = ft.ElevatedButton(
    "Download",
    style=ft.ButtonStyle(
        color="#ffffff",
        bgcolor="#5B0098",
        overlay_color="#5B0098",
        shape=ft.RoundedRectangleBorder(radius=5),
        shadow_color="#5B0098",
        elevation=5,
    ),
    on_click=download_app_flet,
)

home_page = ft.Stack(
    [
        ft.Container(
            content=ft.Column(
                controls=[title, search_term, download, progress_bar],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
    ],
    width=681,
    height=478,
)
