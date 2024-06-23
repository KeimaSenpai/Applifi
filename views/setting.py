import flet as ft
import os
import json
import requests

# Obtener el nombre de usuario del sistema y configurar los directorios de configuración
user_windows = os.environ.get("USERNAME")
config_directory = f"C://Users//{user_windows}//Apple"
config_file = os.path.join(config_directory, "config.json")
ipatool_path = os.path.join(config_directory, "ipatool.exe")
ipatool_download_url = "https://github.com/KeimaSenpai/Applifi/releases/download/0.0.1/ipatool.exe"  # Reemplazar con la URL real

# Función para guardar la configuración en el archivo JSON
def save_config(user, password, page):
    try:
        # Crear directorios si no existen
        if not os.path.exists(config_directory):
            os.makedirs(config_directory)
        
        config = {
            "user": user,
            "password": password,
            "route": ipatool_path
        }
        
        # Guardar configuración en el archivo
        with open(config_file, 'w') as json_file:
            json.dump(config, json_file, indent=4)
        print(f"Configuración guardada en {config_file}")

        # Actualizar página
        page.update()
    except Exception as e:
        print(f"Error guardando la configuración: {e}")

# Función para cargar la configuración desde el archivo JSON
def load_config():
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as json_file:
                config = json.load(json_file)
            return config
    except Exception as e:
        print(f"Error cargando la configuración: {e}")
    return None

# Función para descargar ipatool.exe
def download_ipatool(e):
    def download_file(url, dest, progress_callback):
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # No content length header
            dest.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            with open(dest, 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    progress_callback(dl / total_length)
                    
    def progress_callback(progress):
        progress_ring.value = progress
        e.page.update()

    try:
        download_file(ipatool_download_url, ipatool_path, progress_callback)
        print("ipatool.exe descargado y guardado correctamente.")
        e.control.visible = False  # Ocultar el botón de descarga
        progress_ring.visible = False
        save_button.enabled = True  # Habilitar el botón de guardar
        e.page.update()
    except Exception as ex:
        print(f"Error descargando ipatool.exe: {ex}")

# Manejador del evento de clic del botón de guardar
def save_button_clicked(e):
    save_config(user_input.value, password_input.value, e.page)

# Cargar configuración si existe
config = load_config()

# Cargar valores iniciales de configuración si existen
initial_user = config.get('user', '') if config else ''
initial_password = config.get('password', '') if config else ''

# Título de la página
title = ft.Text('Ajustes', size=30)

# Campo de texto para el nombre de usuario
user_input = ft.TextField(
    hint_text="Introduce tu nombre de usuario",
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
    value=initial_user,
)

# Campo de texto para la contraseña
password_input = ft.TextField(
    hint_text="Introduce tu contraseña",
    password=True,  # Esto asegura que el input se muestre como caracteres ocultos
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
    value=initial_password,
)

# Botón para guardar la configuración
save_button = ft.ElevatedButton(
    "Guardar",
    style=ft.ButtonStyle(
        color="#ffffff",
        bgcolor="#5B0098",
        overlay_color="#5B0098",
        shape=ft.RoundedRectangleBorder(radius=5),
        shadow_color="#5B0098",
        elevation=5,
    ),
    on_click=save_button_clicked,
)

# Botón para descargar ipatool.exe si no está presente
download_button = ft.IconButton(
    icon=ft.icons.FILE_DOWNLOAD,
    style=ft.ButtonStyle(
        color="#ffffff",
        bgcolor="#5B0098",
        shape=ft.RoundedRectangleBorder(radius=5),
    ),
    on_click=download_ipatool,
    visible=not os.path.exists(ipatool_path)
)

# Barra de progreso para la descarga
progress_ring = ft.ProgressRing(width=30, height=30, visible=not os.path.exists(ipatool_path), color='#5B0098')

# Desactivar el botón de guardar si ipatool.exe no está presente
save_button.enabled = os.path.exists(ipatool_path)

# Crear la página de ajustes
setting_page = ft.Stack(
    [
        ft.Container(
            content=ft.Column(
                controls=[
                    title, 
                    user_input, 
                    password_input, 
                    ft.Row(controls=[download_button, 
                                     progress_ring
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                     
                    save_button,
                
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        ),
    ],
    width=681,
    height=478,
)
