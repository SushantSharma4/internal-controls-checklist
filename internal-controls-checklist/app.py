from flask import Flask, render_template, url_for, request, redirect, session

import random

app = Flask(__name__)
app.secret_key = 'sushant_secret_key'


USERNAME = "admin"
PASSWORD = "admin123"


controls = [
    {
        'id': 1,
        'question': 'Is access control implemented for all critical systems?',
        'compliant': False,
    },
    {
        'id': 2,
        'question': 'Are regular backups being performed and tested?',
        'compliant': True,
    }
]


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == "POST":
        control_question = request.form["control_question"]
        cur_id = random.randint(100, 1000)
        controls.append({
            'id': cur_id,
            'question': control_question,
            'compliant': False
        })
    return render_template("index.html", items=controls)

@app.route("/toggle/<int:control_id>", methods=["POST"])
def toggle_compliance(control_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    for control in controls:
        if control['id'] == control_id:
            control['compliant'] = not control['compliant']
            break
    return redirect(url_for("home"))

@app.route("/delete/<int:control_id>", methods=["POST"])
def delete_control(control_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    global controls
    controls = [c for c in controls if c['id'] != control_id]
    return redirect(url_for("home"))

@app.route("/result")
def result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    total = len(controls)
    compliant = sum(1 for c in controls if c['compliant'])
    non_compliant = total - compliant
    score = round((compliant / total) * 100) if total else 0

    return render_template("result.html", items=controls,
                           total=total, compliant=compliant,
                           non_compliant=non_compliant, score=score)


if __name__ == "__main__":
    app.run(debug=True)
