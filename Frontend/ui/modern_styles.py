"""
Moderne UI-Stile für den Bäckerautomaten
Inspiriert von Premium-Automarken wie Mercedes-Benz
"""

import tkinter as tk

# Farbpalette - Schwarz-Weiß-Gelb Design
COLORS = {
    # Hauptfarben
    'primary_dark': '#000000',      # Reines Schwarz
    'primary_light': '#ffffff',     # Reines Weiß
    'accent_silver': '#f5f5f5',     # Hellgrau
    'accent_gold': '#ffd700',       # Lebendiges Gelb/Gold
    'accent_blue': '#ffd700',       # Gelb statt Blau
    
    # UI-Farben
    'background_main': '#ffffff',   # Weißer Haupthintergrund
    'background_card': '#ffffff',   # Weiße Card-Hintergründe
    'background_hover': '#fff8dc',  # Helles Gelb für Hover (cornsilk)
    'background_dark': '#000000',   # Schwarze Bereiche (Header)
    
    # Text-Farben
    'text_primary': '#000000',      # Schwarzer Haupttext
    'text_secondary': '#555555',    # Dunkelgrauer Sekundärtext
    'text_light': '#ffffff',        # Weißer Text (auf schwarzem Hintergrund)
    'text_accent': '#ffd700',       # Gelber Akzenttext
    
    # Button-Farben
    'button_primary': '#ffd700',    # Gelber Button
    'button_primary_hover': '#ffcc00',  # Dunkleres Gelb für Hover
    'button_secondary': '#f5f5f5',  # Hellgrauer Sekundär-Button
    'button_success': '#ffd700',    # Gelber Erfolg-Button
    'button_danger': '#ff6b6b',     # Sanftes Rot für Gefahr-Button
    
    # Rahmen
    'border_light': '#e0e0e0',      # Helle graue Rahmen
    'border_medium': '#cccccc',     # Mittlere graue Rahmen
    'shadow': '#000000',            # Schwarzer Schatten
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

# Button-Stile
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['button_primary'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 20,
        'pady': 10,
        'cursor': 'hand2'
    },
    'secondary': {
        'bg': COLORS['button_secondary'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 20,
        'pady': 10,
        'cursor': 'hand2'
    },
    'success': {
        'bg': COLORS['button_success'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 20,
        'pady': 10,
        'cursor': 'hand2'
    },
    'danger': {
        'bg': COLORS['button_danger'],
        'fg': COLORS['text_light'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 20,
        'pady': 10,
        'cursor': 'hand2'
    },
    'card': {
        'bg': COLORS['background_card'],
        'fg': COLORS['text_primary'],
        'font': FONTS['body_medium'],
        'relief': 'flat',
        'bd': 1,
        'highlightthickness': 0,
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