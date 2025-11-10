import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
from ui.product_data import get_all_products, add_product, update_product, delete_product
from ui.modern_styles import COLORS, FONTS, LAYOUT, create_modern_button, create_modern_card, apply_hover_effect
from PIL import Image, ImageTk
import shutil
import os

class AdminPage(tk.Frame):
    """Moderner Administrationsbereich für Produktverwaltung"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['background_main'])
        self.controller = controller
        self.images = []
        self.product_cards = []
        
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        """Erstellt die moderne Admin-UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header-Bereich
        self.create_header()
        
        # Produktverwaltung
        self.create_products_management()
        
        # Aktionsbereich
        self.create_actions_area()

    def create_header(self):
        """Erstellt den modernen Header"""
        header_frame = tk.Frame(
            self,
            bg=COLORS['background_main'],
            height=100
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=LAYOUT['padding_large'], pady=LAYOUT['padding_large'])
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Titel links
        title_label = tk.Label(
            header_frame,
            text="Produktverwaltung",
            font=FONTS['heading_large'],
            fg=COLORS['text_primary'],
            bg=COLORS['background_main']
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Navigation rechts
        nav_frame = tk.Frame(header_frame, bg=COLORS['background_main'])
        nav_frame.grid(row=0, column=2, sticky="e")
        
        back_btn = create_modern_button(
            nav_frame,
            "← Zurück zur Startseite",
            style='secondary',
            command=lambda: self.controller.show_frame("HomePage")
        )
        back_btn.pack(side="right")

    def create_products_management(self):
        """Erstellt den Produktverwaltungsbereich"""
        # Container
        management_frame = tk.Frame(self, bg=COLORS['background_main'])
        management_frame.grid(row=1, column=0, sticky="nsew", padx=LAYOUT['padding_large'])
        management_frame.grid_columnconfigure(0, weight=1)
        management_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollbarer Bereich
        canvas = tk.Canvas(
            management_frame,
            bg=COLORS['background_main'],
            highlightthickness=0,
            bd=0
        )
        scrollbar = tk.Scrollbar(
            management_frame,
            orient="vertical",
            command=canvas.yview,
            bg=COLORS['accent_silver'],
            width=12
        )
        
        self.products_frame = tk.Frame(canvas, bg=COLORS['background_main'])
        
        # Scrollbar konfigurieren
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Frame im Canvas
        canvas_window = canvas.create_window((0, 0), window=self.products_frame, anchor="nw")
        
        # Responsive Verhalten
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = canvas.winfo_width()
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        self.products_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Mausrad-Scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def create_actions_area(self):
        """Erstellt den Aktionsbereich"""
        actions_frame = tk.Frame(
            self,
            bg=COLORS['background_main'],
            height=80
        )
        actions_frame.grid(row=2, column=0, sticky="ew", padx=LAYOUT['padding_large'], pady=LAYOUT['padding_medium'])
        actions_frame.grid_propagate(False)
        
        # Neues Produkt Button
        add_btn = create_modern_button(
            actions_frame,
            "Neues Produkt hinzufügen",
            style='success',
            command=self.add_product_window
        )
        add_btn.pack(side="left")

    def load_products(self):
        """Lädt alle Produkte mit modernem Card-Design"""
        # Bestehende Cards entfernen
        for card in self.product_cards:
            card.destroy()
        self.product_cards.clear()
        self.images.clear()

        # Produktliste laden
        products = get_all_products()
        
        # Grid-Layout
        cols = 2  # 2 Spalten für Admin-View
        for i, product in enumerate(products):
            row = i // cols
            col = i % cols
            
            # Admin-Produktkarte erstellen
            card = self.create_admin_product_card(product)
            card.grid(
                row=row,
                column=col,
                padx=LAYOUT['padding_medium'],
                pady=LAYOUT['padding_medium'],
                sticky="ew"
            )
            self.product_cards.append(card)
        
        # Spalten gleichmäßig verteilen
        for col in range(cols):
            self.products_frame.grid_columnconfigure(col, weight=1, uniform="admin_col")

    def create_admin_product_card(self, product):
        """Erstellt eine Admin-Produktkarte mit erweiterten Funktionen"""
        card = create_modern_card(self.products_frame)
        
        # Card konfigurieren
        card.configure(width=500, height=200)
        card.grid_propagate(False)
        card.grid_columnconfigure(1, weight=1)
        
        try:
            # Produktbild
            image_path = product.get('image', f"assets/{product['name']}.png")
            img = Image.open(image_path)
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)
            
            img_label = tk.Label(
                card,
                image=tk_img,
                bg=COLORS['background_card'],
                bd=1,
                relief='solid',
                borderwidth=1
            )
            img_label.grid(row=0, column=0, rowspan=4, padx=LAYOUT['padding_medium'], pady=LAYOUT['padding_medium'])
            
        except Exception as e:
            print(f"Fehler beim Laden des Admin-Produktbilds {product['name']}: {e}")
            placeholder_label = tk.Label(
                card,
                text="📷",
                font=FONTS['heading_medium'],
                fg=COLORS['text_secondary'],
                bg=COLORS['background_hover'],
                width=15,
                height=6
            )
            placeholder_label.grid(row=0, column=0, rowspan=4, padx=LAYOUT['padding_medium'], pady=LAYOUT['padding_medium'])
        
        # Produktinformationen
        info_frame = tk.Frame(card, bg=COLORS['background_card'])
        info_frame.grid(row=0, column=1, sticky="ew", padx=LAYOUT['padding_medium'])
        
        # Produktname
        name_label = tk.Label(
            info_frame,
            text=product["name"],
            font=FONTS['heading_small'],
            fg=COLORS['text_primary'],
            bg=COLORS['background_card'],
            anchor="w"
        )
        name_label.pack(fill="x", pady=(0, LAYOUT['padding_small']))
        
        # Preis
        price_label = tk.Label(
            info_frame,
            text=f"Preis: {product['price']:.2f} €",
            font=FONTS['body_large'],
            fg=COLORS['accent_gold'],
            bg=COLORS['background_card'],
            anchor="w"
        )
        price_label.pack(fill="x", pady=(0, LAYOUT['padding_small']))
        
        # Beschreibung
        desc_text = product.get('description', 'Keine Beschreibung')
        if len(desc_text) > 80:
            desc_text = desc_text[:77] + "..."
        
        desc_label = tk.Label(
            info_frame,
            text=f"Beschreibung: {desc_text}",
            font=FONTS['body_medium'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background_card'],
            anchor="w",
            justify='left',
            wraplength=300
        )
        desc_label.pack(fill="x", pady=(0, LAYOUT['padding_small']))
        
        # ID (für interne Referenz)
        id_label = tk.Label(
            info_frame,
            text=f"ID: {product['id']}",
            font=FONTS['caption'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background_card'],
            anchor="w"
        )
        id_label.pack(fill="x")
        
        # Aktions-Buttons
        actions_frame = tk.Frame(card, bg=COLORS['background_card'])
        actions_frame.grid(row=1, column=1, sticky="ew", padx=LAYOUT['padding_medium'], pady=LAYOUT['padding_small'])
        
        edit_btn = create_modern_button(
            actions_frame,
            "Bearbeiten",
            style='primary',
            command=lambda: self.edit_product(product)
        )
        edit_btn.pack(side="left", padx=(0, LAYOUT['padding_small']))
        
        delete_btn = create_modern_button(
            actions_frame,
            "Löschen",
            style='danger',
            command=lambda: self.confirm_delete_product(product)
        )
        delete_btn.pack(side="left")
        
        # Hover-Effekt
        apply_hover_effect(card, COLORS['background_hover'], COLORS['background_card'])
        
        return card

    def confirm_delete_product(self, product):
        """Bestätigung vor dem Löschen eines Produkts"""
        if messagebox.askyesno(
            "Produkt löschen",
            f"Möchten Sie das Produkt '{product['name']}' wirklich löschen?\n\nDiese Aktion kann nicht rückgängig gemacht werden.",
            icon='warning'
        ):
            delete_product(product['id'])
            self.load_products()
            messagebox.showinfo("Erfolgreich", f"Produkt '{product['name']}' wurde erfolgreich gelöscht.")

    def edit_product(self, product):
        """Öffnet das moderne Bearbeitungsfenster"""
        self.open_product_dialog(product, mode='edit')

    def add_product_window(self):
        """Öffnet das moderne Hinzufügungsfenster"""
        self.open_product_dialog(None, mode='add')

    def open_product_dialog(self, product=None, mode='add'):
        """Öffnet einen modernen Produktdialog"""
        is_edit = (mode == 'edit' and product is not None)
        title = "Produkt bearbeiten" if is_edit else "Neues Produkt hinzufügen"
        
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS['background_main'])
        dialog.grab_set()
        dialog.transient(self.controller)
        
        # Zentrieren
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg=COLORS['primary_dark'], height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text=title,
            font=FONTS['heading_medium'],
            fg=COLORS['text_light'],
            bg=COLORS['primary_dark']
        )
        header_label.pack(pady=LAYOUT['padding_large'])
        
        # Formular
        form_frame = tk.Frame(dialog, bg=COLORS['background_main'])
        form_frame.pack(fill="both", expand=True, padx=LAYOUT['padding_xlarge'], pady=LAYOUT['padding_large'])
        
        # Variablen
        name_var = tk.StringVar(value=product['name'] if is_edit else '')
        price_var = tk.DoubleVar(value=product['price'] if is_edit else 0.0)
        desc_var = tk.StringVar(value=product.get('description', '') if is_edit else '')
        image_var = tk.StringVar(value=product.get('image', '') if is_edit else '')
        
        # Produktname
        self.create_form_field(form_frame, "Produktname", name_var, 'entry')
        
        # Preis
        self.create_form_field(form_frame, "Preis (EUR)", price_var, 'entry')
        
        # Beschreibung
        self.create_form_field(form_frame, "Beschreibung", desc_var, 'text')
        
        # Bildauswahl
        self.create_image_field(form_frame, "Produktbild", image_var, name_var)
        
        # Button-Bereich
        button_frame = tk.Frame(form_frame, bg=COLORS['background_main'])
        button_frame.pack(fill="x", pady=LAYOUT['padding_large'])
        
        def save_product():
            try:
                name = name_var.get().strip()
                price = float(price_var.get())
                description = desc_var.get().strip()
                image_path = image_var.get() if image_var.get() else f"assets/{name.replace(' ', '_')}.png"
                
                if not name:
                    messagebox.showerror("Fehler", "Bitte geben Sie einen Produktnamen ein.")
                    return
                
                if is_edit:
                    update_product(product['id'], name, price, description, image_path)
                    messagebox.showinfo("Erfolgreich", "Produkt wurde erfolgreich aktualisiert.")
                else:
                    add_product(name, price, description, image_path)
                    messagebox.showinfo("Erfolgreich", "Neues Produkt wurde erfolgreich hinzugefügt.")
                
                self.load_products()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Fehler", "Bitte geben Sie einen gültigen Preis ein.")
        
        # Buttons
        save_btn = create_modern_button(
            button_frame,
            "Speichern" if is_edit else "Hinzufügen",
            style='success',
            command=save_product
        )
        save_btn.pack(side="left", padx=(0, LAYOUT['padding_small']))
        
        cancel_btn = create_modern_button(
            button_frame,
            "Abbrechen",
            style='secondary',
            command=dialog.destroy
        )
        cancel_btn.pack(side="left")

    def create_form_field(self, parent, label_text, variable, field_type='entry'):
        """Erstellt ein modernes Formularfeld"""
        field_frame = tk.Frame(parent, bg=COLORS['background_main'])
        field_frame.pack(fill="x", pady=(0, LAYOUT['padding_medium']))
        
        label = tk.Label(
            field_frame,
            text=label_text,
            font=FONTS['body_large'],
            fg=COLORS['text_primary'],
            bg=COLORS['background_main']
        )
        label.pack(anchor="w", pady=(0, LAYOUT['padding_small']))
        
        if field_type == 'entry':
            entry = tk.Entry(
                field_frame,
                textvariable=variable,
                font=FONTS['body_large'],
                relief='flat',
                bd=1,
                highlightthickness=1,
                highlightcolor=COLORS['text_accent'],
                highlightbackground=COLORS['border_light']
            )
            entry.pack(fill="x", ipady=LAYOUT['padding_small'])
        elif field_type == 'text':
            text_frame = tk.Frame(field_frame, bg=COLORS['background_main'])
            text_frame.pack(fill="x")
            
            text_widget = tk.Text(
                text_frame,
                height=3,
                font=FONTS['body_medium'],
                relief='flat',
                bd=1,
                highlightthickness=1,
                highlightcolor=COLORS['text_accent'],
                highlightbackground=COLORS['border_light']
            )
            text_widget.pack(fill="x")
            
            # Text Widget mit StringVar verbinden
            def update_text(*args):
                text_widget.delete(1.0, tk.END)
                text_widget.insert(1.0, variable.get())
            
            def text_changed(event=None):
                variable.set(text_widget.get(1.0, tk.END).strip())
            
            variable.trace('w', update_text)
            text_widget.bind('<KeyRelease>', text_changed)
            update_text()

    def create_image_field(self, parent, label_text, image_var, name_var):
        """Erstellt ein Bildauswahlfeld"""
        field_frame = tk.Frame(parent, bg=COLORS['background_main'])
        field_frame.pack(fill="x", pady=(0, LAYOUT['padding_medium']))
        
        label = tk.Label(
            field_frame,
            text=label_text,
            font=FONTS['body_large'],
            fg=COLORS['text_primary'],
            bg=COLORS['background_main']
        )
        label.pack(anchor="w", pady=(0, LAYOUT['padding_small']))
        
        # Bildinfo und Auswahl
        image_frame = tk.Frame(field_frame, bg=COLORS['background_main'])
        image_frame.pack(fill="x")
        
        current_image = os.path.basename(image_var.get()) if image_var.get() else "Kein Bild ausgewählt"
        image_label = tk.Label(
            image_frame,
            text=current_image,
            font=FONTS['body_medium'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background_hover'],
            relief='flat',
            bd=1,
            padx=LAYOUT['padding_medium'],
            pady=LAYOUT['padding_small']
        )
        image_label.pack(fill="x", pady=(0, LAYOUT['padding_small']))
        
        def select_image():
            file_path = filedialog.askopenfilename(
                title="Produktbild auswählen",
                filetypes=[("PNG Dateien", "*.png"), ("JPG Dateien", "*.jpg"), ("Alle Bilder", "*.png;*.jpg;*.jpeg")]
            )
            if file_path:
                try:
                    filename = f"{name_var.get().strip().replace(' ', '_')}.png" if name_var.get().strip() else f"produkt_{len(get_all_products()) + 1}.png"
                    assets_path = os.path.join("assets", filename)
                    shutil.copy2(file_path, assets_path)
                    image_var.set(assets_path)
                    image_label.config(text=filename)
                except Exception as e:
                    messagebox.showerror("Fehler", f"Bild konnte nicht kopiert werden: {str(e)}")
        
        select_btn = create_modern_button(
            image_frame,
            "Bild auswählen",
            style='secondary',
            command=select_image
        )
        select_btn.pack()

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
