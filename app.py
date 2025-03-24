from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

OPERATIVE_PIN = "1234"

def load_sites_and_plots():
    try:
        with open("sites_and_plots.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        pin = request.form["pin"]

        if pin == OPERATIVE_PIN:
            return redirect(url_for("upload", name=name))
        else:
            flash("Incorrect PIN. Try again.")
    
    return render_template("login.html")

@app.route("/upload/<name>", methods=["GET", "POST"])
def upload(name):
    data = load_sites_and_plots()
    sites = list(data.keys())
    plots = data

    if request.method == "POST":
        site = request.form["site"]
        plot = request.form["plot"]
        photo = request.files["photo"]

        if photo:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{name}_{site}_{plot}_{timestamp}_{photo.filename}"
            site_folder = os.path.join(app.config["UPLOAD_FOLDER"], site, plot)
            os.makedirs(site_folder, exist_ok=True)
            photo.save(os.path.join(site_folder, filename))
            flash("Photo uploaded successfully!")

    return render_template("upload.html", name=name, sites=sites, plots=plots)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

