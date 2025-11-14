#!/bin/bash
# Generate all outputs and validate the repository

echo "🚀 Generating all outputs for Awesome Generative AI..."
echo ""

# Create output directory
mkdir -p output

# Validate markdown format
echo "✅ Validating markdown format..."
python3 markdown-validator.py
VALIDATION_EXIT=$?

echo ""

# Generate statistics
echo "📊 Generating statistics..."
python3 stats-generator.py

echo ""

# Generate JSON export
echo "📦 Generating JSON export..."
python3 json-exporter.py

echo ""

# Validate links (non-blocking)
echo "🔗 Validating links (this may take a while)..."
python3 link-validator.py || echo "⚠️  Link validation had some issues (check report)"

echo ""
echo "✅ All outputs generated successfully!"
echo ""
echo "📁 Output files:"
echo "   - output/stats.json"
echo "   - output/STATS.md"
echo "   - output/awesome-generative-ai.json"
echo "   - output/awesome-generative-ai.min.json"
echo "   - output/markdown-validation-report.json"
echo "   - output/link-validation-report.json"
echo ""
echo "🌐 To use the search interface:"
echo "   cd tools && python3 -m http.server 8000"
echo "   Then open http://localhost:8000/search-interface.html"

# Exit with validation status
if [ $VALIDATION_EXIT -ne 0 ]; then
    echo ""
    echo "⚠️  Markdown validation found errors. Please review the report."
    exit $VALIDATION_EXIT
fi

