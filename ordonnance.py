from flask import Flask, request, redirect
import sqlite3
import qrcode
import io
import base64

app = Flask(__name__)


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

@app.route("/qr/<int:ordonnance_id>")
def qr_ordonnance(ordonnance_id):

    url = request.host_url + "ordonnance/" + str(ordonnance_id)



    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"""
    <div style="text-align:center; margin-top:50px;">
        <h1>QR Code de l'ordonnance #{ordonnance_id}</h1>

        <img src="data:image/png;base64,{image_base64}"
             width="300">

        <p>Scannez ce QR Code pour accéder à l'ordonnance.</p>
    </div>
    """
@app.route("/ordonnance/<int:ordonnance_id>")
def afficher_ordonnance(ordonnance_id):

    connexion = sqlite3.connect("ordonnance.db")
    curseur = connexion.cursor()

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
        WHERE ordonnances.id = ?
    """, (ordonnance_id,))

    ordonnance = curseur.fetchone()

    if not ordonnance:
        connexion.close()
        return "Ordonnance introuvable"

    curseur.execute("""
        SELECT nom, dosage, posologie, duree, instructions
        FROM medicaments
        WHERE ordonnance_id = ?
    """, (ordonnance_id,))

    medicaments = curseur.fetchall()
    connexion.close()

    liste = ""

    for medicament in medicaments:
        liste += f"""
        <div style="
            background:#f1f7ff;
            padding:15px;
            margin:15px 0;
            border-left:5px solid #1f3c88;
            border-radius:10px;
        ">
            <h3>💊 {medicament[0]}</h3>
            <p><strong>Dosage :</strong> {medicament[1] or "Non précisé"}</p>
            <p><strong>Posologie :</strong> {medicament[2] or "Non précisée"}</p>
            <p><strong>Durée :</strong> {medicament[3] or "Non précisée"}</p>
            <p><strong>Instructions :</strong> {medicament[4] or "Aucune"}</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Ordonnance #{ordonnance[0]}</title>
    </head>

    <body style="
        font-family:Arial;
        background:#f4f7fb;
        padding:30px;
    ">

        <div style="
            max-width:700px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:15px;
        ">

            <h1>📋 Ordonnance médicale #{ordonnance[0]}</h1>

            <p>
                <strong>Patient :</strong>
                {ordonnance[1]} {ordonnance[2]}
            </p>

            <p>
                <strong>Médecin :</strong>
                Dr {ordonnance[3]}
            </p>

            <p>
                <strong>Spécialité :</strong>
                {ordonnance[4]}
            </p>

            <hr>

            <h2>💊 Médicaments</h2>

            {liste}

        </div>

    </body>
    </html>
    """

@app.route("/ordonnances")
def voir_ordonnances():

    connexion = sqlite3.connect("ordonnance.db")
    curseur = connexion.cursor()

    # Récupérer les ordonnances
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

    for ordonnance in ordonnances:

        ordonnance_id = ordonnance[0]

        # Récupérer tous les médicaments de cette ordonnance
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
            liste_medicaments += f"""
            <div class="medicament">
                <h3>💊 {medicament[0]}</h3>

                <p><strong>Dosage :</strong>
                {medicament[1] or "Non précisé"}</p>

                <p><strong>Posologie :</strong>
                {medicament[2] or "Non précisée"}</p>

                <p><strong>Durée :</strong>
                {medicament[3] or "Non précisée"}</p>

                <p><strong>Instructions :</strong>
                {medicament[4] or "Aucune"}</p>
            </div>
            """

        lignes += f"""
        <div class="card">

            <h2>Ordonnance #{ordonnance[0]}</h2>

            <p>
                <strong>Patient :</strong>
                {ordonnance[1]} {ordonnance[2]}
            </p>

            <p>
                <strong>Médecin :</strong>
                Dr {ordonnance[3]}
            </p>

            <p>
                <strong>Spécialité :</strong>
                {ordonnance[4]}
            </p>

            <hr>

            <h2>💊 Médicaments</h2>

            {liste_medicaments}
<a href="/qr/{ordonnance[0]}"
   style="
       display:inline-block;
       margin-top:15px;
       padding:12px 20px;
       background:#1f3c88;
       color:white;
       text-decoration:none;
       border-radius:8px;
   ">
   🔳 Voir le QR Code
</a>
        </div>
        """

    connexion.close()

    if not lignes:
        lignes = """
        <p class="vide">
            Aucune ordonnance enregistrée.
        </p>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fr">

    <head>

        <meta charset="UTF-8">

        <title>Ordonnances</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
                padding: 30px;
            }}

            h1 {{
                text-align: center;
                color: #1f3c88;
                margin-bottom: 30px;
            }}

            .card {{
                background: white;
                max-width: 750px;
                margin: 20px auto;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }}

            .card h2 {{
                color: #1f3c88;
            }}

            .card p {{
                font-size: 16px;
                line-height: 1.6;
            }}

            .medicament {{
                background: #f1f7ff;
                border-left: 5px solid #1f3c88;
                padding: 15px;
                margin: 15px 0;
                border-radius: 10px;
            }}

            .medicament h3 {{
                margin-top: 0;
                color: #1f3c88;
            }}

            hr {{
                border: none;
                border-top: 1px solid #ddd;
                margin: 20px 0;
            }}

            .vide {{
                text-align: center;
                font-size: 18px;
            }}

            .retour {{
                display: block;
                width: 220px;
                margin: 30px auto;
                padding: 12px;
                text-align: center;
                background: #1f3c88;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}

        </style>

    </head>

    <body>

        <h1>📋 Ordonnances médicales</h1>

        {lignes}

        <a class="retour" href="/">
            ← Retour à l'accueil
        </a>

    </body>

    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)