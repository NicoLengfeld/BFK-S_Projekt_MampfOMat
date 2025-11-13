import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Mampf"
)


cursor = conn.cursor()
print("Verbindung zur Datenbank erfolgreich!")


def get_produkte():
    cursor.execute("SELECT * FROM produkte")
    produkte = cursor.fetchall()
    print("\n--- Produkte ---")
    for p in produkte:
        print(f"ID: {p[0]}, Name: {p[1]}, Preis: {p[2]}€, Beschreibung: {p[3]}")
    return produkte


def create_bestellung(kunde_name, warenkorb):
    """
    warenkorb = [
        {"produkt_id": 1, "menge": 2},
        {"produkt_id": 3, "menge": 1},
    ]
    """
    gesamtpreis = 0

   
    for item in warenkorb:
        cursor.execute("SELECT preis FROM produkte WHERE id = %s", (item["produkt_id"],))
        preis = cursor.fetchone()[0]
        gesamtpreis += preis * item["menge"]

    
    cursor.execute(
        "INSERT INTO bestellungen (kunde_name, gesamtpreis) VALUES (%s, %s)",
        (kunde_name, gesamtpreis)
    )
    conn.commit()
    bestellung_id = cursor.lastrowid


    for item in warenkorb:
        cursor.execute("SELECT preis FROM produkte WHERE id = %s", (item["produkt_id"],))
        einzelpreis = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO bestellpositionen (bestellung_id, produkt_id, menge, einzelpreis)
            VALUES (%s, %s, %s, %s)
        """, (bestellung_id, item["produkt_id"], item["menge"], einzelpreis))
    conn.commit()

    print(f"\n✅ Bestellung {bestellung_id} erfolgreich gespeichert! Gesamtpreis: {gesamtpreis:.2f}€")


if __name__ == "__main__":
    produkte = get_produkte()

    # Beispielbestellung
    warenkorb = [
        {"produkt_id": 1, "menge": 2},
        {"produkt_id": 2, "menge": 1}
    ]
    create_bestellung("Kunde", warenkorb)

cursor.close()
conn.close()
