import flet as ft
import asyncio
import math
from game import Game
from ui import UI

class RouletteApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Русская рулетка'
        self.page.window_width = 400
        self.page.window_height = 650
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        self.game = Game(lives=3, bullets=2) 
        self.ui = UI()

        self.bind_events()
        self.page.add(*self.ui.build())
    
    def bind_events(self):
        self.ui.shoot_btn.on_click = self.shoot
        self.ui.reset_btn.on_click = self.restart
    
    async def animate_drum(self):
        self.ui.drum.rotate += math.pi * 2
        self.ui.drum.src = "revolver.png" 
        self.page.update()
        await asyncio.sleep(0.5) 
    
    async def shoot(self, e):
        if not self.game.alive and self.game.lives > 0:
            self.ui.status.value = "Нужна перезарядка!"
            self.page.update()
            return
        elif self.game.lives <= 0:
            return

        self.ui.shoot_btn.disabled = True
        self.page.update()

        await self.animate_drum()
        result = self.game.shot()

        self.ui.lives.value = "❤️" * self.game.lives + "🖤" * (self.game.max_lives - self.game.lives)

        if result == "boom":
            self.ui.drum.src = "boom.png"
            self.ui.status.value ="🧨 BOOM!"
            self.ui.status.color = "red"
            
            if self.game.lives <= 0:
                self.show_dialog("Игра окончена ", "Жизни закончились. Вы проиграли!")
            else:
                self.show_dialog("Ранение!", f"Осталось жизней: {self.game.lives}. Нажмите перезарядку.")
        else:
            self.ui.drum.src = "safe.png"
            self.ui.status.value = " Фух, пронесло!"
            self.ui.status.color = 'green'
            
        self.ui.round.value = f'Раунд: {self.game.current_position} | Пуль: {self.game.bullets}'
        self.ui.shoot_btn.disabled = False
        self.page.update()
    
    def restart(self, e):
        if self.game.lives <= 0:
            self.game.full_reset()
            self.ui.lives.value = "❤️" * self.game.max_lives
        else:
            self.game.reset_round()
            
        self.ui.status.value ="Нажми на кнопку выстрел"
        self.ui.status.color = "white"
        self.ui.round.value = f"Раунд: 1 | Пуль: {self.game.bullets}"
        self.ui.drum.src = "revolver.png"

        self.page.update()
    
    def show_dialog(self, title, message):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog(dlg))
            ],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def close_dialog(self, dlg):
        dlg.open = False
        self.page.update()