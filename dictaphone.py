
import tkinter as tk
import sounddevice as sd
import wavio
import threading
import speech_recognition as sr

SAMPLE_RATE = 44100
DURATION = 3  

def record_audio(file_name="temp.wav"):
    print("Запись...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    wavio.write(file_name, recording, SAMPLE_RATE, sampwidth=2)
    print("Запись завершена")
    return file_name

def recognize_animal(file_name):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        text = text.lower()
        print("Распознано:", text)
        if "гав" in text:
            return "Собака"
        elif "мяу" in text:
            return "Кошка"
        else:
            return "Не удалось определить"
    except:
        return "Не удалось распознать звук"

def start_recording(label):
    def worker():
        file_name = record_audio()
        result = recognize_animal(file_name)
        label.config(text=f"Это: {result}")
    threading.Thread(target=worker).start()

def create_app():
    root = tk.Tk()
    root.title("Animal Sound Detector")
    root.geometry('300x200')
    root.resizable(False, False)

    label = tk.Label(root, text="Нажмите 'Записать'", font=("Arial", 14))
    label.pack(pady=20)

    tk.Button(root, text="Записать", font=("Arial", 14),
              command=lambda: start_recording(label)).pack(pady=10)

    root.mainloop()

create_app()