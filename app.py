from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import csv

app = Flask(__name__)
app.secret_key = "secret123"

# Load ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login():
    return render_template("login.html")


# ---------------- REGISTER PAGE ----------------
@app.route('/register')
def register():
    return render_template("register.html")


# ---------------- SAVE USER ----------------
@app.route('/register_user', methods=['POST'])
def register_user():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    with open("users.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, password])

    return redirect(url_for('login'))


# ---------------- LOGIN VALIDATION ----------------
@app.route('/login', methods=['POST'])
def login_user():

    email = request.form['email']
    password = request.form['password']

    with open("users.csv", "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[1] == email and row[2] == password:
                session['user'] = email
                return redirect(url_for('home'))

    return render_template("login.html", error="Invalid Email or Password")


# ---------------- HOME PAGE ----------------
@app.route('/home')
def home():

    if 'user' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))


# ---------------- PREDICTION ----------------
@app.route('/predict', methods=['POST'])
def predict():

    if 'user' not in session:
        return redirect(url_for('login'))

    age = int(request.form['age'])
    credit = int(request.form['credit'])
    mileage = int(request.form['mileage'])
    ownership = int(request.form['ownership'])
    year = int(request.form['year'])
    violations = int(request.form['violations'])

    features = np.array([[age, credit, mileage, ownership, year, violations]])

    prediction = model.predict(features)

    if prediction[0] == 1:
        result = "Insurance Claim Likely"
    else:
        result = "No Claim Expected"

    return render_template("index.html", prediction_result=result)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# RUN APP
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)