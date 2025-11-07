import tkinter as tk

class ThankYouPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="🙏 Vielen Dank für Ihre Bestellung!", font=("Arial", 18)).pack(pady=30)
        tk.Label(self, text="Gleich kommt Ihr Produkt heraus 😋", font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Zurück zur Startseite", command=lambda: controller.show_frame("HomePage")).pack(pady=20)
