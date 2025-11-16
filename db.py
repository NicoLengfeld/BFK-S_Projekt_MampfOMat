import mysql.connector
from decimal import Decimal

# Funktion zum Aufbau der Verbindung
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Mampf"
    )

# Produkte abrufen
def get_produkte():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, preis, beschreibung FROM produkte")
    produkte = cursor.fetchall()
    cursor.close()
    conn.close()
    return produkte

# Preis eines Produkts anhand der ID holen
def get_preis_von_produkt(produkt_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT preis FROM produkte WHERE id = %s", (produkt_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return Decimal(result[0])
    else:
        return Decimal(0)

# Bestellung speichern
def add_bestellung(produkte_mit_menge, gesamtpreis):
    conn = get_connection()
    cursor = conn.cursor()

    # Bestellung speichern
    cursor.execute("INSERT INTO bestellungen (gesamtpreis) VALUES (%s)", (gesamtpreis,))
    bestell_id = cursor.lastrowid

    # Einzelne Produkte speichern
    for produkt_id, menge in produkte_mit_menge.items():
        preis = get_preis_von_produkt(produkt_id)
        cursor.execute("""
            INSERT INTO bestellpositionen (bestellung_id, produkt_id, menge, einzelpreis)
            VALUES (%s, %s, %s, %s)
        """, (bestell_id, produkt_id, menge, preis))

    conn.commit()
    cursor.close()
    conn.close()

# Alle Bestellungen abrufen
def get_bestellungen():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.id AS bestell_id, p.name, bp.menge, b.gesamtpreis
        FROM bestellungen b
        JOIN bestellpositionen bp ON b.id = bp.bestellung_id
        JOIN produkte p ON bp.produkt_id = p.id
    """)
    daten = cursor.fetchall()
    cursor.close()
    conn.close()
    return daten

# Testausgabe (nur beim direkten Start)
if __name__ == "__main__":
    print("Verbindung zur Datenbank erfolgreich!")
    produkte = get_produkte()
    for p in produkte:
        print(f"ID: {p[0]}, Name: {p[1]}, Preis: {p[2]}€, Beschreibung: {p[3]}")
