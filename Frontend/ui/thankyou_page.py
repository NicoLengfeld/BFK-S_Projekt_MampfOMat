import tkinter as tk
from ui.modern_styles import COLORS, FONTS, LAYOUT, create_modern_button

class ThankYouPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['background_main'])
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Erstellt die moderne Danke-Seite"""
        # Hauptcontainer
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Zentrierter Container
        center_frame = tk.Frame(self, bg=COLORS['background_main'])
        center_frame.grid(row=0, column=0)
        
        # Großes Erfolgs-Icon
        icon_label = tk.Label(
            center_frame,
            text="✅",
            font=('Segoe UI', 72, 'normal'),
            fg=COLORS['button_success'],
            bg=COLORS['background_main']
        )
        icon_label.pack(pady=(LAYOUT['padding_xlarge'], LAYOUT['padding_medium']))
        
        # Haupttitel
        title_label = tk.Label(
            center_frame,
            text="Vielen Dank für Ihre Bestellung!",
            font=FONTS['heading_large'],
            fg=COLORS['text_primary'],
            bg=COLORS['background_main']
        )
        title_label.pack(pady=(0, LAYOUT['padding_medium']))
        
        # Untertitel
        subtitle_label = tk.Label(
            center_frame,
            text="Ihre frischen Backwaren werden gerade zubereitet.",
            font=FONTS['body_large'],
            fg=COLORS['text_secondary'],
            bg=COLORS['background_main']
        )
        subtitle_label.pack(pady=(0, LAYOUT['padding_large']))
        
        # Wartungshinweis
        info_label = tk.Label(
            center_frame,
            text="Bitte warten Sie einen Moment...",
            font=FONTS['body_medium'],
            fg=COLORS['text_accent'],
            bg=COLORS['background_main']
        )
        info_label.pack(pady=(0, LAYOUT['padding_xlarge']))
        
        # Zurück-Button
        back_btn = create_modern_button(
            center_frame,
            "Neue Bestellung starten",
            style='primary',
            command=self.start_new_order
        )
        back_btn.pack(pady=LAYOUT['padding_medium'])
    
    def start_new_order(self):
        """Startet eine neue Bestellung (leert Warenkorb)"""
        # Warenkorb leeren
        if hasattr(self.controller, 'clear_cart'):
            self.controller.clear_cart()
        
        # Zur Homepage zurückkehren
        self.controller.show_frame("HomePage")
    
    def update_page(self, **kwargs):
        """Wird aufgerufen wenn die Seite angezeigt wird"""
        # Automatisches Leeren des Warenkorbs bei Bestellabschluss
        if hasattr(self.controller, 'clear_cart'):
            self.controller.clear_cart()
