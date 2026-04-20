import flet as ft
import smtplib
from email.message import EmailMessage
from ui import UI

class ProfileApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Анкеты'
        self.page.window_width = 500
        self.page.window_height = 800
        
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

        self.ui = UI()
        
        self.page.add(*self.ui.build())
        self.page.overlay.append(self.ui.file_picker)
        self.build_event()
        self.page.update() 
    
    def build_event(self):
        self.ui.button.on_click = self.create_profile
        self.ui.age.on_change = self.update_age
        
        self.ui.upload_btn.on_click = lambda _: self.ui.file_picker.pick_files(allow_multiple=False)
        self.ui.file_picker.on_result = self.on_photo_selected
    
    def update_age(self, e):
        self.ui.age_text.value = f'Возраст: {int(self.ui.age.value)}'
        self.page.update()

    def on_photo_selected(self, e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            self.ui.photo_path.value = e.files[0].name
            self.ui.photo_path.color = ft.Colors.GREEN
        else:
            self.ui.photo_path.value = "Фото не выбрано"
            self.ui.photo_path.color = ft.Colors.GREY
        self.page.update()

    def send_email(self, profile_data):
        email = "seidakhmatov_e@iuca.com"
        
        password = "1111" 

        msg = EmailMessage()
        msg.set_content(f"Новая анкета была успешно зарегистрирована!\n\nДетали:\n{profile_data}")
        msg['Subject'] = 'Уведомление: Новая Анкета'
        msg['From'] = email
        msg['To'] = email

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email, password)
            server.send_message(msg)
            server.quit()
            print("Письмо успешно отправлено!")
        except Exception as ex:
            print(f"Ошибка отправки почты: {ex}")

    def create_profile(self, e):
        has_error = False

        if not self.ui.name.value:
            self.ui.name.error_text = "Это поле обязательно"
            has_error = True
        else:
            self.ui.name.error_text = None

        if not self.ui.city.value:
            self.ui.city.error_text = "Выберите город"
            has_error = True
        else:
            self.ui.city.error_text = None

        if has_error:
            self.page.update()
            return

        skills = []
        if self.ui.skill1.value:
            skills.append("Python")
        if self.ui.skill2.value:
            skills.append("Django")
        if self.ui.skill3.value:
            skills.append("Flet")
        
        profile_data = (
            f'Имя: {self.ui.name.value}\n'
            f'Город: {self.ui.city.value}\n'
            f'Возраст: {int(self.ui.age.value)}\n'
            f'Навыки: {", ".join(skills)}\n'
            f'Уровень: {self.ui.level.value}\n'
            f'Готов к работе: {"Да" if self.ui.active.value else "Нет"}\n'
            f'Фото: {self.ui.photo_path.value}'
        )

        self.ui.result.value = profile_data
        self.ui.result.color = ft.Colors.GREEN
        self.page.update()

        self.send_email(profile_data)