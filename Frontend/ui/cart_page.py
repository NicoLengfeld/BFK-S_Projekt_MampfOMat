import tkinter as tk

class CartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="🛒 Ihr Warenkorb", font=("Arial", 18)).pack(pady=20)
        self.cart_list = tk.Label(self, font=("Arial", 14))
        self.cart_list.pack(pady=10)

        tk.Button(self, text="Weitere Produkte", command=lambda: controller.show_frame("HomePage")).pack(pady=5)
        tk.Button(self, text="Bestellung abschließen", command=lambda: controller.show_frame("ThankYouPage")).pack(pady=5)

    def update_page(self):
        text = ""
        total = 0
        for name, qty in self.controller.cart.items():
            price = 1.5 * qty
            total += price
            text += f"{name} x{qty} = {price:.2f}€\n"
        text += f"\nGesamt: {total:.2f}€"
        self.cart_list.config(text=text)
