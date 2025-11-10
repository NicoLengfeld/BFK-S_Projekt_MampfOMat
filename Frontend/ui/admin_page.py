import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
from ui.product_data import get_all_products, add_product, update_product, delete_product
import shutil
import os

class AdminPage(tk.Frame):
    """Administrationsbereich für Produktverwaltung"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Überschrift
        tk.Label(self, text="Administrationsbereich", font=("Arial", 18, "bold")).pack(pady=20)
        
        # Navigation
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill="x", padx=20, pady=10)
        tk.Button(nav_frame, text="Zurück zur Startseite", 
                 command=lambda: controller.show_frame("HomePage"),
                 bg="#e0e0e0", font=("Arial", 10)).pack(side="left")
        
        # Produktbereich
        self.products_frame = tk.Frame(self)
        self.products_frame.pack()

        self.images = []
        self.load_products()

        # Neues Produkt hinzufügen
        tk.Button(self, text="Neues Produkt hinzufügen", 
                 command=self.add_product_window,
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)

    def load_products(self):
        """Lädt alle Produkte und zeigt sie in der Oberfläche an"""
        # Bestehende Widgets entfernen
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        self.images.clear()

        # Produktliste aus der gemeinsamen Datenbank laden
        products = get_all_products()
        for i, product in enumerate(products):
            try:
                # Produktbild laden
                img = PhotoImage(file=product.get('image', f"assets/{product['name']}.png")).subsample(4, 4)
                self.images.append(img)
                
                # Produkt-Button erstellen
                btn = tk.Button(
                    self.products_frame,
                    image=img,
                    text=f"{product['name']}\n{product['price']:.2f} EUR",
                    compound="top",
                    command=lambda p=product: self.edit_product(p),
                    width=180, height=160,
                    relief="raised"
                )
                btn.grid(row=i//3, column=i%3, padx=20, pady=20)
            except tk.TclError:
                # Fallback wenn Bild nicht gefunden wird
                btn = tk.Button(
                    self.products_frame,
                    text=f"{product['name']}\n{product['price']:.2f} EUR\n(Bild nicht verfügbar)",
                    command=lambda p=product: self.edit_product(p),
                    width=20, height=8,
                    relief="raised"
                )
                btn.grid(row=i//3, column=i%3, padx=20, pady=20)

    def edit_product(self, product):
        """Öffnet Dialog zum Bearbeiten eines Produkts"""
        edit_window = tk.Toplevel(self)
        edit_window.title("Produkt bearbeiten")
        edit_window.geometry("350x350")
        edit_window.resizable(False, False)

        # Produktname
        tk.Label(edit_window, text="Produktname:", font=("Arial", 10)).pack(pady=5)
        name_var = tk.StringVar(value=product['name'])
        tk.Entry(edit_window, textvariable=name_var, width=25).pack(pady=5)

        # Preis
        tk.Label(edit_window, text="Preis (EUR):", font=("Arial", 10)).pack(pady=5)
        price_var = tk.DoubleVar(value=product['price'])
        tk.Entry(edit_window, textvariable=price_var, width=25).pack(pady=5)

        # Beschreibung
        tk.Label(edit_window, text="Beschreibung:", font=("Arial", 10)).pack(pady=5)
        desc_var = tk.StringVar(value=product['description'])
        desc_entry = tk.Entry(edit_window, textvariable=desc_var, width=25)
        desc_entry.pack(pady=5)

        # Bildpfad
        tk.Label(edit_window, text="Aktuelles Bild:", font=("Arial", 10)).pack(pady=5)
        image_var = tk.StringVar(value=product.get('image', ''))
        image_label = tk.Label(edit_window, text=os.path.basename(image_var.get()) if image_var.get() else "Kein Bild", 
                              bg="lightgray", width=30)
        image_label.pack(pady=5)

        def select_image():
            """Öffnet Dialog zur Bildauswahl"""
            file_path = filedialog.askopenfilename(
                title="Produktbild auswählen",
                filetypes=[("PNG Dateien", "*.png"), ("JPG Dateien", "*.jpg"), ("Alle Bilder", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                try:
                    # Kopiere Bild ins assets-Verzeichnis
                    filename = f"{name_var.get().replace(' ', '_')}.png"
                    assets_path = os.path.join("assets", filename)
                    shutil.copy2(file_path, assets_path)
                    image_var.set(assets_path)
                    image_label.config(text=filename)
                except Exception as e:
                    messagebox.showerror("Fehler", f"Bild konnte nicht kopiert werden: {str(e)}")

        tk.Button(edit_window, text="Bild auswählen", command=select_image,
                 bg="#2196F3", fg="white", width=15).pack(pady=5)

        def save_changes():
            """Speichert die Änderungen am Produkt"""
            try:
                update_product(
                    product['id'],
                    name_var.get().strip(),
                    float(price_var.get()),
                    desc_var.get().strip(),
                    image_var.get() if image_var.get() else product.get('image')
                )
                self.load_products()
                messagebox.showinfo("Erfolgreich", "Produkt wurde erfolgreich aktualisiert.")
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie einen gültigen Preis ein.")

        def delete_product_action():
            """Löscht das Produkt aus der Liste"""
            if messagebox.askyesno("Bestätigung", f"Möchten Sie das Produkt '{product['name']}' wirklich löschen?"):
                delete_product(product['id'])
                self.load_products()
                messagebox.showinfo("Erfolgreich", "Produkt wurde erfolgreich gelöscht.")
                edit_window.destroy()

        # Buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Speichern", command=save_changes,
                 bg="#4CAF50", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Löschen", command=delete_product_action,
                 bg="#f44336", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Abbrechen", command=edit_window.destroy,
                 bg="#808080", fg="white", width=10).pack(side="left", padx=5)

    def add_product_window(self):
        """Öffnet Dialog zum Hinzufügen eines neuen Produkts"""
        add_window = tk.Toplevel(self)
        add_window.title("Neues Produkt hinzufügen")
        add_window.geometry("350x400")
        add_window.resizable(False, False)

        # Produktname
        tk.Label(add_window, text="Produktname:", font=("Arial", 10)).pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var, width=25).pack(pady=5)

        # Preis
        tk.Label(add_window, text="Preis (EUR):", font=("Arial", 10)).pack(pady=5)
        price_var = tk.DoubleVar()
        tk.Entry(add_window, textvariable=price_var, width=25).pack(pady=5)

        # Beschreibung
        tk.Label(add_window, text="Beschreibung:", font=("Arial", 10)).pack(pady=5)
        desc_var = tk.StringVar()
        tk.Entry(add_window, textvariable=desc_var, width=25).pack(pady=5)

        # Bildauswahl
        tk.Label(add_window, text="Produktbild:", font=("Arial", 10)).pack(pady=5)
        image_var = tk.StringVar()
        image_label = tk.Label(add_window, text="Kein Bild ausgewählt", bg="lightgray", width=30)
        image_label.pack(pady=5)

        def select_image():
            """Öffnet Dialog zur Bildauswahl"""
            file_path = filedialog.askopenfilename(
                title="Produktbild auswählen",
                filetypes=[("PNG Dateien", "*.png"), ("JPG Dateien", "*.jpg"), ("Alle Bilder", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                try:
                    # Erstelle Dateinamen basierend auf Produktname
                    if name_var.get().strip():
                        filename = f"{name_var.get().strip().replace(' ', '_')}.png"
                    else:
                        filename = f"produkt_{len(get_all_products()) + 1}.png"
                    
                    # Kopiere Bild ins assets-Verzeichnis
                    assets_path = os.path.join("assets", filename)
                    shutil.copy2(file_path, assets_path)
                    image_var.set(assets_path)
                    image_label.config(text=filename)
                except Exception as e:
                    messagebox.showerror("Fehler", f"Bild konnte nicht kopiert werden: {str(e)}")

        tk.Button(add_window, text="Bild auswählen", command=select_image,
                 bg="#2196F3", fg="white", width=15).pack(pady=5)

        def add_new_product():
            """Fügt ein neues Produkt zur Liste hinzu"""
            try:
                if not name_var.get().strip():
                    messagebox.showerror("Fehler", "Bitte geben Sie einen Produktnamen ein.")
                    return
                
                # Standard-Bildpfad falls kein Bild ausgewählt wurde
                image_path = image_var.get() if image_var.get() else f"assets/{name_var.get().strip().replace(' ', '_')}.png"
                    
                add_product(
                    name_var.get().strip(),
                    float(price_var.get()),
                    desc_var.get().strip(),
                    image_path
                )
                self.load_products()
                messagebox.showinfo("Erfolgreich", "Neues Produkt wurde erfolgreich hinzugefügt.")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie einen gültigen Preis ein.")

        # Buttons
        button_frame = tk.Frame(add_window)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Hinzufügen", command=add_new_product,
                 bg="#4CAF50", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Abbrechen", command=add_window.destroy,
                 bg="#808080", fg="white", width=12).pack(side="left", padx=5)