"""
Moderne UI-Stile für den Bäckerautomaten
Inspiriert von Premium-Automarken wie Mercedes-Benz
"""

import tkinter as tk

# Farbpalette - Premium Mercedes-inspiriertes Design
COLORS = {
    # Hauptfarben
    'primary_dark': '#1a1a1a',      # Elegantes Anthrazit
    'primary_light': '#f8f9fa',     # Warmes Off-White
    'accent_silver': '#c4c7cc',     # Mercedes-Silber
    'accent_gold': '#d4af37',       # Edles Gold
    'accent_blue': '#0078d4',       # Premium Blau
    
    # UI-Farben - Elegantes Weiß mit Premium-Akzenten
    'background_main': '#ffffff',   # Reines Weiß
    'background_card': '#ffffff',   # Weiße Cards
    'background_hover': '#f8f9fa',  # Sehr helles Grau beim Hover
    'background_dark': '#1a1a1a',   # Schwarzer Header
    'background_sidebar': '#f5f6fa', # Helle Seitenbereiche
    'background_premium': '#f8f9fa', # Premium helles Grau
    
    # Text-Farben
    'text_primary': '#212529',      # Dunkler, lesbarer Text
    'text_secondary': '#6c757d',    # Mittlerer Grauton
    'text_light': '#ffffff',        # Weißer Text
    'text_accent': '#d4af37',       # Gold-Akzent
    
    # Button-Farben - Deutlich sichtbar
    'button_primary': '#0078d4',    # Kräftiges Blau
    'button_primary_hover': '#106ebe', # Dunkleres Blau
    'button_secondary': '#6c757d',  # Grauer Button
    'button_secondary_hover': '#5a6268', # Dunkler grau
    'button_success': '#28a745',    # Grüner Erfolg-Button
    'button_success_hover': '#218838', # Dunkler grün
    'button_danger': '#dc3545',     # Roter Gefahr-Button
    'button_danger_hover': '#c82333', # Dunkler rot
    'button_gold': '#d4af37',       # Gold-Button für besondere Aktionen
    'button_gold_hover': '#b8941f',  # Dunkler gold
    
    # Rahmen und Schatten
    'border_light': '#dee2e6',      # Helle Rahmen
    'border_medium': '#adb5bd',     # Mittlere Rahmen
    'shadow': 'rgba(0,0,0,0.15)',   # Weicher Schatten
    'shadow_strong': 'rgba(0,0,0,0.25)', # Starker Schatten
}

# Schriftarten (Premium-Look)
FONTS = {
    'heading_large': ('Segoe UI', 32, 'normal'),     # Große Überschrift
    'heading_medium': ('Segoe UI', 24, 'normal'),    # Mittlere Überschrift
    'heading_small': ('Segoe UI', 18, 'bold'),       # Kleine Überschrift
    'body_large': ('Segoe UI', 14, 'normal'),        # Großer Body-Text
    'body_medium': ('Segoe UI', 12, 'normal'),       # Mittlerer Body-Text
    'body_small': ('Segoe UI', 10, 'normal'),        # Kleiner Body-Text
    'button': ('Segoe UI', 11, 'bold'),              # Button-Text
    'caption': ('Segoe UI', 9, 'normal'),            # Caption-Text
}

# Layout-Konstanten
LAYOUT = {
    'padding_small': 8,
    'padding_medium': 16,
    'padding_large': 24,
    'padding_xlarge': 32,
    'radius_small': 4,
    'radius_medium': 8,
    'radius_large': 12,
    'shadow_offset': 2,
}

# Button-Stile - Premium Look mit besserer Sichtbarkeit
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['button_primary'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'padx': 25,
        'pady': 12,
        'cursor': 'hand2',
        'activebackground': COLORS['button_primary_hover'],
        'activeforeground': COLORS['text_light']
    },
    'secondary': {
        'bg': COLORS['button_secondary'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'padx': 25,
        'pady': 12,
        'cursor': 'hand2',
        'activebackground': COLORS['button_secondary_hover'],
        'activeforeground': COLORS['text_light']
    },
    'success': {
        'bg': COLORS['button_success'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'padx': 25,
        'pady': 12,
        'cursor': 'hand2',
        'activebackground': COLORS['button_success_hover'],
        'activeforeground': COLORS['text_light']
    },
    'danger': {
        'bg': COLORS['button_danger'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'padx': 25,
        'pady': 12,
        'cursor': 'hand2',
        'activebackground': COLORS['button_danger_hover'],
        'activeforeground': COLORS['text_light']
    },
    'gold': {
        'bg': COLORS['button_gold'],
        'fg': COLORS['primary_dark'],
        'font': FONTS['button'],
        'relief': 'raised',
        'bd': 2,
        'padx': 25,
        'pady': 12,
        'cursor': 'hand2',
        'activebackground': COLORS['button_gold_hover'],
        'activeforeground': COLORS['text_light']
    },
    'card': {
        'bg': COLORS['background_card'],
        'fg': COLORS['text_primary'],
        'font': FONTS['body_medium'],
        'relief': 'raised',
        'bd': 2,
        'highlightthickness': 1,
        'highlightbackground': COLORS['border_light'],
        'cursor': 'hand2'
    }
}

# Card-Stile
CARD_STYLES = {
    'product': {
        'bg': COLORS['background_card'],
        'relief': 'flat',
        'bd': 0,
        'padx': LAYOUT['padding_medium'],
        'pady': LAYOUT['padding_medium'],
        'highlightthickness': 1,
        'highlightcolor': COLORS['border_light'],
        'highlightbackground': COLORS['border_light']
    },
    'elevated': {
        'bg': COLORS['background_card'],
        'relief': 'raised',
        'bd': 1,
        'padx': LAYOUT['padding_large'],
        'pady': LAYOUT['padding_large']
    }
}

def create_gradient_frame(parent, color1, color2, width, height):
    """Erstellt ein Frame mit Gradient-Effekt (Simulation)"""
    frame = tk.Frame(parent, width=width, height=height)
    frame.configure(bg=color1)
    return frame

def apply_hover_effect(widget, hover_bg, normal_bg):
    """Fügt Hover-Effekt zu einem Widget hinzu"""
    def on_enter(event):
        widget.configure(bg=hover_bg)
    
    def on_leave(event):
        widget.configure(bg=normal_bg)
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def create_modern_button(parent, text, style='primary', command=None):
    """Erstellt einen modernen Button mit Stil"""
    if style not in BUTTON_STYLES:
        style = 'primary'
    
    btn_style = BUTTON_STYLES[style].copy()
    if command:
        btn_style['command'] = command
    
    button = tk.Button(parent, text=text, **btn_style)
    
    # Hover-Effekt hinzufügen
    normal_bg = btn_style['bg']
    if style == 'primary':
        hover_bg = COLORS['button_primary_hover']
    else:
        # Dunklere Version der ursprünglichen Farbe für Hover
        hover_bg = normal_bg
    
    apply_hover_effect(button, hover_bg, normal_bg)
    
    return button

def create_modern_card(parent, **kwargs):
    """Erstellt eine moderne Card"""
    card_style = CARD_STYLES['product'].copy()
    card_style.update(kwargs)
    
    card = tk.Frame(parent, **card_style)
    return card