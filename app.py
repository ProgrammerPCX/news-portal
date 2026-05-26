from flask import Flask, render_template, request, abort
import threading
import time
import random
from datetime import datetime

app = Flask(__name__)
data_lock = threading.Lock()

# DATABASE NOTIZIE CON CONTENUTI DI GEOPOLITICA ED ECONOMIA
NEWS_DATABASE = [
    {
        "id": 1,
        "date": "26 Maggio 2026",
        "time": "15:30",
        "category": "GEOPOLITICA",
        "title": "Rotte del Pacifico: accordi bilaterali silenziosi cambiano gli equilibri",
        "summary": "Mentre i media tradizionali si focalizzano sui conflitti noti, una fitta rete di trattative infrastrutturali sta ridisegnando il controllo dei canali sottomarini.",
        "content": "Nuovi dati tracciati dai nodi indipendenti confermano lo spostamento di flotte commerciali e la firma di trattati bilaterali non pubblicizzati nei canali televisivi mainstream. Il controllo dei flussi digitali nel Pacifico meridionale sta passando di mano, ridefinendo il concetto stesso di sovranità tecnologica per i prossimi vent'anni. Gli analisti geopolitici parlano di una 'guerra silenziosa' per il controllo dei server di snodo.",
        "urgency": "BREAKING",
        "views": 1420
    },
    {
        "id": 2,
        "date": "26 Maggio 2026",
        "time": "14:15",
        "category": "ECONOMIA",
        "title": "La stretta sulla liquidità fisica e la transizione ai token di Stato",
        "summary": "Analisi tecnica sui piani di introduzione delle valute digitali centralizzate (CBDC) e la progressiva svalutazione del contante.",
        "content": "I tassi d'interesse reali continuano a subire fluttuazioni strutturali nascoste da manovre di facciata. Dietro i proclami di stabilità, i principali istituti bancari stanno testando protocolli di valuta digitale centralizzata con scadenza d'uso. Questo significa che i risparmi potrebbero avere un 'termine di consumazione', una notizia che difficilmente troverà spazio nei telegiornali di prima serata ma che cambierà radicalmente il mercato economico globale.",
        "urgency": "NORMAL",
        "views": 985
    },
    {
        "id": 3,
        "date": "26 Maggio 2026",
        "time": "11:00",
        "category": "MEDIA & DIRETTE",
        "title": "La resistenza della carta stampata indipendente contro la censura degli algoritmi",
        "summary": "Cresce il mercato delle autoproduzioni editoriali come ultimo baluardo di critica sociale non filtrata.",
        "content": "Mentre le grandi corporazioni dell'intrattenimento si piegano alle linee guida degli algoritmi di distribuzione digitale, assistiamo a un boom senza precedenti delle stampe d'inchiesta underground. Scrittori e giornalisti stanno tornando al circuito puramente analogico per trattare temi geopolitici e sociali scottanti, proteggendo le proprie opere dalla cancellazione selettiva del web.",
        "urgency": "NORMAL",
        "views": 640
    }
]

PORTAL_METRICS = {
    "total_visits": 3104,
    "active_readers": 42,
    "server_status": "ONLINE"
}

def live_news_ticker_kernel():
    global NEWS_DATABASE
    pool = [
        {
            "category": "GEOPOLITICA",
            "title": "Spostamenti di capitali nel settore dei microchip: rotte alternative bypassano le sanzioni",
            "summary": "Dati doganali riservati mostrano triangolazioni commerciali inedite nel sud-est asiatico.",
            "content": "Le catene di approvvigionamento delle terre rare stanno subendo una mutazione strutturale. Grandi cargo non tracciati dai radar commerciali standard stanno scaricando materiali critici in porti secondari, eludendo i blocchi ufficiali."
        },
        {
            "category": "ECONOMIA",
            "title": "Beni rifugio: l'impennata delle materie prime agricole scuote i mercati ombra",
            "summary": "L'oro e i titoli di stato perdono terreno rispetto ai contratti di stoccaggio del grano.",
            "content": "I fondi d'investimento speculativi stanno accumulando asset legati alle risorse idriche e alimentari. Questa transizione, ignorata dai media di massa, indica una preparazione a medio termine per scenari di forte stress economico."
        }
    ]
    
    while True:
        time.sleep(20)
        with data_lock:
            item = random.choice(pool)
            if not any(n["title"] == item["title"] for n in NEWS_DATABASE):
                new_id = len(NEWS_DATABASE) + 1
                now = datetime.now()
                NEWS_DATABASE.insert(0, {
                    "id": new_id,
                    "date": now.strftime("%d %B %Y"),
                    "time": now.strftime("%H:%M"),
                    "category": item["category"],
                    "title": item["title"],
                    "summary": item["summary"],
                    "content": item["content"],
                    "urgency": "BREAKING",
                    "views": random.randint(50, 150)
                })
                if len(NEWS_DATABASE) > 10:
                    NEWS_DATABASE.pop()

@app.route('/')
def home_index():
    global PORTAL_METRICS
    with data_lock:
        PORTAL_METRICS["total_visits"] += 1
        breaking_news = [n for n in NEWS_DATABASE if n["urgency"] == "BREAKING"]
        normal_news = [n for n in NEWS_DATABASE if n["urgency"] != "BREAKING"]
    return render_template('index.html', breaking=breaking_news, normal=normal_news, metrics=PORTAL_METRICS)

@app.route('/notizia/<int:news_id>')
def news_detail(news_id):
    with data_lock:
        article = next((n for n in NEWS_DATABASE if n["id"] == news_id), None)
        if article:
            article["views"] += 1
    if not article:
        abort(404)
    return render_template('news_detail.html', item=article)

@app.route('/sistema/telemetria')
def telemetry():
    return render_template('telemetry.html', metrics=PORTAL_METRICS, total_articles=len(NEWS_DATABASE))

if __name__ == '__main__':
    threading.Thread(target=live_news_ticker_kernel, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
