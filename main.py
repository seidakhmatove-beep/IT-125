import tkinter as tk
import pygame
import os
from PIL import Image, ImageTk

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def abs_path(file):
    return os.path.join(BASE_DIR, file)

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

current_img = None

def show_image(file, label):
    global current_img
    img = Image.open(file)
    img = img.resize((300, 200))
    current_img = ImageTk.PhotoImage(img)
    label.config(image=current_img)

def create_app():
    root = tk.Tk()
    root.title("Moto Exhaust Sounds")
    root.geometry('370x600')
    root.resizable(False, False)


    image_label = tk.Label(root)
    image_label.pack()

    # Кнопка Fishing
    tk.Button(root, text="Fishing", font=("Arial", 14),
              command=lambda: [play_sound(abs_path("sounds/Fishing(1).mp3")),
                               show_image(abs_path("photos/fishing1.jpg"), image_label)]
             ).pack(pady=10)

    #r1
    tk.Button(root, text="Fishing 2", font=("Arial", 14),
              command=lambda: [play_sound(abs_path("sounds/Fishing(2).mp3")),
                               show_image(abs_path("photos/Fishing2.jpg"), image_label)]
              ).pack(pady=10)

    #r6
    tk.Button(root, text="Fishing 3", font=("Arial", 14),
              command=lambda: [play_sound(abs_path("sounds/Fishing(3).mp3")),
                               show_image(abs_path("photos/Fishing3.jpg"), image_label)]
              ).pack(pady=10)

    #cbr1000
    tk.Button(root, text="Fishing 4", font=("Arial", 14),
              command=lambda: [play_sound(abs_path("sounds/Fishing(4).mp3")),
                               show_image(abs_path("photos/Fishing 4.jpg"), image_label)]
              ).pack(pady=10)

    #h2r
    tk.Button(root, text="Fishing 5", font=("Arial", 14),
              command=lambda: [play_sound(abs_path("sounds/Fishing(5).mp3")),
                               show_image(abs_path("photos/Fishing5.jpg"), image_label)]
              ).pack(pady=10)

    root.mainloop()

create_app()