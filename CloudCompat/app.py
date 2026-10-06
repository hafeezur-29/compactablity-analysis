from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import requests, re, time

app = Flask(__name__)

CLOUDS = {
    "Small": {"cpu": 1, "ram": 1, "storage": 10},
    "Standard": {"cpu": 2, "ram": 4, "storage": 30},
    "Performance": {"cpu": 4, "ram": 8, "storage": 60},
    "High Performance": {"cpu": 8, "ram": 16, "storage": 120},
}

def analyze_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    started = time.perf_counter()
    r = requests.get(url, timeout=8, headers={"User-Agent": "CloudCompat/1.0"})
    load_ms = round((time.perf_counter() - started) * 1000)
    html = r.text[:500000]
    size_mb = round(len(r.content) / 1024 / 1024, 2)

    tech = []
    patterns = {
        "React": r"react",
        "Next.js": r"__next|next/static",
        "Vue": r"vue",
        "Angular": r"ng-version|angular",
        "WordPress": r"wp-content|wordpress",
        "PHP": r"\.php",
    }
    for name, pattern in patterns.items():
        if re.search(pattern, html, re.I):
            tech.append(name)

    return {
        "url": url, "status": r.status_code, "load_ms": load_ms,
        "page_mb": size_mb, "server": r.headers.get("Server", "Unknown"),
        "technology": tech or ["Unknown / Static Web"],
        "https": url.startswith("https://")
    }

def estimate(data):
    tech = " ".join(data["technology"]).lower()
    cpu, ram, storage = 1, 1, max(10, round(data["page_mb"] * 10))
    if any(x in tech for x in ["react", "vue", "angular", "next"]):
        cpu, ram = 1, 2
    if "wordpress" in tech or "php" in tech:
        cpu, ram = 2, 2
    if data["load_ms"] > 1500:
        cpu += 1
    if data["page_mb"] > 3:
        ram += 1

    return {"cpu": cpu, "ram": ram, "storage": storage}

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    url = request.json.get("url", "").strip()
    if not url:
        return jsonify(error="Enter a website URL"), 400
    try:
        data = analyze_url(url)
        req = estimate(data)
        result = []
        for name, machine in CLOUDS.items():
            ok = (machine["cpu"] >= req["cpu"] and
                  machine["ram"] >= req["ram"] and
                  machine["storage"] >= req["storage"])
            result.append({"name": name, "ok": ok, **machine})
        recommended = next((x["name"] for x in result if x["ok"]), "Custom / Larger")
        return jsonify(scan=data, requirements=req, machines=result,
                        recommended=recommended, compatibility="Compatible")
    except Exception as e:
        return jsonify(error=f"Could not analyze the target: {e}"), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
