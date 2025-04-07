from flask import Flask, render_template, request
from generator import generuj_wszystkie_warianty, generuj_konkretne_akordy, generuj_optymalne_akordy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'warianty':
            tonika = request.form.get('tonika')
            typ = request.form.get('typ')
            obraz = generuj_wszystkie_warianty(tonika, typ)
            return render_template("index.html", obraz=obraz, tonika=tonika, typ=typ)
        elif form_type == 'konkretne':
            dane = request.form.get('akordy_konkretne')
            obraz = generuj_konkretne_akordy(dane)
            return render_template("index.html", obraz=obraz)
        elif form_type == 'optymalne':
            dane = request.form.get('akordy_optymalne')
            obraz = generuj_optymalne_akordy(dane)
            return render_template("index.html", obraz=obraz)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)