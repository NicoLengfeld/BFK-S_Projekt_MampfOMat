import tkinter as tk
from ui.home_page import HomePage
from ui.product_page import ProductPage
from ui.cart_page import CartPage
from ui.thankyou_page import ThankYouPage
from ui.admin_page import AdminPage
from ui.modern_styles import COLORS, FONTS, LAYOUT

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.cart = {}  # speichert Produkte & Mengen
        self.setup_ui()

    def setup_window(self):
        """Konfiguriert das Hauptfenster mit modernem Premium-Design"""
        self.title("BÄCKEREI AUTOMAT")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Eleganter weißer Hintergrund mit dezenten Akzenten
        self.configure(bg='#f8f9fa')  # Sehr helles, warmes Grau
        
        # Zentriere das Fenster auf dem Bildschirm
        self.center_window()
        
        # Responsive Grid konfigurieren
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def center_window(self):
        """Zentriert das Fenster auf dem Bildschirm"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Erstellt die moderne Benutzeroberfläche"""
        # Header mit Premium-Design
        self.create_header()
        
        # Hauptcontainer für Seiten - eleganter weißer Look
        self.container = tk.Frame(
            self, 
            bg='#ffffff',  # Reines Weiß
            relief='flat',
            bd=0
        )
        self.container.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)  # Weniger Padding
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Seiten initialisieren
        self.frames = {}
        for F in (HomePage, ProductPage, CartPage, ThankYouPage, AdminPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame("HomePage")

    def create_header(self):
        """Erstellt den modernen Header"""
        header_frame = tk.Frame(
            self,
            bg=COLORS['background_dark'],
            height=80,
            relief='flat',
            bd=0
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo/Titel links mit Gradient-Effekt
        title_frame = tk.Frame(header_frame, bg=COLORS['background_dark'])
        title_frame.grid(row=0, column=0, padx=LAYOUT['padding_large'], pady=LAYOUT['padding_medium'])
        
        title_label = tk.Label(
            title_frame,
            text="🥐 BÄCKEREI",
            font=FONTS['heading_medium'],
            fg=COLORS['text_light'],
            bg=COLORS['background_dark']
        )
        title_label.pack(side="left")
        
        subtitle_label = tk.Label(
            title_frame,
            text="AUTOMAT",
            font=FONTS['body_large'],
            fg=COLORS['accent_gold'],
            bg=COLORS['background_dark']
        )
        subtitle_label.pack(side="left", padx=(LAYOUT['padding_small'], 0))
        
        # Moderne Status-Info rechts
        status_frame = tk.Frame(header_frame, bg=COLORS['background_dark'])
        status_frame.grid(row=0, column=2, padx=LAYOUT['padding_large'], pady=LAYOUT['padding_medium'])
        
        # Warenkorb-Info mit Icon
        self.cart_info_label = tk.Label(
            status_frame,
            text="🛒 Warenkorb: 0 Artikel",
            font=FONTS['body_medium'],
            fg=COLORS['accent_blue'],
            bg=COLORS['background_dark']
        )
        self.cart_info_label.pack(side="right")

    def show_frame(self, page_name, **kwargs):
        """Zeigt eine Seite an mit sanften Übergängen"""
        frame = self.frames[page_name]
        if hasattr(frame, "update_page"):
            frame.update_page(**kwargs)
        frame.tkraise()
        
        # Warenkorb-Info aktualisieren
        self.update_cart_info()

    def update_cart_info(self):
        """Aktualisiert die Warenkorb-Information im Header"""
        total_items = sum(self.cart.values()) if self.cart else 0
        if total_items == 0:
            cart_text = "🛒 Warenkorb: leer"
            cart_color = COLORS['text_secondary']
        elif total_items == 1:
            cart_text = "🛒 Warenkorb: 1 Artikel"
            cart_color = COLORS['accent_gold']
        else:
            cart_text = f"🛒 Warenkorb: {total_items} Artikel"
            cart_color = COLORS['button_success']
        
        if hasattr(self, 'cart_info_label'):
            self.cart_info_label.configure(text=cart_text, fg=cart_color)
    
    def clear_cart(self):
        """Leert den Warenkorb nach einer Bestellung"""
        self.cart = {}
        self.update_cart_info()
        print("Warenkorb wurde geleert!")  # Debug-Output
