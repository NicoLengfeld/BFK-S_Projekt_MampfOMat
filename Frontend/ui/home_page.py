import tkinter as tk
from PIL import Image, ImageTk  # <--- wichtig für Größenanpassung der Bilder!
from tkinter import PhotoImage, messagebox
from ui.product_data import get_all_products

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Willkommen beim Bäckerautomaten", font=("Arial", 18, "bold")).pack(pady=20)

        self.products_frame = tk.Frame(self)
        self.products_frame.pack()

        self.images = []
        self.load_products()

        # --- Anmelde-Button unten links ---
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(fill="x", pady=10, padx=20)

        self.login_button = tk.Button(
            self.bottom_frame,
            text="Anmelden",
            font=("Arial", 12),
            bg="#d0d0d0",
            relief="raised",
            command=self.open_login
        )
        self.login_button.pack(side="left", anchor="sw")

    def open_login(self):
        """Öffnet das Login-Fenster für Admin-Zugang"""
        popup = tk.Toplevel(self)
        popup.title("Administrator Anmeldung")
        popup.geometry("350x250")
        popup.resizable(False, False)
        popup.grab_set()  # Modal dialog
        
        # Zentriere das Fenster
        popup.transient(self.controller)
        
        tk.Label(popup, text="Administrator Login", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Benutzername
        tk.Label(popup, text="Benutzername:", font=("Arial", 10)).pack(pady=5)
        username_var = tk.StringVar()
        username_entry = tk.Entry(popup, textvariable=username_var, width=20, font=("Arial", 10))
        username_entry.pack(pady=5)
        
        # Passwort
        tk.Label(popup, text="Passwort:", font=("Arial", 10)).pack(pady=5)
        password_var = tk.StringVar()
        password_entry = tk.Entry(popup, textvariable=password_var, show="*", width=20, font=("Arial", 10))
        password_entry.pack(pady=5)
        
        # Status Label für Fehlermeldungen
        status_label = tk.Label(popup, text="", fg="red", font=("Arial", 9))
        status_label.pack(pady=5)
        
        def try_login():
            """Überprüft die Anmeldedaten und gewährt Admin-Zugang"""
            username = username_var.get()
            password = password_var.get()
            
            # Einfache Admin-Authentifizierung
            if username == "admin" and password == "admin":
                popup.destroy()
                self.controller.show_frame("AdminPage")
                messagebox.showinfo("Login erfolgreich", "Sie wurden erfolgreich als Administrator angemeldet.")
            else:
                status_label.config(text="Ungültige Anmeldedaten. Bitte versuchen Sie es erneut.")
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                username_entry.focus()
        
        def cancel_login():
            """Schließt das Login-Fenster"""
            popup.destroy()
            
        # Button-Container
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=15)
        
        # Anmelden Button
        login_btn = tk.Button(button_frame, text="Anmelden", command=try_login, 
                             bg="#4CAF50", fg="white", font=("Arial", 10), width=10)
        login_btn.pack(side="left", padx=5)
        
        # Abbrechen Button
        cancel_btn = tk.Button(button_frame, text="Abbrechen", command=cancel_login, 
                              bg="#f44336", fg="white", font=("Arial", 10), width=10)
        cancel_btn.pack(side="left", padx=5)
        
        # Enter-Taste für Login
        popup.bind('<Return>', lambda event: try_login())
        
        # Setze Fokus auf Benutzername-Eingabefeld
        username_entry.focus()

    def load_products(self):
        """Lädt alle Produkte und zeigt sie auf der Hauptseite an"""
        # Bestehende Widgets entfernen
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        self.images.clear()

        # Aktuelle Produktliste laden
        products = get_all_products()
        for i, product in enumerate(products):
            try:
                # Öffne Bild mit Pillow, skaliere es auf 120x120 Pixel
                image_path = product.get("image", f"assets/{product['name']}.png")
                img = Image.open(image_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)  # gleich große Bilder
                tk_img = ImageTk.PhotoImage(img)
                self.images.append(tk_img)

                # Erstelle Button mit Bild
                btn = tk.Button(
                    self.products_frame,
                    image=tk_img,
                    text=product["name"],
                    compound="top",
                    command=lambda p=product: self.controller.show_frame("ProductPage", product=p),
                    width=160, height=160,  # sorgt für gleich große Buttons
                    relief="raised",
                    bg="white"
                )
                btn.grid(row=i // 3, column=i % 3, padx=20, pady=20)
            except Exception as e:
                print(f"Fehler beim Laden des Produkts {product['name']}: {e}")
                # Fallback wenn Bild nicht gefunden wird
                btn = tk.Button(
                    self.products_frame,
                    text=f"{product['name']}\n(Bild nicht verfügbar)",
                    command=lambda p=product: self.controller.show_frame("ProductPage", product=p),
                    width=20, height=8,
                    relief="raised",
                    bg="lightgray"
                )
                btn.grid(row=i // 3, column=i % 3, padx=20, pady=20)

    def update_page(self, **kwargs):
        """Wird aufgerufen, wenn die Seite angezeigt wird - aktualisiert die Produktliste"""
        self.load_products()

