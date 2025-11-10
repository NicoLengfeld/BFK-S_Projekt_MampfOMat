"""
Zentrale Produktdatenbank für den Bäckerautomaten
Hier werden alle Produktinformationen verwaltet
"""

# Gemeinsame Produktliste für alle Seiten
PRODUCTS = [
    {
        "id": 1, 
        "name": "Brezel", 
        "price": 1.50, 
        "description": "Frisch gebackene Brezel.", 
        "image": "assets/Brezel.png"
    },
    {
        "id": 2, 
        "name": "Croissant", 
        "price": 2.20, 
        "description": "Zartblättriges Buttercroissant.", 
        "image": "assets/Croissant.png"
    },
    {
        "id": 3, 
        "name": "Brötchen", 
        "price": 1.00, 
        "description": "Klassisches Weizenbrötchen.", 
        "image": "assets/Broetchen.png"
    },
    {
        "id": 4, 
        "name": "Käsebrötchen", 
        "price": 1.80, 
        "description": "Brötchen mit Käse überbacken.", 
        "image": "assets/Kaesebroetchen.png"
    },
    {
        "id": 5, 
        "name": "Muffin", 
        "price": 2.50, 
        "description": "Saftiger Muffin.", 
        "image": "assets/Muffin.png"
    },
    {
        "id": 6, 
        "name": "Berliner", 
        "price": 1.90, 
        "description": "Gefüllter Berliner mit Marmelade.", 
        "image": "assets/Berliner.png"
    },
]

def get_all_products():
    """Gibt alle verfügbaren Produkte zurück"""
    return PRODUCTS

def add_product(name, price, description, image_path):
    """Fügt ein neues Produkt zur Liste hinzu"""
    new_id = max([p["id"] for p in PRODUCTS], default=0) + 1
    new_product = {
        "id": new_id,
        "name": name,
        "price": float(price),
        "description": description,
        "image": image_path
    }
    PRODUCTS.append(new_product)
    return new_product

def update_product(product_id, name, price, description, image_path=None):
    """Aktualisiert ein bestehendes Produkt"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            product["name"] = name
            product["price"] = float(price)
            product["description"] = description
            if image_path:
                product["image"] = image_path
            return product
    return None

def delete_product(product_id):
    """Löscht ein Produkt aus der Liste"""
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p["id"] != product_id]

def get_product_by_id(product_id):
    """Gibt ein spezifisches Produkt zurück"""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None