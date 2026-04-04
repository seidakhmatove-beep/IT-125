import flet as ft
import json
import os
import datetime
import threading
import time

class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "TODO Планировщик"
        
        try:
            self.page.window.width = 600
            self.page.window.height = 700
        except AttributeError:
            self.page.window_width = 600
            self.page.window_height = 700

        self.tasks = []
        self.load_data()
        self.build_ui()
        
        threading.Thread(target=self.check_deadlines, daemon=True).start()

    def load_data(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []

    def save_data(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def build_ui(self):
        self.task_input = ft.TextField(label="Задача", width=250)
        
        self.priority = ft.Dropdown(
            label="Приоритет",
            width=150,
            options=[
                ft.dropdown.Option("Высокий"),
                ft.dropdown.Option("Средний"),
                ft.dropdown.Option("Низкий"),
            ],
        )
        
        self.deadline_input = ft.TextField(
            label="Дедлайн (ГГГГ-ММ-ДД)", 
            width=250, 
            hint_text="Например: 2024-12-31"
        )

        add_btn = ft.ElevatedButton("Добавить", on_click=self.add_task)

        self.search_input = ft.TextField(
            label="Поиск задач", 
            width=600, 
            on_change=lambda e: self.update_tasks()
        )
        
        self.stats_text = ft.Text("Всего: 0 | Выполнено: 0 | Осталось: 0", weight="bold", size=16)

        self.task_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        self.page.add(
            ft.Text("Планировщик задач", size=24, weight="bold", color=ft.Colors.BLUE),
            self.stats_text,
            self.search_input,
            ft.Row([self.task_input, self.priority]),
            ft.Row([self.deadline_input, add_btn]),
            ft.Divider(),
            self.task_list
        )
        
        self.update_tasks()

    def add_task(self, e):
        if not self.task_input.value or not self.priority.value:
            self.show_message("Заполните название и приоритет!")
            return

        dl_val = self.deadline_input.value.strip()
        if dl_val:
            try:
                datetime.datetime.strptime(dl_val, "%Y-%m-%d")
            except ValueError:
                self.show_message("Неверный формат дедлайна! Используйте ГГГГ-ММ-ДД")
                return

        task = {
            "title": self.task_input.value,
            "priority": self.priority.value,
            "completed": False,
            "deadline": dl_val,
            "notified": False
        }

        self.tasks.append(task)
        self.save_data()

        self.task_input.value = ""
        self.priority.value = None
        self.deadline_input.value = ""

        self.update_tasks()
        self.page.update()

    def update_tasks(self):
        self.task_list.controls.clear()
        
        search_query = self.search_input.value.lower() if self.search_input.value else ""
        
        total = len(self.tasks)
        completed_count = 0

        for index, task in enumerate(self.tasks):
            is_completed = task.get("completed", False)
            if is_completed:
                completed_count += 1
                
            if search_query and search_query not in task["title"].lower():
                continue

            color = ft.Colors.BLACK
            if task["priority"] == "Высокий":
                color = ft.Colors.RED
            elif task["priority"] == "Средний":
                color = ft.Colors.ORANGE
            elif task["priority"] == "Низкий":
                color = ft.Colors.GREEN

            deadline_str = f" {task['deadline']}" if task.get("deadline") else ""

            text_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH, color=ft.Colors.GREY) if is_completed else ft.TextStyle(color=color)

            task_row = ft.Row(
                [
                    ft.Row([
                        ft.Checkbox(
                            value=is_completed,
                            on_change=lambda e, i=index: self.toggle_complete(i)
                        ),
                        ft.Text(
                            f"[{task['priority']}] {task['title']}{deadline_str}",
                            style=text_style,
                            size=16
                        ),
                    ]),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        on_click=lambda e, i=index: self.delete_task(i)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

            self.task_list.controls.append(task_row)

        self.stats_text.value = f"Всего: {total} | Выполнено: {completed_count} | Осталось: {total - completed_count}"
        self.page.update()

    def toggle_complete(self, index):
        self.tasks[index]["completed"] = not self.tasks[index].get("completed", False)
        self.save_data()
        self.update_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_data()
        self.update_tasks()

    def show_message(self, message):
        snack = ft.SnackBar(ft.Text(message), bgcolor=ft.Colors.RED_700)
        try:
            self.page.open(snack)
        except AttributeError:
            self.page.snack_bar = snack
            snack.open = True
            self.page.update()
        
    def alert_deadline(self, title):
        dlg = ft.AlertDialog(
            title=ft.Text("Дедлайн наступил!", color=ft.Colors.RED),
            content=ft.Text(f"Пора выполнить задачу:\n\n«{title}»"),
        )
        try:
            self.page.open(dlg)
        except AttributeError:
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

    def check_deadlines(self):
        while True:
            now = datetime.datetime.now()
            changed = False
            
            for task in self.tasks:
                if not task.get("completed") and not task.get("notified") and task.get("deadline"):
                    try:
                        dt = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d")
                        if now >= dt:
                            task["notified"] = True
                            changed = True
                            self.alert_deadline(task["title"])
                    except ValueError:
                        pass
                        
            if changed:
                self.save_data()
                
            time.sleep(10)


def main(page: ft.Page):
    TodoApp(page)

if __name__ == "__main__":
    ft.app(target=main)