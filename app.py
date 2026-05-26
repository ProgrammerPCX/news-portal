from flask import Flask, render_template, jsonify

app = Flask(__name__)

# -------------------------
# DATI DI ESEMPIO (sostituisci con i tuoi)
# -------------------------
breaking = []
normal = []

metrics = {
    "active_readers": 0,
    "total_visits": 0,
    "server_status": "OPERATIVO"
}

# -------------------------
# CACHE HTTP SERIA
# -------------------------
@app.after_request
def add_cache_headers(response):
    if response.content_type and "text/html" in response.content_type:
        # HTML aggiornabile ogni 15 minuti
        response.headers["Cache-Control"] = "public, max-age=900"

    elif response.content_type and "application/json" in response.content_type:
        # API più reattiva
        response.headers["Cache-Control"] = "public, max-age=60"

    else:
        # static assets (css, js, immagini)
        response.headers["Cache-Control"] = "public, max-age=86400"

    return response


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    metrics["total_visits"] += 1

    return render_template(
        "index.html",
        breaking=breaking,
        normal=normal,
        metrics=metrics
    )


# -------------------------
# NEWS DETAIL
# -------------------------
@app.route("/notizia/<int:item_id>")
def news_detail(item_id):
    # esempio minimale: sostituisci con DB reale
    item = {
        "id": item_id,
        "title": "Articolo esempio",
        "category": "Generale",
        "summary": "Riassunto esempio",
        "content": "Contenuto completo dell'articolo.",
        "date": "2026-05-26",
        "time": "12:00",
        "views": 0
    }

    return render_template("news_detail.html", item=item)


# -------------------------
# TELEMETRIA
# -------------------------
@app.route("/sistema/telemetria")
def telemetry():
    return render_template(
        "telemetry.html",
        metrics=metrics,
        total_articles=len(breaking) + len(normal)
    )


# -------------------------
# API (per futuro upgrade senza reload pagina)
# -------------------------
@app.route("/api/news")
def api_news():
    return jsonify({
        "breaking": breaking,
        "normal": normal,
        "metrics": metrics
    })


if __name__ == "__main__":
    app.run(debug=True)
