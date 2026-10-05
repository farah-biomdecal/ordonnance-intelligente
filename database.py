import sqlite3


def creer_base():
    connexion = sqlite3.connect("ordonnance.db")

    curseur = connexion.cursor()

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT UNIQUE NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT
        )
    """)
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ordonnances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_patient TEXT NOT NULL,
        medicament TEXT NOT NULL,
        dosage TEXT,
        posologie TEXT,
        duree TEXT,
        instructions TEXT
    )
""")
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS medecins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            specialite TEXT,
            telephone TEXT,
            etablissement TEXT
        )
    """)
    curseur.execute("""
        PRAGMA table_info(ordonnances)
    """)

    colonnes = [colonne[1] for colonne in curseur.fetchall()]

    if "medecin_id" not in colonnes:
        curseur.execute("""
            ALTER TABLE ordonnances
            ADD COLUMN medecin_id INTEGER
        """)
        curseur.execute("""
        CREATE TABLE IF NOT EXISTS medicaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ordonnance_id INTEGER NOT NULL,
            nom TEXT NOT NULL,
            dosage TEXT,
            posologie TEXT,
            duree TEXT,
            instructions TEXT,
            FOREIGN KEY (ordonnance_id) REFERENCES ordonnances(id)
        )
    """)
    connexion.commit()
    connexion.close()


if __name__ == "__main__":
    creer_base()
    print("Base de données créée avec succès.")
