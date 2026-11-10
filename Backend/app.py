
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter
import csv
import io

app = Flask(__name__)

# Allow frontend access
CORS(app)

# Sample cybersecurity logs
logs = [
    {
        "ip": "192.168.1.105",
        "user": "admin",
        "event": "Failed Login",
        "severity": "Critical",
        "status": "Blocked"
    },
    {
        "ip": "45.142.212.61",
        "user": "unknown",
        "event": "Port Scan",
        "severity": "High",
        "status": "Flagged"
    },
    {
        "ip": "10.0.0.24",
        "user": "student01",
        "event": "Successful Login",
        "severity": "Low",
        "status": "Allowed"
    },
    {
        "ip": "103.82.21.9",
        "user": "root",
        "event": "Malware Alert",
        "severity": "Critical",
        "status": "Quarantined"
    },
    {
        "ip": "172.16.0.8",
        "user": "user02",
        "event": "Failed Login",
        "severity": "Medium",
        "status": "Flagged"
    }
]


# Home page
@app.route("/")
def home():
    return jsonify({
        "project": "Cybersecurity Log Analytics",
        "backend": "Flask",
        "status": "Running"
    })


# Get all logs
@app.route("/api/logs")
def get_logs():
    return jsonify(logs)


# Dashboard statistics
@app.route("/api/stats")
def get_stats():

    total = len(logs)

    threats = sum(
        1 for log in logs
        if log["severity"] in ["Critical", "High"]
    )

    failed = sum(
        1 for log in logs
        if log["event"] == "Failed Login"
    )

    return jsonify({
        "total_logs": total,
        "threats_detected": threats,
        "failed_logins": failed
    })


# Analyze security logs
@app.route("/api/analyze")
def analyze_logs():

    severity = Counter(
        log["severity"] for log in logs
    )

    events = Counter(
        log["event"] for log in logs
    )

    return jsonify({
        "severity_analysis": dict(severity),
        "event_analysis": dict(events)
    })


# Upload CSV file
@app.route("/api/upload", methods=["POST"])
def upload_logs():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        content = file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))

        count = 0

        for row in reader:
            logs.append({
                "ip": row.get("ip", "Unknown"),
                "user": row.get("user", "Unknown"),
                "event": row.get("event", "Unknown"),
                "severity": row.get("severity", "Medium"),
                "status": row.get("status", "Imported")
            })
            count += 1

        return jsonify({
            "message": "Upload successful",
            "records_added": count,
            "total_logs": len(logs)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# MapReduce demo
@app.route("/api/mapreduce", methods=["POST"])
def mapreduce():

    severity_count = Counter(
        log["severity"] for log in logs
    )

    event_count = Counter(
        log["event"] for log in logs
    )

    return jsonify({
        "status": "Completed",
        "mapper": "Logs converted into key-value pairs",
        "reducer": "Records aggregated",
        "severity_results": dict(severity_count),
        "event_results": dict(event_count)
    })


if __name__ == "__main__":
    app.run()
