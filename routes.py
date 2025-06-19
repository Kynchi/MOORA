from flask import render_template, request, redirect, url_for, flash
from app import app
from app.proses_moora import proses_moora
import os
import tempfile

@app.route("/", methods=["GET", "POST"])
def index():
    top5 = bottom5 = message = None
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            suffix = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                file.save(tmp.name)
                temp_path = tmp.name  # simpan path-nya
            df = proses_moora(temp_path)  # proses setelah file tertutup
            os.unlink(temp_path)
            if not df.empty:
                top5 = df.sort_values("Nilai MOORA", ascending=False).head(5).to_dict(orient="records")
                bottom5 = df.sort_values("Nilai MOORA", ascending=True).head(5).to_dict(orient="records")
            else:
                message = "File tidak valid atau data kosong."
        else:
            message = "Silakan upload file terlebih dahulu."
    return render_template("index.html", top5=top5, bottom5=bottom5, message=message)
