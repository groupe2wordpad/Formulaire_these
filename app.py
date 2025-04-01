from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reponses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT,
                age INTEGER,
                profession TEXT,
                niveau_cybersecurite TEXT,
                attaque TEXT,
                type_attaque TEXT,
                vpn TEXT,
                donnees TEXT,
                fuite TEXT,
                commentaire TEXT,
                accord_these TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def formulaire():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    accord_these = request.form['accord_these']
    
    # Si la personne ne donne pas son accord, ne pas enregistrer
    if accord_these == "non":
        return redirect(url_for('thankyou'))
    
    data = (
        request.form['nom'], request.form['prenom'], request.form['age'],
        request.form['profession'], request.form['niveau_cybersecurite'],
        request.form['attaque'], request.form.get('type_attaque', ''),
        request.form['vpn'], request.form['donnees'], request.form['fuite'],
        request.form.get('commentaire', ''), accord_these
    )
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reponses (nom, prenom, age, profession, niveau_cybersecurite, attaque, type_attaque, vpn, donnees, fuite, commentaire, accord_these)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
    
    return redirect(url_for('thankyou'))

@app.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")

@app.route('/reponses')
def voir_reponses():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reponses")
        reponses = cursor.fetchall()
    return {"reponses": reponses}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
