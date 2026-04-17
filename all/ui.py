import flet as ft

class UI:
    def __init__(self):
        self.title = ft.Text("Русская рулетка", size=26, weight="bold")
        self.status = ft.Text("Нажми выстрел", size=20)
        self.round = ft.Text("Раунд: 1 | Пуль: 2")
        self.lives = ft.Text("❤️❤️❤️", size=24)

        self.drum = ft.Image(
            src="revolver.png",
            width=150,
            height=150,
            fit="contain",
            rotate=0, 
            animate_rotation=500 
        )

        self.shoot_btn = ft.ElevatedButton("🔫 Выстрел", width=200, height=50)
        self.reset_btn = ft.ElevatedButton("🔃 Перезарядка", width=200, height=50)
    
    def build(self):
        return [
            ft.Column(
                [
                    self.title,
                    self.lives,
                    self.drum,
                    self.status,
                    self.round,
                    self.shoot_btn,
                    self.reset_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        ]