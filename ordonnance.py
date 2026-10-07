from flask import Flask, request, redirect
import sqlite3
import qrcode
import io
import base64

from database import creer_base
app = Flask(__name__)
creer_base()

@app.route("/")
def accueil():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ordonnance médicale intelligente</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7f9;
                text-align: center;
            }

            .header {
                background: #1976d2;
                color: white;
                padding: 30px;
            }

            .header h1 {
                margin: 0;
                font-size: 32px;
            }

            .container {
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
            }

            .card {
                background: white;
                padding: 30px;
                margin: 20px 0;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }

            .card h2 {
                color: #1976d2;
            }

            button {
                background: #1976d2;
                color: white;
                border: none;
                padding: 14px 25px;
                margin: 10px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background: #125ca3;
            }

            .footer {
                margin-top: 40px;
                padding: 20px;
                color: #666;
            }
        </style>
    </head>

    <body>

        <div class="header">
            <h1>Ordonnance médicale intelligente</h1>
            <p>Système numérique de gestion des ordonnances médicales</p>
        </div>

        <div class="container">

            <div class="card">
                <h2>👤 Patient</h2>
                <p>Ajouter et gérer les informations du patient.</p>

                <a href="/patient">
                    <button>Ajouter un patient</button>
                </a>
            </div>

            <div class="card">
                <h2>👨‍⚕️ Médecin</h2>
                <p>Informations du médecin prescripteur.</p>
           <a href="/medecin">
    <button>Informations du médecin</button>
</a>
            </div>

            <div class="card">
                <h2>💊 Ordonnance</h2>
                <p>Créer une nouvelle ordonnance médicale.</p>
                <a href="/ordonnance">
    <button>Créer une ordonnance</button>
