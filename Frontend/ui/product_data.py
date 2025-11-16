"""
Zentrale Produktdatenbank für den MampfOMat
Jetzt DB-gestützt (ruft die MySQL-Tabelle `produkte` ab)
"""

import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import db  

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

def _row_to_product(row):
    """Konvertiert ein DB-Tupel (id, name, preis, beschreibung) zu einem Dict"""
    if row is None:
        return None
    prod_id, name, preis, beschreibung = row[0], row[1], row[2], row[3]
   
    image_candidate = os.path.join(os.path.dirname(__file__), "..", "assets", f"{name}.png")
    if os.path.exists(image_candidate):
        image_path = image_candidate
    else:
        image_path = os.path.join("assets", f"{name}.png") 
    return {
        "id": prod_id,
        "name": name,
        "price": float(preis),
        "description": beschreibung if beschreibung is not None else "",
        "image": image_path
    }

def get_all_products():
    """Liefert eine Liste von Produkt-Dicts aus der DB."""
    rows = db.get_produkte() 
    products = []
    for r in rows:
        products.append(_row_to_product(r))
    return products

def add_product(name, price, description, image_path=None):
    """
    Fügt ein Produkt in die DB ein und gibt das neue Produkt-Dict zurück.
    image_path wird nur als UI-Feld verwendet (Datei muss bereits im assets liegen).
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produkte (name, preis, beschreibung) VALUES (%s, %s, %s)",
        (name, price, description)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()

    
    image_candidate = image_path if image_path else os.path.join("assets", f"{name}.png")
    return {
        "id": new_id,
        "name": name,
        "price": float(price),
        "description": description,
        "image": image_candidate
    }

def update_product(product_id, name, price, description, image_path=None):
    """Aktualisiert Produktdaten in der DB und gibt das aktualisierte Dict zurück."""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produkte SET name=%s, preis=%s, beschreibung=%s WHERE id=%s",
        (name, price, description, product_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    image_candidate = image_path if image_path else os.path.join("assets", f"{name}.png")
    return {
        "id": product_id,
        "name": name,
        "price": float(price),
        "description": description,
        "image": image_candidate
    }

def delete_product(product_id):
    """Löscht ein Produkt aus der DB."""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produkte WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_product_by_id(product_id):
    """Gibt ein Produkt-Dict anhand der Produkt-ID zurück."""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produkte WHERE id = %s", (product_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return _row_to_product(row)

def get_product_by_name(product_name):
    """Gibt ein Produkt-Dict anhand des Namens zurück (erster Treffer)."""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produkte WHERE name = %s", (product_name,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return _row_to_product(row)
