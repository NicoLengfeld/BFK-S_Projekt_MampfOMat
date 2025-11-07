import tkinter as tk
from ui.home_page import HomePage
from ui.product_page import ProductPage
from ui.cart_page import CartPage
from ui.thankyou_page import ThankYouPage
from ui.admin_page import AdminPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bäckerautomat")
        self.geometry("800x600")
        self.cart = {}  # speichert Produkte & Mengen

        # Container für alle Seiten
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, ProductPage, CartPage, ThankYouPage, AdminPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name, **kwargs):
        frame = self.frames[page_name]
        if hasattr(frame, "update_page"):
            frame.update_page(**kwargs)
        frame.tkraise()
