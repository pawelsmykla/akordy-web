if __name__ == "__main__":
    import os
    if os.environ.get("RENDER") == "true":
        # Render użyje wersji webowej
        from flask import Flask, render_template
        app = Flask(__name__)

        @app.route("/")
        def home():
            return render_template("index.html")

        app.run(host="0.0.0.0", port=10000)
    else:
        uruchom_gui()
