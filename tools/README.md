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
# Basic export
python3 tools/json-exporter.py

# With GitHub stats (stars, forks, etc.)
python3 tools/json-exporter.py --github-stats

# With GitHub token for higher rate limits
python3 tools/json-exporter.py --github-stats --github-token YOUR_TOKEN
```

**Output:**
- `output/awesome-generative-ai.json` - Full JSON export (formatted)
- `output/awesome-generative-ai.min.json` - Minified JSON (for web use)

**Features:**
- Optional GitHub statistics fetching (stars, forks, language, etc.)
- Supports GitHub personal access tokens for higher API rate limits
- Includes metadata about when stats were fetched

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

### 3. Link Validator (`link-validator.py`)

Validates all URLs in README.md and DISCOVERIES.md to check for broken or dead links.

**Usage:**
```bash
# Install required dependency first
pip install requests

# Run validator
python3 tools/link-validator.py
```

**Output:**
- `output/link-validation-report.json` - Detailed validation report

**Features:**
- Checks all URLs for accessibility
- Handles timeouts and connection errors gracefully
- Skips domains that may block automated requests (Twitter, LinkedIn)
- Provides detailed error messages
- Exit code indicates success/failure (useful for CI/CD)

### 4. Markdown Validator (`markdown-validator.py`)

Validates markdown entries against contribution guidelines to ensure quality and consistency.

**Usage:**
```bash
python3 tools/markdown-validator.py
```

**Output:**
- `output/markdown-validation-report.json` - Detailed validation report

**Features:**
- Validates entry format: `[ProjectName](Link) - Description.`
- Checks for trailing periods in descriptions
- Detects duplicate entries
- Validates URL formats
- Checks for trailing whitespace
- Warns about overly long descriptions
- Exit code indicates success/failure (useful for CI/CD)

### 5. Search Interface (`search-interface.html`)

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

1. **Install dependencies:**
   ```bash
   pip install requests  # Required for link-validator.py
   ```

2. **Generate all outputs:**
   ```bash
   python3 tools/stats-generator.py
   python3 tools/json-exporter.py
   ```

3. **Validate the list:**
   ```bash
   python3 tools/markdown-validator.py
   python3 tools/link-validator.py
   ```

4. **View statistics:**
   ```bash
   cat tools/output/STATS.md
   ```

5. **Use the search interface:**
   ```bash
   cd tools
   python3 -m http.server 8000
   # Open http://localhost:8000/search-interface.html
   ```

## Requirements

- Python 3.6+
- `requests` library (for link-validator.py and GitHub stats in json-exporter.py)
  ```bash
  pip install requests
  ```
- All other tools use only the Python standard library

## Output Directory

All generated files are saved to `tools/output/`:
- `stats.json` - Statistics in JSON
- `STATS.md` - Statistics in Markdown
- `awesome-generative-ai.json` - Full JSON export
- `awesome-generative-ai.min.json` - Minified JSON
- `link-validation-report.json` - Link validation results
- `markdown-validation-report.json` - Markdown validation results

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

