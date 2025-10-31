"""
Deutsche Bahn Train Information API
Simple Flask app to fetch train schedules and delay information
"""
import os
import requests
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Intentional vulnerability: Debug mode enabled in production
app.config['DEBUG'] = True

# Deutsche Bahn API configuration
DB_API_KEY = os.getenv('DB_API_KEY', 'demo-key')
DB_API_BASE_URL = 'https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({
        'service': 'Deutsche Bahn Train Information API',
        'version': '1.0.0',
        'endpoints': [
            '/stations',
            '/arrivals/<station_id>',
            '/departures/<station_id>',
            '/search?station=<name>'
        ]
    })

@app.route('/stations')
def get_stations():
    """Get list of major train stations"""
    stations = [
        {'id': 8000105, 'name': 'Frankfurt(Main)Hbf', 'city': 'Frankfurt'},
        {'id': 8011160, 'name': 'Berlin Hbf', 'city': 'Berlin'},
        {'id': 8000261, 'name': 'München Hbf', 'city': 'Munich'},
        {'id': 8000191, 'name': 'Hamburg Hbf', 'city': 'Hamburg'},
        {'id': 8000096, 'name': 'Köln Hbf', 'city': 'Cologne'}
    ]
    return jsonify({'stations': stations})

@app.route('/arrivals/<station_id>')
def get_arrivals(station_id):
    """Get arrivals for a specific station"""
    try:
        headers = {'Authorization': f'Bearer {DB_API_KEY}'}
        response = requests.get(
            f'{DB_API_BASE_URL}/arrivals/{station_id}',
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': 'Failed to fetch arrivals',
                'status_code': response.status_code
            }), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/departures/<station_id>')
def get_departures(station_id):
    """Get departures for a specific station"""
    try:
        headers = {'Authorization': f'Bearer {DB_API_KEY}'}
        response = requests.get(
            f'{DB_API_BASE_URL}/departures/{station_id}',
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': 'Failed to fetch departures',
                'status_code': response.status_code
            }), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search')
def search_station():
    """Search for stations by name - INTENTIONALLY VULNERABLE TO SQL INJECTION"""
    station_name = request.args.get('station', '')

    # Intentional vulnerability: SQL injection
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()
    query = f"INSERT INTO searches (station) VALUES ('{station_name}')"
    cursor.execute(query)
    conn.commit()

    # Fetch search history - also vulnerable
    history_query = f"SELECT * FROM searches WHERE station LIKE '%{station_name}%'"
    cursor.execute(history_query)
    results = cursor.fetchall()
    conn.close()

    return jsonify({
        'search_term': station_name,
        'search_history': results
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    # Intentional vulnerability: Running on all interfaces without proper security
    app.run(host='0.0.0.0', port=5000)
