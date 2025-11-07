import tkinter as tk
from tkinter import PhotoImage

class ProductPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product = None

        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)
        self.name_label = tk.Label(self, font=("Arial", 18))
        self.name_label.pack()
        self.desc_label = tk.Label(self, wraplength=400)
        self.desc_label.pack(pady=10)

        self.qty_var = tk.IntVar(value=1)
        tk.Label(self, text="Menge:").pack()
        tk.Entry(self, textvariable=self.qty_var, width=5).pack()

        self.price_label = tk.Label(self, text="Preis: 0.00€", font=("Arial", 14))
        self.price_label.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Abbrechen", command=lambda: controller.show_frame("HomePage")).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Weiter", command=self.add_to_cart).grid(row=0, column=1, padx=10)

    def update_page(self, product):
        self.product = product
        img = PhotoImage(file=product["image"]).subsample(3, 3)
        self.image_label.config(image=img)
        self.image_label.image = img
        self.name_label.config(text=product["name"])
        self.desc_label.config(text=f"Leckere {product['name']} – frisch gebacken!")
        self.price_label.config(text="Preis: 1.50€")

    def add_to_cart(self):
        name = self.product["name"]
        qty = self.qty_var.get()
        self.controller.cart[name] = qty
        self.controller.show_frame("CartPage")
