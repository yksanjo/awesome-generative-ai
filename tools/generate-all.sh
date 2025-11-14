#!/bin/bash
# Generate all outputs for sharing the repository

echo "🚀 Generating all outputs for Awesome Generative AI..."
echo ""

# Create output directory
mkdir -p output

# Generate statistics
echo "📊 Generating statistics..."
python3 stats-generator.py

echo ""

# Generate JSON export
echo "📦 Generating JSON export..."
python3 json-exporter.py

echo ""
echo "✅ All outputs generated successfully!"
echo ""
echo "📁 Output files:"
echo "   - output/stats.json"
echo "   - output/STATS.md"
echo "   - output/awesome-generative-ai.json"
echo "   - output/awesome-generative-ai.min.json"
echo ""
echo "🌐 To use the search interface:"
echo "   cd tools && python3 -m http.server 8000"
echo "   Then open http://localhost:8000/search-interface.html"

