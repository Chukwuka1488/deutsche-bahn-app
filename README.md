# Deutsche Bahn Train Information API

A simple Flask API for fetching train schedules and delay information from Deutsche Bahn.

## ⚠️ WARNING: Intentional Vulnerabilities

This application contains **intentional security vulnerabilities** for testing SpellCarver's security scanning capabilities. **DO NOT use in production!**

### Known Vulnerabilities Included:

#### Code-Level Vulnerabilities (SAST):
- **SQL Injection**: `/search` endpoint uses string concatenation for SQL queries
- **Debug Mode Enabled**: Flask debug mode enabled in production
- **Insecure Server Configuration**: Running on all interfaces (0.0.0.0)
- **No Input Validation**: User input not sanitized

#### Dependency Vulnerabilities (SCA/Image Scan):
- **Flask 2.2.2**: Known CVE-2023-30861 (Information Disclosure)
- **Werkzeug 2.2.2**: Various security issues
- **urllib3 1.26.5**: Multiple CVEs
- **cryptography 3.3.2**: Known vulnerabilities
- **PyYAML 5.3.1**: CVE-2020-14343 (Unsafe Deserialization)
- **Jinja2 3.0.1**: Template injection vulnerabilities

#### Container Vulnerabilities:
- Running as root user
- Using outdated Python 3.8-slim base image
- No health checks defined
- Missing security best practices

## API Endpoints

### `GET /`
Returns service information and available endpoints.

### `GET /stations`
Returns a list of major German train stations.

### `GET /arrivals/<station_id>`
Get arrival information for a specific station.

### `GET /departures/<station_id>`
Get departure information for a specific station.

### `GET /search?station=<name>`
Search for stations by name. ⚠️ **VULNERABLE TO SQL INJECTION**

### `GET /health`
Health check endpoint.

## Setup

### Environment Variables
- `DB_API_KEY`: Deutsche Bahn API key (optional, uses demo key by default)

### Running Locally
```bash
pip install -r requirements.txt
python app.py
```

### Running with Docker
```bash
docker build -t deutsche-bahn-app .
docker run -p 5000:5000 deutsche-bahn-app
```

## Testing with SpellCarver

This app is designed to trigger multiple security scans:

1. **SAST Scan (Bearer)**: Will detect SQL injection and insecure configurations
2. **Image Scan (Trivy)**: Will find vulnerable dependencies and container issues
3. **SBOM Generation**: Will catalog all dependencies and their versions

Expected scan results:
- Critical: 5+ vulnerabilities
- High: 10+ vulnerabilities
- Medium: 20+ vulnerabilities
- Low: Various warnings

## Sample Stations

- Frankfurt: 8000105
- Berlin: 8011160
- Munich: 8000261
- Hamburg: 8000191
- Cologne: 8000096

## License

MIT License - For educational and testing purposes only.
