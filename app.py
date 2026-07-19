# app.py
import flet as ft
from components import Poster
from services import search_kinopoisk

def build_app(page: ft.Page):
    # User Input Field
    search_input = ft.TextField(
        hint_text="Search series, movies, K-dramas...",
        expand=True,
        on_submit=lambda e: run_search() # Allows pressing 'Enter' to execute search
    )
    
    # Clean Loading Indicator spinning animation
    loader = ft.ProgressRing(visible=False, color=ft.Colors.BLUE_400)
    
    # The fluid grid to hold your dynamically added Poster items
    results_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=300,
        spacing=10,
        run_spacing=10,
    )

    def run_search():
        # Clear past items and show spinner
        results_grid.controls.clear()
        loader.visible = True
        page.update()
        
        # Pull records from Kinopoisk Unofficial Service
        raw_items = search_kinopoisk(search_input.value)
        
        for item in raw_items:
            # Kinopoisk uses 'posterUrlPreview' for smaller fast loading images
            poster_url = item.get("posterUrlPreview")
            if poster_url:
                # English priority title selection fallback chain
                en_title = item.get("nameEn")
                ru_title = item.get("nameRu")
                display_name = en_title if en_title else ru_title
                
                # Default case protection if names field array parsing missing
                if not display_name:
                    display_name = "Untitled Show"
                
                # Instantiate your customized Poster component
                poster_card = Poster(title=display_name, image_url=poster_url)
                results_grid.controls.append(poster_card)
                
        # Turn off loading indicator wheel and paint new grid assets
        loader.visible = False
        page.update()

    search_button = ft.IconButton(
        icon=ft.Icons.SEARCH, 
        icon_color=ft.Colors.BLUE_400,
        on_click=lambda e: run_search()
    )

    # Compile layouts straight to visible view tree configurations
    page.add(
        ft.Row([search_input, search_button]),
        ft.Row([loader], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        results_grid
    )
    page.update()
