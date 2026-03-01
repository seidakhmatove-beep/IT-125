import tkinter as tk
from tkinter import messagebox, ttk

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Каталог сотрудников")
        self.root.geometry("500x700")

        self.employees = []

        self.setup_ui()

    def setup_ui(self):
        # ну это контейнер для формы как я понял
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(form_frame)
        self.ent_name.grid(row=0, column=1, pady=5, sticky="we")

        tk.Label(form_frame, text="Фамилия:").grid(row=1, column=0, sticky="w")
        self.ent_surname = tk.Entry(form_frame)
        self.ent_surname.grid(row=1, column=1, pady=5, sticky="we")

        tk.Label(form_frame, text="Возраст:").grid(row=2, column=0, sticky="w")
        self.ent_age = tk.Entry(form_frame)
        self.ent_age.grid(row=2, column=1, pady=5, sticky="we")

        tk.Label(form_frame, text="Должность:").grid(row=3, column=0, sticky="w")
        self.combo_role = ttk.Combobox(form_frame, values=["Разработчик", "Дизайнер", "Менеджер", "Тестировщик"])
        self.combo_role.grid(row=3, column=1, pady=5, sticky="we")
        self.combo_role.current(0)

        tk.Label(form_frame, text="Зарплата:").grid(row=4, column=0, sticky="w")
        self.ent_salary = tk.Entry(form_frame)
        self.ent_salary.grid(row=4, column=1, pady=5, sticky="we")

        # кнопочка для добавления
        self.btn_add = tk.Button(form_frame, text="Добавить сотрудника", command=self.add_employee, bg="#4CAF50", fg="white")
        self.btn_add.grid(row=5, column=0, columnspan=2, pady=15, sticky="we")

        # вывод данных
        tk.Label(self.root, text="Список сотрудников (сортировка по зарплате):", font=("Arial", 10, "bold")).pack()
        
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

    def add_employee(self):
        #  сборка данных
        name = self.ent_name.get().strip()
        surname = self.ent_surname.get().strip()
        age_str = self.ent_age.get().strip()
        role = self.combo_role.get()
        salary_str = self.ent_salary.get().strip()

        # вид
        if not (name and surname and age_str and salary_str):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            age = int(age_str)
            salary = float(salary_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст и зарплата должны быть числами!")
            return

        # save
        new_emp = {
            "name": name,
            "surname": surname,
            "age": age,
            "role": role,
            "salary": salary
        }
        self.employees.append(new_emp)
        
        # Сортировка,кажется с малого до большого 
        self.employees.sort(key=lambda x: x['salary'])
        
        self.clear_form()
        self.refresh_list()

    def clear_form(self):
        self.ent_name.delete(0, tk.END)
        self.ent_surname.delete(0, tk.END)
        self.ent_age.delete(0, tk.END)
        self.ent_salary.delete(0, tk.END)

    def delete_employee(self, emp_dict):
        self.employees.remove(emp_dict)
        self.refresh_list()

    def refresh_list(self):
        # очистка 
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # это вроде сортировка обновленого списка
        for emp in self.employees:
            # цвет подсветки, если зп > 100 000
            bg_color = "#ffffcc" if emp['salary'] > 100000 else "#f0f0f0"
            
            card = tk.Frame(self.scrollable_frame, bg=bg_color, bd=1, relief="solid", pady=5, padx=5)
            card.pack(fill="x", pady=2, padx=5)

            info_text = f"{emp['name']} {emp['surname']} ({emp['age']} лет) \n{emp['role']} — {emp['salary']:.2f} руб."
            tk.Label(card, text=info_text, bg=bg_color, justify="left").pack(side="left")

            btn_del = tk.Button(card, text="Удалить", command=lambda e=emp: self.delete_employee(e), bg="#ff4d4d", fg="white")
            btn_del.pack(side="right")
# это уже запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()