</a>
            </div>

            <div class="card">
                <h2>🔳 QR Code</h2>
                <p>Accéder rapidement à l'ordonnance numérique.</p>
                <a href="/voir_qr">
             <button>Voir le QR Code</button>
            </a>
            </div>

        </div>

        <div class="footer">icale intelligente</p>
        </div>
            <p>Projet universitaire — Ordonnance méd

    </body>
    </html>
    """
@app.route("/patient", methods=["GET", "POST"])
def patient():

    message = ""

    if request.method == "POST":

        numero = request.form["numero"]
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        date_naissance = request.form["date_naissance"]

        connexion = sqlite3.connect("ordonnance.db")
        curseur = connexion.cursor()

        try:
            curseur.execute("""
                INSERT INTO patients
                (numero, nom, prenom, date_naissance)
                VALUES (?, ?, ?, ?)
            """, (numero, nom, prenom, date_naissance))

            connexion.commit()
            message = "Patient enregistré avec succès ✅"

        except sqlite3.IntegrityError:
            message = "Ce numéro de patient existe déjà."

        connexion.close()

    return """
    <!DOCTYPE html>
    <html lang="fr">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Ajouter un patient</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7f9;
            }

            .container {
                max-width: 600px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
                color: #1976d2;
            }

            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 5px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 12px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 7px;
            }

            button {
                width: 100%;
                margin-top: 25px;
                padding: 14px;
                background: #1976d2;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }

            .message {
                text-align: center;
                margin-top: 15px;
                color: green;
                font-weight: bold;
            }

            .retour {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #1976d2;
                text-decoration: none;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>Ajouter un patient</h1>

            <form method="POST">

                <label>Numéro du patient</label>
                <input type="text" name="numero" required>

                <label>Nom</label>
                <input type="text" name="nom" required>

                <label>Prénom</label>
                <input type="text" name="prenom" required>

                <label>Date de naissance</label>
                <input type="date" name="date_naissance">

                <button type="submit">
                    Enregistrer le patient
                </button>

            </form>

            <p class="message">""" + message + """</p>

            <a class="retour" href="/">
                ← Retour à l'accueil
            </a>

        </div>

    </body>

    </html>
    """
@app.route("/ordonnance", methods=["GET", "POST"])
def ordonnance():

    message = ""

    connexion = sqlite3.connect("ordonnance.db")
    curseur = connexion.cursor()

    # Récupérer les patients
    curseur.execute("""
        SELECT numero, nom, prenom
        FROM patients
        ORDER BY nom
    """)
    patients = curseur.fetchall()

    # Récupérer les médecins
    curseur.execute("""
        SELECT id, nom, specialite
        FROM medecins
        ORDER BY nom
    """)
    medecins = curseur.fetchall()

    if request.method == "POST":

        numero_patient = request.form["numero_patient"]
        medecin_id = request.form["medecin_id"]

        noms = request.form.getlist("medicament")
        dosages = request.form.getlist("dosage")
        posologies = request.form.getlist("posologie")
        durees = request.form.getlist("duree")
        instructions_list = request.form.getlist("instructions")

        if len(noms) > 0 and noms[0].strip():

            # Garder le premier médicament dans l'ancienne table
            # pour conserver la compatibilité avec les données existantes.
            premier_nom = noms[0]
            premier_dosage = dosages[0] if len(dosages) > 0 else ""
            premiere_posologie = posologies[0] if len(posologies) > 0 else ""
            premiere_duree = durees[0] if len(durees) > 0 else ""
            premieres_instructions = (
                instructions_list[0]
                if len(instructions_list) > 0 else ""
            )

            curseur.execute("""
                INSERT INTO ordonnances
                (
                    numero_patient,
                    medecin_id,
                    medicament,
                    dosage,
                    posologie,
                    duree,
                    instructions
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                numero_patient,
                medecin_id,
                premier_nom,
                premier_dosage,
                premiere_posologie,
                premiere_duree,
                premieres_instructions
            ))

            ordonnance_id = curseur.lastrowid

            # Ajouter tous les médicaments dans la nouvelle table
            for i in range(len(noms)):

                if noms[i].strip():

                    dosage = dosages[i] if i < len(dosages) else ""
                    posologie = posologies[i] if i < len(posologies) else ""
                    duree = durees[i] if i < len(durees) else ""
                    instructions = (
                        instructions_list[i]
                        if i < len(instructions_list) else ""
                    )

                    curseur.execute("""
                        INSERT INTO medicaments
                        (
                            ordonnance_id,
                            nom,
                            dosage,
                            posologie,
                            duree,
                            instructions
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        ordonnance_id,
                        noms[i],
                        dosage,
                        posologie,
                        duree,
                        instructions
                    ))

            connexion.commit()

            message = "Ordonnance enregistrée avec succès ✅"

    connexion.close()

    options_patients = ""

    for patient in patients:
        options_patients += f"""
        <option value="{patient[0]}">
            {patient[0]} - {patient[1]} {patient[2]}
        </option>
        """

    options_medecins = ""

    for medecin in medecins:
        options_medecins += f"""
        <option value="{medecin[0]}">
            Dr {medecin[1]} - {medecin[2]}
        </option>
        """

    return """
    <!DOCTYPE html>
    <html lang="fr">

    <head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Créer une ordonnance</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7f9;
            }

            .container {
                max-width: 700px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
                color: #1976d2;
            }

            h2 {
                color: #1976d2;
                margin-top: 30px;
            }

            .medicament {
                background: #f8fafc;
                padding: 20px;
                margin-top: 15px;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }

            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 5px;
                font-weight: bold;
            }

            input, select, textarea {
                width: 100%;
                padding: 12px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 7px;
            }

            textarea {
                height: 80px;
                resize: vertical;
            }

            .ajouter {
                width: 100%;
                margin-top: 20px;
                padding: 12px;
                background: #4caf50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                cursor: pointer;
            }

            .enregistrer {
                width: 100%;
                margin-top: 25px;
                padding: 14px;
                background: #1976d2;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }

            .message {
                text-align: center;
                margin-top: 15px;
                color: green;
                font-weight: bold;
            }

            .retour {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #1976d2;
                text-decoration: none;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>Créer une ordonnance</h1>

            <form method="POST">

                <label>Patient</label>

                <select name="numero_patient" required>

                    <option value="">
                        -- Sélectionner un patient --
                    </option>

                    """ + options_patients + """

                </select>


                <label>Médecin</label>

                <select name="medecin_id" required>

                    <option value="">
                        -- Sélectionner un médecin --
                    </option>

                    """ + options_medecins + """

                </select>


                <h2>Médicaments</h2>

                <div id="medicaments">

                    <div class="medicament">

                        <label>Nom du médicament</label>
                        <input type="text" name="medicament" required>

                        <label>Dosage</label>
                        <input type="text" name="dosage">

                        <label>Posologie</label>
                        <input type="text" name="posologie">

                        <label>Durée du traitement</label>
                        <input type="text" name="duree">

                        <label>Instructions</label>
                        <textarea name="instructions"></textarea>

                    </div>

                </div>


                <button type="button"
                        class="ajouter"
                        onclick="ajouterMedicament()">

                    ＋ Ajouter un médicament

                </button>


                <button type="submit" class="enregistrer">

                    Enregistrer l'ordonnance

                </button>

            </form>


            <p class="message">""" + message + """</p>


            <a class="retour" href="/">
                ← Retour à l'accueil
            </a>

        </div>


        <script>

            function ajouterMedicament() {

                const container = document.getElementById("medicaments");

                const nouveau = document.createElement("div");

                nouveau.className = "medicament";

                nouveau.innerHTML = `

                    <label>Nom du médicament</label>
                    <input type="text" name="medicament">

                    <label>Dosage</label>
                    <input type="text" name="dosage">

                    <label>Posologie</label>
                    <input type="text" name="posologie">

                    <label>Durée du traitement</label>
                    <input type="text" name="duree">

                    <label>Instructions</label>
                    <textarea name="instructions"></textarea>

                `;

                container.appendChild(nouveau);
            }

        </script>

    </body>

    </html>
    """


@app.route("/medecin", methods=["GET", "POST"])
def medecin():

    message = ""

    if request.method == "POST":

        nom = request.form["nom"]
        specialite = request.form["specialite"]
        telephone = request.form["telephone"]
        etablissement = request.form["etablissement"]

        connexion = sqlite3.connect("ordonnance.db")
        curseur = connexion.cursor()

        curseur.execute("""
            INSERT INTO medecins
            (nom, specialite, telephone, etablissement)
            VALUES (?, ?, ?, ?)
        """, (
            nom,
            specialite,
            telephone,
            etablissement
        ))

        connexion.commit()
        connexion.close()

        message = "Informations du médecin enregistrées avec succès ✅"

    return """
    <!DOCTYPE html>
    <html lang="fr">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Informations du médecin</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7f9;
            }

            .container {
                max-width: 650px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
                color: #1976d2;
            }

            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 5px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 12px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 7px;
            }

            button {
                width: 100%;
                margin-top: 25px;
                padding: 14px;
                background: #1976d2;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }

            .message {
                text-align: center;
                margin-top: 15px;
                color: green;
                font-weight: bold;
            }

            .retour {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #1976d2;
                text-decoration: none;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>Informations du médecin</h1>

            <form method="POST">

                <label>Nom du médecin</label>
                <input type="text" name="nom" required>

                <label>Spécialité</label>
                <input type="text" name="specialite" required>

                <label>Téléphone</label>
                <input type="text" name="telephone">

                <label>Établissement</label>
                <input type="text" name="etablissement">

                <button type="submit">
                    Enregistrer les informations
                </button>

            </form>

            <p class="message">""" + message + """</p>

            <a class="retour" href="/">
                ← Retour à l'accueil
            </a>

        </div>

    </body>

    </html>
    """
@app.route("/voir_qr")
def voir_qr():

    connexion = sqlite3.connect("ordonnance.db")
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT
            ordonnances.id,
            patients.nom,
            patients.prenom
        FROM ordonnances
        JOIN patients
            ON ordonnances.numero_patient = patients.numero
        ORDER BY ordonnances.id DESC
    """)

    ordonnances = curseur.fetchall()
    connexion.close()

    lignes = ""

    for ordonnance in ordonnances:
        lignes += f"""
        <div style="
            background:white;
            padding:20px;
            margin:15px auto;
            max-width:600px;
            border-radius:12px;
            box-shadow:0 3px 10px rgba(0,0,0,0.08);
        ">
            <h3>📋 Ordonnance #{ordonnance[0]}</h3>
            <p>
                <strong>Patient :</strong>
                {ordonnance[1]} {ordonnance[2]}
            </p>

            <a href="/qr/{ordonnance[0]}"
               style="
                   display:inline-block;
                   padding:10px 18px;
                   background:#1f3c88;
                   color:white;
                   text-decoration:none;
                   border-radius:8px;
               ">
               🔳 Voir le QR Code
            </a>
        </div>
        """

    if not lignes:
        lignes = """
        <p style="text-align:center;">
            Aucune ordonnance enregistrée.
        </p>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>QR Codes</title>
    </head>

    <body style="
        font-family:Arial;
        background:#f4f7fb;
        padding:30px;
    ">

        <h1 style="
            text-align:center;
            color:#1f3c88;
        ">
            🔳 QR Codes des ordonnances
        </h1>

        {lignes}

        <a href="/" style="
            display:block;
            width:220px;
            margin:30px auto;
            padding:12px;
            text-align:center;
            background:#1f3c88;
            color:white;
            text-decoration:none;
            border-radius:8px;
        ">
            ← Retour à l'accueil
        </a>

    </body>
    </html>
    """

@app.route("/ordonnance/<int:ordonnance_id>")
def afficher_ordonnance(ordonnance_id):

    connexion = sqlite3.connect("ordonnance.db")
    curseur = connexion.cursor()

    # =========================================================
    # INFORMATIONS PATIENT + MEDECIN
    # =========================================================

    curseur.execute("""
        SELECT
            ordonnances.id,
            patients.numero,
            patients.nom,
            patients.prenom,
            patients.date_naissance,
            medecins.nom,
            medecins.specialite,
            medecins.telephone,
            medecins.etablissement
        FROM ordonnances
        JOIN patients
            ON ordonnances.numero_patient = patients.numero
        JOIN medecins
            ON ordonnances.medecin_id = medecins.id
        WHERE ordonnances.id = ?
    """, (ordonnance_id,))

    ordonnance = curseur.fetchone()

    if not ordonnance:
        connexion.close()
        return "Ordonnance introuvable"

    # =========================================================
    # MEDICAMENTS
    # =========================================================

    curseur.execute("""
        SELECT
            nom,
            dosage,
            posologie,
            duree,
            instructions
        FROM medicaments
        WHERE ordonnance_id = ?
    """, (ordonnance_id,))

    medicaments = curseur.fetchall()

    connexion.close()

    # =========================================================
    # DATE
    # =========================================================

    from datetime import datetime

    date_prescription = datetime.now().strftime("%d/%m/%Y")

    # Pour le projet universitaire :
    validite = "30 jours"

    # =========================================================
    # LISTE DES MEDICAMENTS
    # =========================================================

    liste_medicaments = ""

    for i, medicament in enumerate(medicaments, start=1):

        nom = medicament[0] or "Non précisé"
        dosage = medicament[1] or "Non précisé"
        posologie = medicament[2] or "Non précisée"
        duree = medicament[3] or "Non précisée"
        instructions = medicament[4] or "Aucune"

        liste_medicaments += f"""
        
        <div class="medicament">

            <div class="numero">
                {i}
            </div>

            <div class="medicament-content">

                <h3>
                    {nom}
                </h3>

                <div class="medicament-infos">

                    <div>
                        <span>Dosage</span>
                        <strong>{dosage}</strong>
                    </div>

                    <div>
                        <span>Posologie</span>
                        <strong>{posologie}</strong>
                    </div>

                    <div>
                        <span>Durée</span>
                        <strong>{duree}</strong>
                    </div>

                </div>

                <div class="instructions">

                    <strong>
                        Instructions :
                    </strong>

                    {instructions}

                </div>

            </div>

        </div>
        """

    # =========================================================
    # QR CODE
    # =========================================================

    url = request.host_url.rstrip("/") + \
          "/ordonnance/" + str(ordonnance_id)

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    # =========================================================
    # PAGE
    # =========================================================

    return f"""
<!DOCTYPE html>

<html lang="fr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
    Ordonnance médicale #{ordonnance[0]}
</title>

<style>

/* =========================================================
   GENERAL
========================================================= */

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    padding: 30px;

    background: #eef2f5;

    font-family: Arial, Helvetica, sans-serif;

    color: #222;
}}


/* =========================================================
   FEUILLE
========================================================= */

.ordonnance {{

    max-width: 900px;

    min-height: 1100px;

    margin: auto;

    background: white;

    box-shadow:
        0 6px 25px
        rgba(0,0,0,0.12);

    position: relative;
}}


/* =========================================================
   HEADER
========================================================= */

.header {{

    padding: 35px 40px 25px;

    border-bottom:
        3px solid #1f5f8b;
}}

.header-top {{

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 40px;
}}


/* =========================================================
   PATIENT - GAUCHE
========================================================= */

.patient {{

    text-align: left;

    border-right:
        1px solid #ddd;

    padding-right: 30px;
}}

.patient-title {{

    color: #1f5f8b;

    font-size: 17px;

    font-weight: bold;

    margin-bottom: 12px;

    text-transform: uppercase;
}}

.patient-name {{

    font-size: 21px;

    font-weight: bold;

    margin: 8px 0 15px;

    color: #222;
}}

.patient p {{

    margin: 7px 0;

    font-size: 14px;

    color: #555;
}}


/* =========================================================
   MEDECIN - DROITE
========================================================= */

.medecin {{

    text-align: right;

    padding-left: 30px;
}}

.medecin h1 {{

    margin: 0 0 8px;

    font-size: 24px;

    color: #174a6b;
}}

.specialite {{

    font-weight: bold;

    font-size: 15px;

    margin-bottom: 14px;

    color: #444;
}}

.medecin p {{

    margin: 7px 0;

    font-size: 14px;

    color: #555;
}}


/* =========================================================
   NUMERO + DATE
========================================================= */

.informations-ordonnance {{

    margin-top: 25px;

    padding-top: 15px;

    border-top:
        1px solid #ddd;

    display: flex;

    justify-content:
        space-between;

    font-size: 14px;

    color: #555;
}}

.informations-ordonnance strong {{

    color: #174a6b;
}}


/* =========================================================
   TITRE
========================================================= */

.titre {{

    text-align: center;

    padding: 30px 20px 15px;
}}

.titre h2 {{

    margin: 0;

    color: #174a6b;
font-size: 30px;

    letter-spacing: 2px;
}}

.titre-line {{

    width: 80px;

    height: 3px;

    background: #174a6b;

    margin: 12px auto;
}}


/* =========================================================
   TRAITEMENT
========================================================= */

.traitement {{

    padding: 10px 40px 30px;
}}

.traitement-title {{

    font-size: 19px;

    font-weight: bold;

    color: #174a6b;

    border-bottom:
        1px solid #ddd;

    padding-bottom: 12px;

    margin-bottom: 20px;
}}


/* =========================================================
   MEDICAMENT
========================================================= */

.medicament {{

    display: flex;

    gap: 15px;

    padding: 18px;

    margin-bottom: 15px;

    background: #fafcfd;

    border-left:
        5px solid #1f5f8b;

    border-radius: 8px;
}}

.numero {{

    width: 34px;

    height: 34px;

    min-width: 34px;

    border-radius: 50%;

    background: #1f5f8b;

    color: white;

    display: flex;

    align-items: center;

    justify-content: center;

    font-weight: bold;
}}

.medicament-content {{

    flex: 1;
}}

.medicament-content h3 {{

    margin: 0 0 15px;

    color: #222;

    font-size: 19px;
}}

.medicament-infos {{

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;
}}

.medicament-infos div {{

    background: white;

    padding: 10px;

    border-radius: 7px;

    border:
        1px solid #e2e7eb;
}}

.medicament-infos span {{

    display: block;

    font-size: 12px;

    color: #777;

    margin-bottom: 5px;
}}

.medicament-infos strong {{

    font-size: 14px;

    color: #333;
}}

.instructions {{

    margin-top: 12px;

    padding-top: 10px;

    border-top:
        1px dashed #ccc;

    font-size: 13px;

    color: #555;
}}


/* =========================================================
   SIGNATURE + CACHET
========================================================= */

.signature-zone {{

    display: flex;

    justify-content:
        flex-end;

    align-items:
        flex-start;

    gap: 70px;

    padding:
        35px 40px;
}}

.signature {{

    width: 220px;

    text-align: center;
}}

.signature h3 {{

    font-size: 15px;

    color: #444;

    margin-bottom: 50px;
}}

.signature-line {{

    border-top:
        1px solid #555;

    padding-top: 8px;

    font-size: 12px;

    color: #777;
}}


/* =========================================================
   CACHET
========================================================= */

.cachet {{

    width: 190px;

    height: 110px;

    border:
        3px solid #2878bd;

    border-radius: 12px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    color: #2878bd;

    transform:
        rotate(-2deg);
}}

.cachet strong {{

    font-size: 16px;
}}

.cachet span {{

    font-size: 11px;

    margin-top: 4px;
}}

.cachet small {{

    font-size: 7px;

    margin-top: 8px;

    font-weight: bold;
}}


/* =========================================================
   QR
========================================================= */

.qr-zone {{

    display: flex;

    align-items: center;

    justify-content:
        space-between;

    gap: 30px;

    border-top:
        1px solid #ddd;

    padding:
        25px 40px;
}}

.qr-text {{

    flex: 1;
}}

.qr-text h3 {{

    color: #174a6b;

    margin-top: 0;
}}

.qr-text p {{

    font-size: 13px;

    color: #666;

    line-height: 1.5;
}}

.qr-zone img {{

    width: 150px;

    height: 150px;
}}


/* =========================================================
   FOOTER
========================================================= */

.footer {{

    text-align: center;

    border-top:
        1px solid #ddd;

    padding: 15px;

    font-size: 11px;

    color: #777;
}}


/* =========================================================
   BUTTONS
========================================================= */

.buttons {{

    max-width: 900px;

    margin: 20px auto;

    text-align: center;
}}

.btn {{

    display: inline-block;

    padding:
        12px 22px;

    margin: 5px;

    border-radius: 8px;

    text-decoration: none;

    font-weight: bold;

    border: none;

    cursor: pointer;
}}

.btn-print {{

    background: #1f5f8b;

    color: white;
}}

.btn-home {{

    background: #e5edf2;

    color: #174a6b;
}}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 700px) {{

    body {{
        padding: 8px;
    }}

    .header-top {{
        grid-template-columns: 1fr;
        gap: 20px;
    }}

    .patient {{
        border-right: none;
        border-bottom:
            1px solid #ddd;
        padding-right: 0;
        padding-bottom: 20px;
    }}

    .medecin {{
        text-align: left;
        padding-left: 0;
    }}

    .informations-ordonnance {{
        flex-direction: column;
        gap: 8px;
    }}

    .traitement {{
        padding: 10px 20px 25px;
    }}

    .medicament-infos {{
        grid-template-columns: 1fr;
    }}

    .signature-zone {{
        flex-direction: column;
        align-items: center;
        gap: 35px;
    }}

    .qr-zone {{
        flex-direction: column;
        text-align: center;
    }}

}}


/* =========================================================
   IMPRESSION
========================================================= */

@media print {{

    body {{
        background: white;
        padding: 0;
    }}

    .ordonnance {{
        box-shadow: none;
        max-width: none;
    }}

    .buttons {{
        display: none;
    }}

}}

</style>

</head>


<body>


<!--

   
ORDONNANCE
===================================================== -->

<div class="ordonnance">


    <!-- HEADER -->

    <div class="header">

        <div class="header-top">


            <!-- PATIENT A GAUCHE -->

            <div class="patient">

                <div class="patient-title">
                    Patient
                </div>

                <div class="patient-name">
                    {ordonnance[2]} {ordonnance[3]}
                </div>

                <p>
                    <strong>N° patient :</strong>
                    {ordonnance[1]}
                </p>

                <p>
                    <strong>Date de naissance :</strong>
                    {ordonnance[4] or "Non précisée"}
                </p>

            </div>


            <!-- MEDECIN A DROITE -->

            <div class="medecin">

                <h1>
                    Dr {ordonnance[5]}
                </h1>

                <div class="specialite">
                    {ordonnance[6] or "Médecin"}
                </div>

                <p>
                    <strong>Établissement :</strong>
                    {ordonnance[8] or "Non précisé"}
                </p>

                <p>
                    <strong>Téléphone :</strong>
                    {ordonnance[7] or "Non précisé"}
                </p>

            </div>

        </div>


        <!-- DATE + NUMERO -->

        <div class="informations-ordonnance">

            <div>

                <strong>
                    Ordonnance N° :
                </strong>

                {ordonnance[0]}

            </div>

            <div>

                <strong>
                    Date de prescription :
                </strong>

                {date_prescription}

            </div>

            <div>

                <strong>
                    Validité :
                </strong>

                {validite}

            </div>

        </div>

    </div>


    <!-- TITRE -->

    <div class="titre">

        <h2>
            ORDONNANCE
        </h2>

        <div class="titre-line"></div>

    </div>


    <!-- TRAITEMENT -->

    <div class="traitement">

        <div class="traitement-title">
            Traitement prescrit
        </div>

        {liste_medicaments}

    </div>


    <!-- SIGNATURE + CACHET -->

    <div class="signature-zone">


        <div class="signature">

            <h3>
                Signature du médecin
            </h3>

            <div class="signature-line">
                Dr {ordonnance[5]}
            </div>

        </div>


        <div class="cachet">

            <strong>
                DR {ordonnance[5]}
            </strong>

            <span>
                {ordonnance[6] or "Médecin"}
            </span>

            <span>
                {ordonnance[8] or "Établissement"}
            </span>

            <small>
                DOCUMENT DE DÉMONSTRATION
            </small>

        </div>

    </div>


    <!-- QR CODE -->

    <div class="qr-zone">

        <div class="qr-text">

            <h3>
                Vérification numérique
            </h3>

            <p>
                Scannez le QR Code pour accéder
                à la version numérique de cette
                ordonnance.
            </p>

            <p>
                <strong>
                    Ordonnance médicale intelligente
                </strong>
            </p>

        </div>

        <img
            src="data:image/png;base64,{image_base64}"
            alt="QR Code"
        >

    </div>


    <!-- FOOTER -->

    <div class="footer">

        Ordonnance médicale intelligente
        — Projet universitaire
        — Document de démonstration

    </div>


</div>


<!-- BUTTONS -->

<div class="buttons">

    <button
        class="btn btn-print"
        onclick="window.print()">

        🖨️ Imprimer l'ordonnance

    </button>


    <a
        href="/"
        class="btn btn-home">

        ← Retour à l'accueil

    </a>

</div>


</body>

</html>
"""
@app.route("/ordonnances")
def voir_ordonnances():

    connexion = sqlite3.connect("ordonnance.db")
    curseur = connexion.cursor()

    # =====================================================
    # RECUPERER LES ORDONNANCES
    # =====================================================

    curseur.execute("""
        SELECT
            ordonnances.id,
            patients.nom,
            patients.prenom,
            medecins.nom,
            medecins.specialite
        FROM ordonnances
        JOIN patients
            ON ordonnances.numero_patient = patients.numero
        JOIN medecins
            ON ordonnances.medecin_id = medecins.id
        ORDER BY ordonnances.id DESC
    """)

    ordonnances = curseur.fetchall()

    lignes = ""

    # =====================================================
    # AFFICHER CHAQUE ORDONNANCE
    # =====================================================

    for ordonnance in ordonnances:

        ordonnance_id = ordonnance[0]

        # Recuperer les medicaments
        curseur.execute("""
            SELECT
                nom,
                dosage,
                posologie,
                duree,
                instructions
            FROM medicaments
            WHERE ordonnance_id = ?
        """, (ordonnance_id,))

        medicaments = curseur.fetchall()

        liste_medicaments = ""

        for medicament in medicaments:

            nom = medicament[0] or "Non précisé"
            dosage = medicament[1] or "Non précisé"
            posologie = medicament[2] or "Non précisée"
            duree = medicament[3] or "Non précisée"
            instructions = medicament[4] or "Aucune"

            liste_medicaments += f"""
            <div class="medicament">

                <h3>
                    💊 {nom}
                </h3>

                <p>
                    <strong>Dosage :</strong>
                    {dosage}
                </p>

                <p>
                    <strong>Posologie :</strong>
                    {posologie}
                </p>

                <p>
                    <strong>Durée :</strong>
                    {duree}
                </p>

                <p>
                    <strong>Instructions :</strong>
                    {instructions}
                </p>

            </div>
            """

        # =================================================
        # CARTE DE L'ORDONNANCE
        # =================================================

        lignes += f"""
        <div class="card">

            <div class="card-header">

                <h2>
                    Ordonnance #{ordonnance[0]}
                </h2>

            </div>

            <div class="patient">

                <p>
                    <strong>Patient :</strong>
                    {ordonnance[1]} {ordonnance[2]}
                </p>

            </div>

            <div class="medecin">

                <p>
                    <strong>Médecin :</strong>
                    Dr {ordonnance[3]}
                </p>

                <p>
                    <strong>Spécialité :</strong>
                    {ordonnance[4]}
                </p>

            </div>

            <hr>

            <h2 class="titre-medicaments">
                💊 Médicaments
            </h2>

            {liste_medicaments}

            <div class="actions">

                <a
                    href="/ordonnance/{ordonnance[0]}"
                    class="btn btn-voir">

                    📋 Voir l'ordonnance

                </a>

                <a
                    href="/qr/{ordonnance[0]}"
                    class="btn btn-qr">

                    🔳 Voir le QR Code

                </a>

            </div>

        </div>
        """

    connexion.close()

    # =====================================================
    # SI AUCUNE ORDONNANCE
    # =====================================================

    if not lignes:

        lignes = """
        <div class="vide">

            <p>
                Aucune ordonnance enregistrée.
            </p>

        </div>
        """

    # =====================================================
    # PAGE HTML
    # =====================================================

    return f"""
<!DOCTYPE html>

<html lang="fr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
    Ordonnances médicales
</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    padding: 30px;

    font-family: Arial, sans-serif;

    background: #eef4f9;

    color: #183153;
}}


/* =====================================================
   TITRE
===================================================== */

h1 {{

    text-align: center;

    color: #174a6b;

    margin-bottom: 35px;
}}


/* =====================================================
   CARTE
===================================================== */

.card {{

    max-width: 800px;

    margin: 25px auto;

    background: white;

    padding: 28px;

    border-radius: 15px;

    box-shadow:
        0 5px 20px
        rgba(0,0,0,0.08);
}}


/* =====================================================
   HEADER
===================================================== */

.card-header {{

    border-bottom:
        2px solid #1f5f8b;

    margin-bottom: 20px;

    padding-bottom: 10px;
}}

.card-header h2 {{

    margin: 0;

    color: #174a6b;
}}


/* =====================================================
   INFORMATIONS
===================================================== */

.patient,
.medecin {{

    margin: 10px 0;
}}

.patient p,
.medecin p {{

    margin: 7px 0;

    font-size: 15px;
}}


/* =====================================================
   MEDICAMENTS
===================================================== */

.titre-medicaments {{

    color: #174a6b;

    font-size: 20px;

    margin-bottom: 15px;
}}

.medicament {{

    background: #f4f9fd;

    border-left:
        5px solid #1f5f8b;

    padding: 16px;

    margin: 15px 0;

    border-radius: 10px;
}}

.medicament h3 {{

    margin-top: 0;

    color: #174a6b;
}}

.medicament p {{

    margin: 7px 0;

    color: #444;
}}


/* =====================================================
   BOUTONS
===================================================== */

.actions {{

    margin-top: 20px;

    display: flex;

    gap: 10px;

    flex-wrap: wrap;
}}

.btn {{

    display: inline-block;

    padding:
        12px 18px;

    border-radius: 8px;

    text-decoration: none;

    font-weight: bold;
}}

.btn-voir {{

    background: #1f5f8b;

    color: white;
}}

.btn-qr {{

    background: #e7f0f6;

    color: #174a6b;
}}


/* =====================================================
   AUCUNE ORDONNANCE
===================================================== */

.vide {{

    max-width: 600px;

    margin: 50px auto;

    background: white;

    padding: 30px;

    text-align: center;

    border-radius: 15px;

    color: #666;
}}


/* =====================================================
   RETOUR
===================================================== */

.retour {{

    display: block;

    width: 220px;

    margin: 35px auto;

    padding: 12px;

    text-align: center;

    background: #174a6b;

    color: white;

    text-decoration: none;

    border-radius: 8px;
}}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 600px) {{

    body {{
        padding: 10px;
    }}

    .card {{
        padding: 20px;
    }}

    .actions {{
        flex-direction: column;
    }}

    .btn {{
        text-align: center;
    }}

}}

</style>

</head>


<body>


<h1>
    📋 Ordonnances médicales
</h1>


{lignes}


<a
    href="/"
    class="retour">

    ← Retour à l'accueil

</a>


</body>

</html>
"""
@app.route("/qr/<int:ordonnance_id>")
def qr_ordonnance(ordonnance_id):

    # إنشاء رابط الوصفة
    url = request.host_url.rstrip("/") + "/ordonnance/" + str(ordonnance_id)

    # إنشاء QR Code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    # تحويل الصورة إلى Base64
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"""
    <!DOCTYPE html>

    <html lang="fr">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>
            QR Code - Ordonnance #{ordonnance_id}
        </title>

        <style>

            body {{
                margin: 0;
                padding: 30px;
                font-family: Arial, sans-serif;
                background: #eef4f9;
                color: #183153;
            }}

            .container {{
                max-width: 650px;
                margin: 50px auto;
                background: white;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 25px rgba(0,0,0,0.10);
            }}

            h1 {{
                color: #174a6b;
                margin-bottom: 25px;
            }}

            img {{
                width: 300px;
                height: 300px;
                margin: 20px;
            }}

            p {{
                color: #607789;
                font-size: 16px;
            }}

            .btn {{
                display: inline-block;
                margin-top: 20px;
                padding: 13px 22px;
                background: #174a6b;
                color: white;
                text-decoration: none;
                border-radius: 9px;
                font-weight: bold;
            }}

            .btn:hover {{
                background: #123d59;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>
                🔳 QR Code
            </h1>

            <h2>
                Ordonnance #{ordonnance_id}
            </h2>

            <img
                src="data:image/png;base64,{image_base64}"
                alt="QR Code de l'ordonnance"
            >

            <p>
                Scannez ce QR Code pour accéder
                à l'ordonnance numérique.
            </p>

            <a
                href="/ordonnance/{ordonnance_id}"
                class="btn">

                📋 Voir l'ordonnance

            </a>

            <br>

            <a
                href="/ordonnances"
                class="btn">

                ← Retour aux ordonnances

            </a>

        </div>

    </body>

    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)