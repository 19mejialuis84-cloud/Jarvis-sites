from flask import Flask, request, jsonify, render_template_string
import subprocess
import os
import re
from datetime import datetime

app = Flask(__name__)

# JARVIS V3 BRAIN - Er versteht deine Befehle + Amazon ID
AMAZON_ID = "Fairdeals21-21"

def jarvis_brain(prompt):
    prompt = prompt.lower()
    
    # Regel: "Bau Seite 3 Luftreiniger mit Levoit Philips Xiaomi"
    if "bau seite" in prompt and "mit" in prompt:
        match = re.search(r'bau seite (\d+) (.+?) mit (.+)', prompt)
        if match:
            anzahl = int(match.group(1))
            produkt = match.group(2).strip()
            marken = [m.strip().title() for m in match.group(3).split()]
            return generiere_affiliate_seite(anzahl, produkt, marken)
    
    return f"<h1>{prompt}</h1><p>Jarvis V3 hat dich verstanden.</p>"

def generiere_affiliate_seite(anzahl, produkt, marken):
    daten = {
        "levoit": {"modell": "Core 300S", "cadr": "230", "preis": "99", "vorteil": "Testsieger 2026"},
        "philips": {"modell": "AC0820/10", "cadr": "190", "preis": "79", "vorteil": "Flüsterleise 19dB"},
        "xiaomi": {"modell": "Air Purifier 4 Pro", "cadr": "400", "preis": "199", "vorteil": "App-Steuerung"},
        "roborock": {"modell": "S8 MaxV Ultra", "cadr": "0", "preis": "1299", "vorteil": "Saugen+Wischen"},
        "dyson": {"modell": "V15 Detect", "cadr": "0", "preis": "749", "vorteil": "Laser-Erkennung"},
        "ecovacs": {"modell": "Deebot X2 Omni", "cadr": "0", "preis": "1099", "vorteil": "KI-Hindernis"},
        "bosch": {"modell": "Unlimited 7", "cadr": "0", "preis": "399", "vorteil": "Wechselakku"},
        "siemens": {"modell": "EQ.6 Plus", "cadr": "0", "preis": "699", "vorteil": "OneTouch"},
        "delonghi": {"modell": "Magnifica S", "cadr": "0", "preis": "349", "vorteil": "Milchschaum"},
        "melitta": {"modell": "Caffeo Solo", "cadr": "0", "preis": "199", "vorteil": "Kompakt"},
        "jura": {"modell": "E8", "cadr": "0", "preis": "999", "vorteil": "P.E.P. Brühgruppe"}
    }
    
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{produkt.title()} Test 2026 - Die {anzahl} Besten</title>
        <style>
            body {{ font-family: -apple-system, Arial; margin:0; padding:15px; background:#f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .card {{ background:white; border-radius:12px; padding:20px; margin:15px 0; box-shadow:0 2px 8px rgba(0,0,0,0.1); }}
            .btn {{ background:#FF9900; color:#000; padding:15px 25px; border:none; border-radius:8px; font-size:18px; font-weight:bold; cursor:pointer; width:100%; text-decoration:none; display:block; text-align:center; }}
            .preis {{ font-size:26px; color:#B12704; font-weight:bold; margin:10px 0; }}
            .cadr {{ background:#E8F5E8; padding:8px 12px; border-radius:6px; display:inline-block; margin:5px 0; }}
            h1 {{ color:#111; }} h2 {{ color:#FF6600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏆 {produkt.title()} Test {datetime.now().year}</h1>
            <p>Jarvis hat für dich die {anzahl} besten {produkt} analysiert. Stand: {datetime.now().strftime('%d.%m.%Y')}</p>
    """
    
    for i, marke in enumerate(marken[:anzahl]):
        m = marke.lower()
        info = daten.get(m, {"modell": f"{marke} Pro", "cadr": "200", "preis": "99", "vorteil": "Gutes Modell"})
        amazon_link = f"https://www.amazon.de/s?k={marke}+{produkt}&tag={AMAZON_ID}"
        badge = "🥇 Testsieger" if i == 0 else "🥈 Preis-Tipp" if i == 1 else "🥉 Profi-Wahl" if i == 2 else f"Platz {i+1}"
        
        html += f"""
            <div class="card">
                <h2>{badge}: {marke} {info['modell']}</h2>
                <p><b>Vorteil:</b> {info['vorteil']}</p>
                {"<p class='cadr'><b>CADR:</b> " + info['cadr'] + " m³/h</p>" if info['cadr'] != "0" else ""}
                <p class="preis">{info['preis']}€</p>
                <a href="{amazon_link}" target="_blank" class="btn">→ Jetzt bei Amazon prüfen</a>
            </div>
        """
    
    html += """
            <div class="card">
                <h3>🤖 Erstellt mit Jarvis V3</h3>
                <p>Diese Affiliate-Seite wurde in 3 Sekunden generiert.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/')
def home():
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jarvis V3 Geldmaschine</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial; padding:20px; background:#0a0a0a; color:white; }
            input { width:100%; padding:15px; font-size:16px; margin:10px 0; background:#1a1a1a; color:white; border:1px solid #333; border-radius:8px; }
            button { padding:15px 25px; font-size:18px; margin:5px; background:#FF6600; color:#000; border:none; border-radius:8px; font-weight:bold; }
            #preview { border:2px solid #FF6600; margin-top:20px; height:500px; width:100%; border-radius:8px; }
        </style>
    </head>
    <body>
        <h1>🤖 JARVIS V3 - Geldmaschine</h1>
        <p><b>Beispiel:</b> Bau Seite 3 Luftreiniger mit Levoit Philips Xiaomi</p>
        <input type="text" id="prompt" placeholder="Dein Befehl für Jarvis...">
        <button onclick="generieren()">🎤 1. Generieren</button>
        <button onclick="deploy()">🚀 2. LIVE SCHALTEN</button>
        <iframe id="preview"></iframe>

        <script>
        let currentHTML = "";
        function generieren() {
            const prompt = document.getElementById('prompt').value;
            fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: prompt})
            })
            .then(r => r.json())
            .then(data => {
                currentHTML = data.html;
                document.getElementById('preview').srcdoc = currentHTML;
            });
        }
        function deploy() {
            if(!currentHTML) { alert('Erst Generieren klicken!'); return; }
            fetch('/deploy', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({html: currentHTML})
            })
            .then(r => r.json())
            .then(data => {
                alert('💰 LIVE! ' + data.url);
                window.open(data.url, '_blank');
            });
        }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '')
    html = jarvis_brain(prompt)
    return jsonify({"html": html})

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    html = data.get('html', '')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    subprocess.run(['git', 'add', 'index.html'])
    subprocess.run(['git', 'commit', '-m', f'Jarvis V3: {datetime.now()}'])
    subprocess.run(['git', 'push'])
    return jsonify({"url": "https://19mejialuis84-cloud.github.io/Jarviy-sites/"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
