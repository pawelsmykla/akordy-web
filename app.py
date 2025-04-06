from flask import Flask, render_template, request, send_file
from generator import generuj_wizualizacje
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tonika = request.form["tonika"]
        typ = request.form["typ"]
        output_path = generuj_wizualizacje(tonika, typ)
        return render_template("index.html", tonika=tonika, typ=typ, obraz=output_path)
    return render_template("index.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

# app.py placeholder
