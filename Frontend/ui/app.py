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
        self.title("MAMPFOMAT")
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
            text="🍰 MAMPF",
            font=FONTS['heading_medium'],
            fg=COLORS['text_light'],
            bg=COLORS['background_dark']
        )
        title_label.pack(side="left")
        
        subtitle_label = tk.Label(
            title_frame,
            text="OMAT",
            font=FONTS['body_large'],
            fg=COLORS['accent_gold'],
            bg=COLORS['background_dark']
        )
        subtitle_label.pack(side="left", padx=(LAYOUT['padding_small'], 0))
        
        # Moderne Status-Info rechts
        status_frame = tk.Frame(header_frame, bg=COLORS['background_dark'])
        status_frame.grid(row=0, column=2, padx=LAYOUT['padding_large'], pady=LAYOUT['padding_medium'])
        
        # Warenkorb-Info mit Icon und Hover-Funktionalität
        self.cart_info_label = tk.Label(
            status_frame,
            text="🛒 Warenkorb: 0 Artikel",
            font=FONTS['body_medium'],
            fg=COLORS['accent_blue'],
            bg=COLORS['background_dark'],
            cursor='hand2'
        )
        self.cart_info_label.pack(side="right")
        
        # Hover-Popup für Warenkorb
        self.cart_popup = None
        self.hover_delay_id = None
        
        # Events für Warenkorb-Hover
        self.cart_info_label.bind("<Enter>", self.schedule_show_cart_popup)
        self.cart_info_label.bind("<Leave>", self.schedule_hide_cart_popup)
        self.cart_info_label.bind("<Button-1>", lambda e: self.show_frame("CartPage"))

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
    
    def schedule_show_cart_popup(self, event):
        """Zeigt das Warenkorb-Popup mit kurzer Verzögerung"""
        if self.hover_delay_id:
            self.after_cancel(self.hover_delay_id)
        self.hover_delay_id = self.after(300, self.show_cart_popup)  # 300ms Verzögerung
    
    def schedule_hide_cart_popup(self, event):
        """Versteckt das Warenkorb-Popup mit Verzögerung"""
        if self.hover_delay_id:
            self.after_cancel(self.hover_delay_id)
        self.hover_delay_id = self.after(200, self.hide_cart_popup)  # 200ms Verzögerung
    
    def show_cart_popup(self):
        """Zeigt das Warenkorb-Hover-Popup"""
        if self.cart_popup:
            self.hide_cart_popup()
        
        # Popup erstellen
        self.cart_popup = tk.Toplevel(self)
        self.cart_popup.overrideredirect(True)  # Keine Fenster-Rahmen
        self.cart_popup.configure(bg=COLORS['background_card'])
        
        # Position relativ zum Warenkorb-Label berechnen
        x = self.cart_info_label.winfo_rootx()
        y = self.cart_info_label.winfo_rooty() + self.cart_info_label.winfo_height() + 5
        
        # Falls zu weit rechts, nach links verschieben
        if x + 300 > self.winfo_screenwidth():
            x = self.winfo_screenwidth() - 320
            
        self.cart_popup.geometry(f"300x400+{x}+{y}")
        
        # Popup-Inhalt
        self.create_cart_popup_content()
        
        # Hover-Events für Popup selbst
        self.cart_popup.bind("<Enter>", self.cancel_hide_popup)
        self.cart_popup.bind("<Leave>", self.schedule_hide_cart_popup)
    
    def cancel_hide_popup(self, event):
        """Bricht das Verstecken des Popups ab"""
        if self.hover_delay_id:
            self.after_cancel(self.hover_delay_id)
            self.hover_delay_id = None
    
    def hide_cart_popup(self):
        """Versteckt das Warenkorb-Popup"""
        if self.cart_popup:
            self.cart_popup.destroy()
            self.cart_popup = None
        if self.hover_delay_id:
            self.after_cancel(self.hover_delay_id)
            self.hover_delay_id = None
    
    def create_cart_popup_content(self):
        """Erstellt den Inhalt des Warenkorb-Popups"""
        # Debug: Warenkorb-Inhalt ausgeben
        print(f"DEBUG: Warenkorb-Inhalt: {self.cart}")
        print(f"DEBUG: Anzahl Artikel: {sum(self.cart.values()) if self.cart else 0}")
        
        # Header
        header_frame = tk.Frame(self.cart_popup, bg=COLORS['primary_dark'], height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🛒 Warenkorb",
            font=FONTS['heading_small'],
            fg=COLORS['text_light'],
            bg=COLORS['primary_dark']
        )
        title_label.pack(pady=10)
        
        # Content-Frame mit Scrolling
        content_frame = tk.Frame(self.cart_popup, bg=COLORS['background_card'])
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not self.cart or sum(self.cart.values()) == 0:
            # Leerer Warenkorb
            empty_label = tk.Label(
                content_frame,
                text="Warenkorb ist leer\n\n🛍️ Fügen Sie Produkte hinzu!",
                font=FONTS['body_medium'],
                fg=COLORS['text_secondary'],
                bg=COLORS['background_card'],
                justify='center'
            )
            empty_label.pack(expand=True)
            print("DEBUG: Zeige leeren Warenkorb")
        else:
            # Warenkorb-Inhalt anzeigen
            from ui.product_data import get_product_by_name
            print("DEBUG: Lade Warenkorb-Inhalt...")
            
            total_price = 0.0
            row = 0
            
            for product_name, quantity in self.cart.items():
                print(f"DEBUG: Lade Produkt '{product_name}' mit Menge {quantity}")
                product = get_product_by_name(product_name)
                
                if product:
                    print(f"DEBUG: Produkt gefunden: {product}")
                    # Produkt-Frame
                    item_frame = tk.Frame(content_frame, bg=COLORS['background_hover'], relief='raised', bd=1)
                    item_frame.pack(fill="x", pady=5, padx=5)
                    item_frame.pack_propagate(False)
                    item_frame.configure(height=70)
                    
                    # Produktinfo
                    info_frame = tk.Frame(item_frame, bg=COLORS['background_hover'])
                    info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
                    
                    name_label = tk.Label(
                        info_frame,
                        text=product['name'],
                        font=FONTS['body_medium'],
                        fg=COLORS['text_primary'],
                        bg=COLORS['background_hover'],
                        anchor='w'
                    )
                    name_label.pack(anchor="w", fill="x")
                    
                    # Menge und Preis
                    if 'price' in product:
                        item_price = product['price'] * quantity
                        total_price += item_price
                        
                        price_text = f"{quantity}x à {product['price']:.2f}€ = {item_price:.2f}€"
                        price_label = tk.Label(
                            info_frame,
                            text=price_text,
                            font=FONTS['caption'],
                            fg=COLORS['button_success'],
                            bg=COLORS['background_hover'],
                            anchor='w'
                        )
                        price_label.pack(anchor="w", fill="x")
                    
                    row += 1
                else:
                    print(f"DEBUG: Produkt '{product_name}' nicht gefunden!")
            
            print(f"DEBUG: Gesamtpreis: {total_price}€, Anzahl Artikel: {row}")
            
            # Gesamtsumme
            if total_price > 0:
                total_frame = tk.Frame(content_frame, bg=COLORS['primary_dark'], height=45)
                total_frame.pack(fill="x", pady=(15, 0))
                total_frame.pack_propagate(False)
                
                total_label = tk.Label(
                    total_frame,
                    text=f"Gesamt: {total_price:.2f}€",
                    font=FONTS['heading_small'],
                    fg=COLORS['accent_gold'],
                    bg=COLORS['primary_dark']
                )
                total_label.pack(pady=12)
        
        # Footer mit Buttons
        footer_frame = tk.Frame(self.cart_popup, bg=COLORS['background_card'])
        footer_frame.pack(fill="x", padx=10, pady=5)
        
        view_cart_btn = tk.Button(
            footer_frame,
            text="Warenkorb öffnen",
            font=FONTS['button_small'],
            bg=COLORS['button_gold'],
            fg=COLORS['primary_dark'],
            relief='raised',
            bd=1,
            padx=20,
            pady=5,
            cursor='hand2',
            command=lambda: [self.hide_cart_popup(), self.show_frame("CartPage")]
        )
        view_cart_btn.pack(side="right")
    
    def clear_cart(self):
        """Leert den Warenkorb nach einer Bestellung"""
        self.cart = {}
        self.update_cart_info()
        print("Warenkorb wurde geleert!")  # Debug-Output
