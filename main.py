import flet as ft
from views.home import home_page
from views.setting import setting_page

def main(page: ft.Page):
    page.title = "Applifi"
    page.window_width = 770
    page.window_height = 479
    page.window_resizable = False
    page.padding = 0
    page.fonts = {
        "nunito_dun": "fonts/Nunito-Bold.ttf",
        "nunito": "fonts/Nunito-VariableFont_wght.ttf",
    }
    page.theme = ft.Theme(font_family="nunito_dun")

    logo = ft.Container(
        content=ft.Image(src="img/logo.png", height=45, width=45),
        alignment=ft.alignment.center,
        height=47,
        margin=10,
    )

    a = ft.IconButton(
        icon=ft.icons.HOME,
        style=ft.ButtonStyle(
            color="#5B0098",
            bgcolor="#0C0C0C",
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
        on_click=lambda _: page.go("/"),
    )
    b = ft.IconButton(
        icon=ft.icons.SETTINGS,
        style=ft.ButtonStyle(
            color="#5B0098",
            bgcolor="#0C0C0C",
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
        on_click=lambda _: page.go("/setting"),
    )
    
    iconos = ft.Column(
        controls=[a, b],
        alignment=ft.MainAxisAlignment.END,  # Mueve los botones al fondo
        spacing=20
    )

    nab = ft.Container(
        content=ft.Column(
            controls=[logo, iconos],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=478,
        width=70,
        bgcolor="#131313",
        alignment=ft.alignment.center,
    )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            spacing=0,
                            controls=[
                                nab,
                                home_page,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    padding=0,
                )
            )
        elif page.route == "/setting":
            page.views.append(
                ft.View(
                    "/setting",
                    [
                        ft.Row(
                            spacing=0,
                            controls=[
                                nab,
                                setting_page,
                            ],
                        ),
                    ],
                    padding=0,
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir="assets")