from flask import Flask, render_template_string, request
import subprocess, os, datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <title>Jarvis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#ff6600">
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🤖</text></svg>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: #0a0a0a; color: #fff; padding: 16px; }
      .header { text-align: center; padding: 20px 0; }
      .header h1 { font-size: 28px; color: #ff6600; }
      .card { background: #1a1a1a; border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid #333; }
        textarea { width: 100%; height: 120px; background: #0a0a0a; color: #fff; border: 1px solid #333; border-radius: 12px; padding: 16px; font-size: 16px; }
      .btn { width: 100%; background: #ff6600; color: #000; padding: 18px; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; margin-top: 12px; }
      .btn-mic { background: #222; color: #ff6600; border: 2px solid #ff6600; }
      .btn-live { background: #00ff88; color: #000; }
        iframe { width: 100%; height: 60vh; border: 2px solid #333; border-radius: 12px; background: white; }
      .status { text-align: center; color: #00ff88; font-weight: bold; padding: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 JARVIS</h1>
        <p>Deine Geldmaschinen-Fabrik</p>
    </div>
    <div class="card">
        <button class="btn btn-mic" onclick="startMic()">🎤 Sprachbefehl</button>
        <form method="post" id="form">
            <textarea name="prompt" id="prompt" placeholder="Sag: Bau Saugroboter Seite mit Roborock Dreame Ecovacs">{{ prompt }}</textarea>
            <button type="submit" class="btn">1. Vorschau generieren</button>
        </form>
    </div>
    {% if code %}
    <div class="card">
        <h3>Live-Vorschau:</h3>
        <iframe srcdoc="{{ code }}"></iframe>
        <form method="post" action="/deploy">
            <input type="hidden" name="code" value="{{ code }}">
            <input type="hidden" name="filename" value="{{ filename }}">
            <button type="submit" class="btn btn-live">2. LIVE SCHALTEN</button>
        </form>
    </div>
    {% endif %}
    {% if deployed %}
    <div class="status">✅ LIVE! GitHub Repo geupdated.</div>
    {% endif %}
<script>
if ('serviceWorker' in navigator) { navigator.serviceWorker.register('/sw.js'); }
function startMic() {
    const rec = new webkitSpeechRecognition() || new SpeechRecognition();
    rec.lang = 'de-DE';
    rec.start();
    rec.onresult = e => {
        document.getElementById('prompt').value = e.results[0][0].transcript;
        document.getElementById('form').submit();
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    filename, code = generate_site(prompt)
    return render_template_string(HTML, code=code, filename=filename, prompt=prompt)

@app.route('/deploy', methods=['POST'])
def deploy():
    code, filename = request.form['code'], request.form['filename']
    with open(filename, 'w') as f: f.write(code)
    subprocess.run(['git', 'add', filename])
    subprocess.run(['git', 'commit', '-m', f'Jarvis Deploy {datetime.datetime.now()}'])
    subprocess.run(['git', 'push'])
    return render_template_string(HTML, deployed=True, filename=filename)

@app.route('/manifest.json')
def manifest():
    return {"name":"Jarvis","short_name":"Jarvis","start_url":"/","display":"standalone","background_color":"#0a0a0a","theme_color":"#ff6600","icons":[{"src":"data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🤖</text></svg>","sizes":"512x512"}]}

@app.route('/sw.js')
def sw(): return 'self.addEventListener("fetch", e => {});', 200, {'Content-Type': 'application/javascript'}

def generate_site(prompt):
    if "saugroboter" in prompt.lower():
        return "index.html", """<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"><title>Saugroboter Test</title><style>body{font-family:Arial;max-width:800px;margin:0 auto;padding:20px}.test-box{border:1px solid #ddd;padding:20px;margin:20px 0;border-radius:8px}.winner{border:2px solid #ff6600;background:#fff9f5}.cta-button{display:block;background:#ff6600;color:white;padding:15px;text-align:center;text-decoration:none;border-radius:5px;font-weight:bold;margin-top:15px}h2{color:#ff6600;margin-top:0}</style></head><body><h1>Saugroboter Test 2025: Die 3 Besten für Tierhaare & Teppich</h1><p>Nach 40 Stunden Test: Diese 3 Saugroboter entfernen Hunde- und Katzenhaare wirklich.</p><div class="test-box winner"><h2>1. Testsieger: Roborock S8 MaxV Ultra</h2><p><strong>Bestnote: 1,4</strong> - Beste Saugleistung auf Teppich.</p><a href="ROBOROCK-LINK?tag=fairdeals21-21" class="cta-button">➡️ Zum besten Preis bei Amazon</a></div><div class="test-box"><h2>2. Preis-Leistungs-Sieger: Dreame L40s Pro Ultra</h2><p><strong>Note: 1,6</strong> - Hebt Wischmopps bei Teppich an.</p><a href="DREAME-LINK?tag=fairdeals21-21" class="cta-button">➡️ Zum Angebot bei Amazon</a></div><div class="test-box"><h2>3. Für große Wohnungen: Ecovacs Deebot T80 Omni</h2><p><strong>Note: 1,8</strong> - Eckige Bauform reinigt Kanten besser.</p><a href="ECOVACS-LINK?tag=fairdeals21-21" class="cta-button">➡️ Jetzt auf Amazon ansehen</a></div></body></html>"""
    return "seite.html", f"<h1>Jarvis baut:</h1><p>{prompt}</p>"

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)

