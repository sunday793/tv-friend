import flet as ft

class Poster(ft.Container):
    def __init__(self, title: str, image_url: str):
        super().__init__()
        self.title = title
        self.image_url = image_url

        # Dimensions optimized for a phone aspect ratio
        self.width = 130
        self.height = 200
        self.border_radius = 8
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        # self.bgcolor = ft.Colors.SURFACE
        
        # Build the structural layers of the poster
        self.content = ft.Stack(
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.PINK_100
                ),
                # Layer 1: The Poster Image
                ft.Image(
                    src=self.image_url,
                    fit = ft.BoxFit.COVER,
                    width=self.width,
                    height=self.height,
                ),
                # Layer 2: Gradient background overlay at bottom for title legibility
                ft.Container(
                    # gradient=ft.LinearGradient(
                    #     begin=ft.Alignment.TOP_CENTER,
                    #     end=ft.Alignment.TOP_CENTER,
                    #     colors=[ft.Colors.TRANSPARENT, ft.Colors.BLACK87],
                    # ),
                    alignment=ft.Alignment.BOTTOM_CENTER,
                    padding=8,
                    content=ft.Text(
                        self.title, 
                        size=14, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.WHITE,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        # bgcolor=ft.Colors.PINK_100
                    )
                )
            ],
            alignment=ft.Alignment.CENTER,
        )
