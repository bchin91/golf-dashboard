# ⛳ DataGolf Dashboard

A Flask app that proxies the DataGolf API and serves a live betting dashboard.

## File structure

```
golf-render/
├── server.py          ← Flask app (proxy + static file server)
├── requirements.txt   ← Python dependencies
├── Procfile           ← Tells Render how to start the app
└── static/
    └── index.html     ← The dashboard UI
```

## Editing going forward

- **Change the UI** → edit `static/index.html`, commit to GitHub, Render auto-deploys
- **Add/change an API endpoint** → edit `server.py` ROUTES dict, commit, auto-deploys
- No downloads, no Terminal needed after initial setup

## Local dev (optional)

```bash
pip install flask flask-cors requests
python server.py
# open http://localhost:5050
```
