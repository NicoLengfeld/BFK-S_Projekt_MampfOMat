CREATE DATABASE IF NOT EXISTS Mampf;
USE Mampf;


CREATE TABLE IF NOT EXISTS produkte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    preis DECIMAL(6,2) NOT NULL,
    beschreibung TEXT
);


CREATE TABLE IF NOT EXISTS bestellungen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datum DATETIME DEFAULT CURRENT_TIMESTAMP,
    kunde_name VARCHAR(100),
    gesamtpreis DECIMAL(8,2)
);


CREATE TABLE IF NOT EXISTS bestellpositionen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bestellung_id INT NOT NULL,
    produkt_id INT NOT NULL,
    menge INT DEFAULT 1,
    einzelpreis DECIMAL(6,2),
    FOREIGN KEY (bestellung_id) REFERENCES bestellungen(id) ON DELETE CASCADE,
    FOREIGN KEY (produkt_id) REFERENCES produkte(id)
);


INSERT INTO produkte (name, preis, beschreibung) VALUES
('Croissant', 2.20, 'Zartblättriges Buttercroissant, goldbraun gebacken und herrlich buttrig im Geschmack.'),
('Brezel', 1.50, 'Frisch gebackene, knusprige Brezel.'),
('Muffin', 2.50, 'Saftiger Muffin mit zarter Krume, frisch gebacken und leicht süß im Geschmack.'),
('Berliner', 2.20, 'Klassischer Berliner mit feiner Marmeladenfüllung und Puderzucker bestäubt.'),
('Brötchen', 0.80, 'Knuspriges Weizenbrötchen, goldbraun gebacken – perfekt zum Frühstück.'),
('Käsebrötchen', 1.50, 'Frisches Brötchen mit herzhafter Käsekruste, warm ein echter Genuss.');
