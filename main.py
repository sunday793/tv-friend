# main.py
import flet as ft
from app import build_app

def main(page: ft.Page):
    page.title = "TV Friend"
    page.window.width = 400
    page.window.height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Hand off control mechanics to the interface layer script
    build_app(page)

if __name__ == "__main__":
    ft.app(target=main)