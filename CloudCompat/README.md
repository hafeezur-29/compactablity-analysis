# CloudCompat

A lightweight cloud compatibility analyzer for websites and web applications.

## Features
- URL health and response-time check
- Basic technology detection
- CPU / RAM / storage estimation
- Cloud machine compatibility comparison
- Recommended cloud profile
- Docker-ready deployment
- Clean responsive dashboard

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

## Run with Docker
```bash
docker compose up --build
```

## Important scope
No tool can safely execute literally "any" arbitrary app from an untrusted URL.
This starter analyzes public websites and is Docker-ready for applications you control.
For production arbitrary-app execution, add authenticated uploads, a sandbox,
network policy, CPU/RAM/time limits, image scanning and an isolated worker host.
