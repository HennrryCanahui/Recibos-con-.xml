from Fac import Facturacion  # Importa la función Facturacion del módulo Fac
import flet as ft

def main(page: ft.Page):
    page.title = "Facturacion"

    def on_button_click(e):
        try:
            Facturacion()  # Llama a la función Facturacion del módulo Fac
            show_success_dialog()  # Muestra el diálogo de éxito
        except Exception as ex:
            show_error_dialog(str(ex))  # Muestra el diálogo de error con el mensaje de la excepción
    
    def show_success_dialog():
        dlg = ft.AlertDialog(
            title=ft.Text("Operación exitosa"),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))]
        )
        page.open(dlg)

    def show_error_dialog(message):
        dlg = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))]
        )
        page.open(dlg)

    page.add(
        ft.IconButton(
            icon=ft.icons.LOCAL_PRINTSHOP_ROUNDED,
            icon_size=80,
            on_click=on_button_click  # Asigna la función on_button_click al evento on_click del botón
        )
    )

ft.app(target=main)
