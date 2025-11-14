# Awesome Generative AI - Sharing Tools

This directory contains tools to help share and promote the Awesome Generative AI repository.

## Tools

### 1. Stats Generator (`stats-generator.py`)

Generates comprehensive statistics about the repository that can be shared on social media or documentation.

**Usage:**
```bash
python3 tools/stats-generator.py
```

**Output:**
- `output/stats.json` - Statistics in JSON format
- `output/STATS.md` - Statistics in Markdown format (great for sharing!)

**Features:**
- Counts total projects in main list and discoveries
- Identifies open source projects
- Categorizes projects by section
- Generates shareable statistics

### 2. JSON Exporter (`json-exporter.py`)

Converts the markdown lists to structured JSON format for programmatic access. This enables:
- Building APIs
- Creating search interfaces
- Generating visualizations
- Integrating with other tools

**Usage:**
```bash
python3 tools/json-exporter.py
```

**Output:**
- `output/awesome-generative-ai.json` - Full JSON export (formatted)
- `output/awesome-generative-ai.min.json` - Minified JSON (for web use)

**JSON Structure:**
```json
{
  "metadata": {
    "generated_at": "2024-01-01T00:00:00",
    "version": "1.0"
  },
  "main_list": {
    "projects": [...],
    "categories": [...]
  },
  "discoveries_list": {
    "projects": [...],
    "categories": [...]
  },
  "statistics": {...}
}
```

### 3. Search Interface (`search-interface.html`)

A beautiful, interactive web interface for searching and browsing the list.

**Usage:**
1. First, generate the JSON export:
   ```bash
   python3 tools/json-exporter.py
   ```

2. Open `search-interface.html` in a web browser (requires a local server for CORS):
   ```bash
   # Using Python
   cd tools
   python3 -m http.server 8000
   # Then open http://localhost:8000/search-interface.html
   ```

**Features:**
- Real-time search across project names, descriptions, and categories
- Filter by section, source (main/discoveries), and open source status
- Beautiful, responsive design
- Live statistics

## Quick Start

1. **Generate all outputs:**
   ```bash
   python3 tools/stats-generator.py
   python3 tools/json-exporter.py
   ```

2. **View statistics:**
   ```bash
   cat tools/output/STATS.md
   ```

3. **Use the search interface:**
   ```bash
   cd tools
   python3 -m http.server 8000
   # Open http://localhost:8000/search-interface.html
   ```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Output Directory

All generated files are saved to `tools/output/`:
- `stats.json` - Statistics in JSON
- `STATS.md` - Statistics in Markdown
- `awesome-generative-ai.json` - Full JSON export
- `awesome-generative-ai.min.json` - Minified JSON

## Ideas for Sharing

1. **Social Media:**
   - Share the statistics from `STATS.md` on Twitter/LinkedIn
   - Create visual cards using the stats
   - Highlight interesting categories or open source projects

2. **Documentation:**
   - Include stats in README
   - Create a dedicated stats page
   - Add badges showing project counts

3. **API/Integration:**
   - Use the JSON export to build an API
   - Create a GitHub Action to auto-generate stats
   - Build a website using the JSON data

4. **Community:**
   - Share the search interface link
   - Create visualizations from the JSON data
   - Build browser extensions using the data

## Contributing

Feel free to add more tools! Some ideas:
- Social media card generator
- RSS feed generator
- PDF exporter
- Visualization generator
- API server

## License

Same as the main repository.

