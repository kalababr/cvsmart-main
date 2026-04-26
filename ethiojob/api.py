from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

JOBS_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__) or "."), "jobs.json")


def load_jobs():
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    seen = {}
    for item in raw:
        link = item.get("link", "")
        title = item.get("title", "")
        if "/job/" in link and title and link not in seen:
            seen[link] = {
                "title": title,
                "company": "",
                "location": "Ethiopia",
                "link": link,
                "snippet": (item.get("description") or "")[:200],
                "source": "ethiojobs"
            }
    return list(seen.values())


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    try:
        jobs = load_jobs()
        keyword = request.args.get("q", "").lower().strip()

        if keyword:
            words = keyword.split()
            filtered = []
            for j in jobs:
                title = j["title"].lower()
                snippet = j["snippet"].lower()
                if any(w in title or w in snippet for w in words):
                    filtered.append(j)
            # if nothing matches keywords, return ALL jobs anyway
            jobs = filtered if filtered else jobs

        return jsonify({"jobs": jobs, "total": len(jobs)})

    except FileNotFoundError:
        return jsonify({"error": "jobs.json not found. Run scraper.py first.", "jobs": [], "total": 0}), 404
    except Exception as e:
        return jsonify({"error": str(e), "jobs": [], "total": 0}), 500


@app.route("/api/health", methods=["GET"])
def health():
    try:
        jobs = load_jobs()
        return jsonify({"status": "ok", "job_count": len(jobs)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    print("=" * 50)
    print("EthioJobs API starting on http://localhost:5001")
    print("=" * 50)
    app.run(port=5001, debug=True)
