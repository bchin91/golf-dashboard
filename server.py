"""
DataGolf Dashboard - Server
Runs locally via: python server.py
Runs on Render via: gunicorn server:app
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

API_KEY = os.environ.get('DATAGOLF_KEY', '71b1bfb73a7fee06a62ee432c9fe')
BASE    = 'https://feeds.datagolf.com'

# Every endpoint from datagolf.com/api-access, verified against docs
ROUTES = {
    # ── General Use ──────────────────────────────────────────────────────────
    'player-list':              '/get-player-list',
    'schedule':                 '/get-schedule',
    'field-updates':            '/field-updates',

    # ── Model Predictions ────────────────────────────────────────────────────
    'dg-rankings':              '/preds/get-dg-rankings',
    'pre-tournament':           '/preds/pre-tournament',
    'pre-tournament-archive':   '/preds/pre-tournament-archive',
    'skill-decompositions':     '/preds/player-decompositions',
    'skill-ratings':            '/preds/skill-ratings',
    'approach-skill':           '/preds/approach-skill',
    'fantasy-projections':      '/preds/fantasy-projection-defaults',

    # ── Live Model ───────────────────────────────────────────────────────────
    'live-model':               '/preds/in-play',
    'live-tournament-stats':    '/preds/live-tournament-stats',
    'live-hole-stats':          '/preds/live-hole-stats',

    # ── Betting Tools ────────────────────────────────────────────────────────
    'outrights':                '/betting-tools/outrights',
    'matchups':                 '/betting-tools/matchups',
    'matchups-all-pairings':    '/betting-tools/matchups-all-pairings',

    # ── Historical Raw Data ──────────────────────────────────────────────────
    'historical-event-list':    '/historical-raw-data/event-list',
    'historical-rounds':        '/historical-raw-data/rounds',

    # ── Historical Event Stats ───────────────────────────────────────────────
    'event-data-list':          '/historical-event-data/event-list',
    'event-data':               '/historical-event-data/events',

    # ── Historical Odds ──────────────────────────────────────────────────────
    'historical-odds-list':     '/historical-odds/event-list',
    'historical-outrights':     '/historical-odds/outrights',
    'historical-matchups':      '/historical-odds/matchups',

    # ── Historical DFS ───────────────────────────────────────────────────────
    'dfs-event-list':           '/historical-dfs-data/event-list',
    'dfs-points':               '/historical-dfs-data/points',
}

@app.route('/api/<path:endpoint>')
def proxy(endpoint):
    path = ROUTES.get(endpoint)
    if not path:
        return jsonify({
            'error': f'Unknown endpoint "{endpoint}"',
            'available': list(ROUTES.keys())
        }), 404

    params = dict(request.args)
    params['key'] = API_KEY
    params.setdefault('file_format', 'json')

    url = BASE + path
    print(f'  → {url}  {params}')

    try:
        r = requests.get(url, params=params, timeout=15)
        print(f'  ← {r.status_code}  {len(r.content)}b')
        r.raise_for_status()
        return jsonify(r.json())
    except requests.exceptions.HTTPError as e:
        try:    detail = r.json()
        except: detail = r.text
        print(f'  ✗ {e}  {detail}')
        return jsonify({'error': str(e), 'detail': detail}), r.status_code
    except Exception as e:
        print(f'  ✗ {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f'\n  ⛳  Golf Dashboard → http://localhost:{port}\n')
    app.run(host='0.0.0.0', port=port, debug=False)
